import os
import io
import config
from service.constants import DB_DATE_FORMAT
from service.storage.StorageFactory import StorageFactory
from datetime import datetime, timedelta
import zipfile
from service.storage.LoggerManager import LoggerManager

class BackupData:
    def __init__(self, log_manager: LoggerManager):
        # self.source_file = config.DESERTER_XLSX_FILE_PATH
        # Базовий шлях для бекапів (тепер беремо з config)
        self.base_backup_path = config.BACKUP_STORAGE_PATH
        self.log_manager = log_manager

    def make_backup(self) -> str:
        effective_date = datetime.now().date()
        return ""


    def _check_remote_dir_exists(self, client, path):
        """Допоміжна перевірка для SMB клієнта, якщо os.path.exists не працює з UNC."""
        try:
            client.list_files(path, silent=True)
            return True
        except:
            return False

    def cleanupOldBackups(self, n_days: int):
        """Видаляє папки бекапів, які старіші за n_days."""
        self.log_manager.debug(f"--- 🧹 Очищення бекапів старіше за {n_days} днів...")

        limit_date = datetime.now() - timedelta(days=n_days)

        with StorageFactory.create_client(self.base_backup_path, self.log_manager) as client:
            try:
                # 1. Отримуємо список років
                years = client.list_files(self.base_backup_path, silent=True)
                for year in years:
                    year_path = f"{self.base_backup_path.rstrip(client.separator)}{client.separator}{year}"

                    # 2. Отримуємо місяці
                    months = client.list_files(year_path, silent=True)
                    for month in months:
                        month_path = f"{year_path}{client.separator}{month}"

                        # 3. Отримуємо дні (папки типу 15.02.2026)
                        days = client.list_files(month_path, silent=True)
                        for day_folder in days:
                            day_path = f"{month_path}{client.separator}{day_folder}"

                            # Спробуємо розпарсити дату з назви папки (якщо формат 15.02.2026)
                            try:
                                # Формат має збігатися з вашим config.FOLDER_DAY_FORMAT
                                folder_date = datetime.strptime(day_folder, config.FOLDER_DAY_FORMAT)

                                if folder_date < limit_date:
                                    self._delete_dir_recursive(client, day_path)
                                    self.log_manager.debug(f"--- 🗑️ Видалено застарілий бекап: {day_path}")
                            except ValueError:
                                # Якщо папка має інший формат назви — ігноруємо
                                continue
            except Exception as e:
                self.log_manager.warning(f"⚠️ Помилка під час очищення старіх бекапів: {e}")

    def _delete_dir_recursive(self, client, path: str):
        """Рекурсивне видалення папки через клієнт."""
        # У SMBFileClient треба буде додати методи для видалення файлів та папок
        # Наразі, якщо це SMB, можна використати smbclient.rmdir / remove
        import smbclient
        try:
            # Для SMB:
            if path.startswith("\\\\"):
                # Спочатку видаляємо файли всередині
                files = client.list_files(path, silent=True)
                for f in files:
                    smbclient.remove(f"{path}{client.separator}{f}")
                # Потім саму папку
                smbclient.rmdir(path)
            else:
                # Для локального диска:
                import shutil
                shutil.rmtree(path)
        except Exception as e:
            self.log_manager.error(f"❌ Не вдалося видалити {path}: {e}")