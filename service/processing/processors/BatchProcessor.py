from service.storage.LoggerManager import LoggerManager
from service.storage.StorageFactory import StorageFactory

class BatchProcessor:
    def __init__(self, log_manager: LoggerManager, excel_file_path):
        self.fileProxy = StorageFactory.create_client(excel_file_path, log_manager)
        self.log_manager = log_manager

    def start_processing(self, days_back=1):
        self.log_manager.debug("🚀 >>> BATCH STARTED")
