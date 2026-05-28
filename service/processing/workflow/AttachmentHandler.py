import os
import config
from gui.services.request_context import RequestContext
from service.processing.DocumentProcessingService import DocumentProcessingService
from service.storage.StorageFactory import StorageFactory
from utils.utils import sanitize_filename


class AttachmentHandler:
    def __init__(self, workflow):
        # Залишаємо workflow, бо його передає MyWorkFlow (Signal-бот)
        self.workflow = workflow
        self.log_manager = self.workflow.log_manager
        self.system_context = RequestContext(
                                    user_id=None,
                                    user_login='system',
                                    user_role='admin',
                                    user_name='system'
                                )


    def handle_attachment(self, attachment_id, original_filename) -> list[str]:
        # --- БЕЗПЕКА: Санітизація імені файлу ---
        safe_original_filename = sanitize_filename(original_filename)

        if safe_original_filename != original_filename:
            self.log_manager.warning(f"⚠️ Підозріле ім'я файлу змінено: {original_filename} -> {safe_original_filename}")

        # 1. Знаходимо локальний файл, який завантажив Signal
        source_file = os.path.join(config.SIGNAL_ATTACHMENTS_DIR, attachment_id)
        if not os.path.exists(source_file):
            self.log_manager.error(f"❌ Файл {source_file} не знайдено в системній папці Signal.")
            return []

        # 2. Ініціалізуємо сервіс обробки
        processor_service = DocumentProcessingService(
            log_manager=self.workflow.log_manager,
            backuper=self.workflow.backuper,
            excel_processor=self.workflow.excelProcessor
        )

        return []