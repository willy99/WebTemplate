"""Inbox business logic — file listing, download, assign, delete, upload."""
from service.storage.LoggerManager import LoggerManager
from service.storage.StorageFactory import StorageFactory
import config
from typing import Dict, List
from gui.services.request_context import RequestContext
import io


class InboxService:
    def __init__(self, log_manager: LoggerManager, ctx: RequestContext):
        self.log_manager = log_manager
        self.ctx = ctx

    def get_user_inbox_messages(self) -> Dict[str, List[str]]:
        client = StorageFactory.create_client(config.INBOX_DIR_PATH, self.log_manager)
        result = {'root_files': [], 'personal_files': [], 'outbox_files': []}
        try:
            with client:
                try:
                    root_items = client.list_files(config.INBOX_DIR_PATH, silent=True, exclude_dirs=True)
                    result['root_files'] = [f for f in root_items if not f.startswith('.')]
                except Exception as e:
                    self.log_manager.error(f"Помилка читання кореня Inbox: {e}")

                if self.ctx.user_login:
                    user_path = f"{config.INBOX_DIR_PATH}{client.get_separator()}{self.ctx.user_login}"
                    outbox_path = f"{config.OUTBOX_DIR_PATH}{client.get_separator()}{self.ctx.user_login}"
                    try:
                        u_items = client.list_files(user_path, silent=True, exclude_dirs=False)
                        if u_items:
                            result['personal_files'] = [f for f in u_items if not f.startswith('.')]
                        u_items = client.list_files(outbox_path, silent=True, exclude_dirs=False)
                        if u_items:
                            result['outbox_files'] = [f for f in u_items if not f.startswith('.')]
                    except Exception:
                        pass
        except Exception as e:
            self.log_manager.error(f"Критична помилка доступу до Inbox Service: {e}")
        return result

    def download_file(self, personal_folder: str, filename: str, root_dir: str) -> io.BytesIO:
        client = StorageFactory.create_client(root_dir, self.log_manager)
        if personal_folder:
            target_path = f"{root_dir}{client.get_separator()}{personal_folder}{client.get_separator()}{filename}"
        else:
            target_path = f"{root_dir}{client.get_separator()}{filename}"
        with client:
            try:
                return client.get_file_buffer(self.ctx, target_path)
            except Exception as e:
                self.log_manager.error(f"Помилка завантаження файлу {target_path}: {e}")
                raise

    def assign_file(self, personal_folder: str, filename: str, target_user: str, source_folder=None):
        if not source_folder:
            source_folder = config.INBOX_DIR_PATH
        root_dir = source_folder
        client = StorageFactory.create_client(root_dir, self.log_manager)
        if personal_folder:
            src_path = f"{root_dir}{client.get_separator()}{personal_folder}{client.get_separator()}{filename}"
        else:
            src_path = f"{root_dir}{client.get_separator()}{filename}"
        dest_dir = f"{root_dir}{client.get_separator()}{target_user}"
        dest_path = f"{dest_dir}{client.get_separator()}{filename}"
        with client:
            try:
                client.make_dirs(dest_dir)
                client.move_file(src_path, dest_path)
            except Exception as e:
                self.log_manager.error(f"Помилка призначення файлу {filename} для {target_user}: {e}")
                raise

    def delete_file(self, personal_folder: str, folder: str, filename: str):
        client = StorageFactory.create_client(config.INBOX_DIR_PATH, self.log_manager)
        if personal_folder:
            target_path = f"{folder}{client.get_separator()}{personal_folder}{client.get_separator()}{filename}"
        else:
            target_path = f"{folder}{client.get_separator()}{filename}"
        with client:
            try:
                client.remove_file(target_path)
                self.log_manager.debug(f"🗑️ Файл видалено: {target_path}")
            except Exception as e:
                self.log_manager.error(f"❌ Помилка видалення файлу {target_path}: {e}")
                raise

    def upload_file_to_root(self, filename: str, file_data: bytes):
        buffer = io.BytesIO(file_data)
        root_dir = config.INBOX_DIR_PATH
        client = StorageFactory.create_client(root_dir, self.log_manager)
        target_path = f"{root_dir}{client.get_separator()}{filename}"
        with client:
            try:
                client.save_file_from_buffer(target_path, buffer)
                self.log_manager.debug(f"⬆️ Файл успішно завантажено в корінь: {target_path}")
            except Exception as e:
                self.log_manager.error(f"❌ Помилка завантаження файлу {target_path}: {e}")
                raise
