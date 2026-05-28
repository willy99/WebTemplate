# service/processing/DocumentProcessingService.py
from typing import List, Dict, Any, Optional, Tuple

import config
from service.storage.LoggerManager import LoggerManager
from utils.utils import get_effective_date
import unicodedata
import traceback
from service.storage.StorageFactory import StorageFactory
import tempfile

class DocumentProcessingService:
    def __init__(self, log_manager: LoggerManager, backuper: Optional[Any] = None, person_service = None) -> None:
        self.log_manager = log_manager
        self.backuper = backuper
        self.fileProxy = StorageFactory.create_client(config.DOCUMENT_STORAGE_PATH, self.log_manager)
        self.person_service = person_service

    def make_backup(self) -> bool:
        """1. Створення резервної копії бази/Excel."""
        if self.backuper:
            try:
                self.backuper.make_backup()
                return True
            except Exception as e:
                self.log_manager.error(f"❌ Помилка під час бекапу: {e}")
                return False
        return True  # Якщо бекапер не переданий, вважаємо, що все ОК

    def archive_document(self, source_file_path: str, original_filename: str) -> Optional[str]:
        """2. Копіювання файлу у цільову (впорядковану) папку."""
        effective_date = get_effective_date()
        original_filename = unicodedata.normalize('NFC', original_filename)
        target_path = self.fileProxy.get_target_folder_path(effective_date, config.DOCUMENT_STORAGE_PATH)

        try:
            with StorageFactory.create_client(config.DOCUMENT_STORAGE_PATH, self.log_manager) as client:
                destination_file = f"{target_path}{client.separator}{original_filename}"
                return destination_file
        except Exception as e:
            self.log_manager.error(f"❌ Помилка архівації документа: {e}")
            self.log_manager.debug(traceback.format_exc())
            return None
