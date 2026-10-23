#include <windows.h>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>
#include <thread>
#include <chrono>

// ==========================================
// ЧАСТЬ 1: ЖУТКИЕ ИЕРОГЛИФЫ (ЮНИКОД)
// ==========================================
std::wstring GetSpookyText() {
    const wchar_t* symbols[] = { L"♆", L"☠", L"⛧", L"᚛", L"᚜", L"ᚉ", L"ᚒ", L"ᛟ", L"ᛉ", L"ᛊ", L"✠", L"✙" };
    std::wstring result;
    for (int i = 0; i < 5; i++) {
        result += symbols[rand() % 12];
    }
    return result;
}

// ==========================================
// ЧАСТЬ 2: РАЗРУШЕНИЕ ФАЙЛОВ
// ==========================================
void DestroyFiles() {
    // Просто создаем мусорные файлы, чтобы не ждать долго
    wchar_t userProfile[MAX_PATH];
    GetEnvironmentVariableW(L"USERPROFILE", userProfile, MAX_PATH);
    std::wstring desktop = std::wstring(userProfile) + L"\\Desktop\\";
    
    for (int i = 0; i < 50; i++) {
        std::wstring filePath = desktop + L"HELPED_" + std::to_wstring(i) + L".txt";
        HANDLE hFile = CreateFileW(filePath.c_str(), GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
        if (hFile != INVALID_HANDLE_VALUE) {
            const char* data = "I HELPED YOU >:D";
            DWORD written;
            WriteFile(hFile, data, strlen(data), &written, NULL);
            CloseHandle(hFile);
        }
    }
}

// ==========================================
// ЧАСТЬ 3: УВЕДОМЛЕНИЕ (С ЖУТКИМ ТЕКСТОМ)
// ==========================================
void ShowNotification() {
    std::wstring text = L"Hello, I am " + GetSpookyText() + L". I want to help you with the files!";
    MessageBoxW(NULL, text.c_str(), L"SYSTEM HELPER", MB_OK | MB_ICONWARNING);
}

// ==========================================
// ЧАСТЬ 4: РИСУЕМ ЖУТКОЕ ЛИЦО (GDI)
// ==========================================
void DrawScaryFace() {
    HDC hdc = GetDC(NULL);
    int w = GetSystemMetrics(SM_CXSCREEN);
    int h = GetSystemMetrics(SM_CYSCREEN);

    // Черный фон
    HBRUSH blackBrush = CreateSolidBrush(RGB(0, 0, 0));
    RECT rect = { 0, 0, w, h };
    FillRect(hdc, &rect, blackBrush);
    DeleteObject(blackBrush);

    // Красные глаза
    HBRUSH redBrush = CreateSolidBrush(RGB(255, 0, 0));
    Ellipse(hdc, w/2 - 200, h/2 - 200, w/2 - 50, h/2 - 50);
    Ellipse(hdc, w/2 + 50, h/2 - 200, w/2 + 200, h/2 - 50);
    DeleteObject(redBrush);

    // Черные зрачки
    HBRUSH blackEyeBrush = CreateSolidBrush(RGB(0, 0, 0));
    Ellipse(hdc, w/2 - 150, h/2 - 150, w/2 - 100, h/2 - 100);
    Ellipse(hdc, w/2 + 100, h/2 - 150, w/2 + 150, h/2 - 100);
    DeleteObject(blackEyeBrush);

    // Кровавая улыбка (красная линия)
    HPEN redPen = CreatePen(PS_SOLID, 10, RGB(255, 0, 0));
    SelectObject(hdc, redPen);
    Arc(hdc, w/2 - 150, h/2 + 50, w/2 + 150, h/2 + 250, w/2 - 150, h/2 + 150, w/2 + 150, h/2 + 150);
    DeleteObject(redPen);

    // Текст
    SetTextColor(hdc, RGB(255, 0, 0));
    SetBkMode(hdc, TRANSPARENT);
    const wchar_t* text = L"I AM HELPING YOU >:D";
    TextOutW(hdc, w/2 - 150, h/2 + 300, text, wcslen(text));

    ReleaseDC(NULL, hdc);
}

// ==========================================
// ГЛАВНАЯ ФУНКЦИЯ
// ==========================================
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    srand(time(NULL));

    // 1. Показываем уведомление
    ShowNotification();

    // 2. В фоне разрушаем файлы
    std::thread destroyThread(DestroyFiles);
    destroyThread.detach();

    // 3. Ждем 3 секунды и показываем жуткое лицо
    std::this_thread::sleep_for(std::chrono::seconds(3));
    DrawScaryFace();

    // Держим программу открытой, чтобы лицо не исчезло
    while (true) {
        Sleep(1000);
    }

    return 0;
}
