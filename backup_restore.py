import subprocess
from datetime import datetime
import os
import glob

# Настройки
BACKUP_DIR = "./mongo_backups"
DB_NAME = "practice_db"
CONTAINER_NAME = "mongodb"
USERNAME = "root"
PASSWORD = "example123"

def create_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"{DB_NAME}_{timestamp}")
    
    try:
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        cmd = [
            "docker", "exec", CONTAINER_NAME, "mongodump",
            "--uri", f"mongodb://{USERNAME}:{PASSWORD}@mongodb:27017/",
            "--db", DB_NAME,
            "--out", "/backup/backup_manual",
            "--authenticationDatabase", "admin"
        ]
        
        subprocess.run(cmd, check=True)
        
        # Копируем бэкап из контейнера на хост
        subprocess.run([
            "docker", "cp",
            f"{CONTAINER_NAME}:/backup/backup_manual/{DB_NAME}",
            backup_path
        ], check=True)
        
        print(f"✅ Бэкап создан: {backup_path}")
        return backup_path
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка бэкапа: {e}")
        return None

def restore_backup(backup_path):
    if not os.path.exists(backup_path):
        print(f"❌ Путь не существует: {backup_path}")
        return
    
    try:
        subprocess.run([
            "docker", "exec", "mongodb", "mkdir", "-p", "/backup/restore"
        ], check=True)

        subprocess.run([
            "docker", "cp",
            backup_path,
            f"{CONTAINER_NAME}:/backup/restore/{DB_NAME}"
        ], check=True)
        
        cmd = [
            "docker", "exec", CONTAINER_NAME, "mongorestore",
            "-u", USERNAME,
            "-p", PASSWORD,
            "--host", "mongodb",
            "--db", DB_NAME,
            "--drop",
            f"/backup/restore/{DB_NAME}",
            "--authenticationDatabase", "admin"
        ]
 
        subprocess.run(cmd, check=True)
        print(f"✅ Данные восстановлены из: {backup_path}")
        
        subprocess.run([
            "docker", "exec", CONTAINER_NAME, "rm", "-rf", "/backup/restore"
        ], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка восстановления: {e}")

def get_latest_backup():
    """Возвращает путь к последнему бэкапу"""
    # Получаем список всех директорий бэкапов
    backup_dirs = glob.glob(os.path.join(BACKUP_DIR, f"{DB_NAME}_*"))
    if not backup_dirs:
        return None

    # Функция для извлечения временной метки из имени директории
    def extract_timestamp(backup_path):
        # Извлекаем часть имени, соответствующую временной метке
        base_name = os.path.basename(backup_path)
        # Убираем префикс имени базы данных и расширение
        timestamp_str = base_name[len(DB_NAME) + 1:]
        return datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")

    # Находим последний бэкап по временной метке
    latest_backup = max(backup_dirs, key=extract_timestamp)
    return latest_backup


if __name__ == "__main__":
    print("1. Создать бэкап")
    print("2. Восстановить последний бэкап")
    choice = input("Выберите действие: ")
    
    if choice == "1":
        create_backup()
    elif choice == "2":
        latest_backup = get_latest_backup()
        if latest_backup:
            print(f"Восстанавливаем из: {latest_backup}")
            restore_backup(latest_backup)
        else:
            print("❌ Нет доступных бэкапов")