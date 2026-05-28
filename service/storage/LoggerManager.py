import logging
import os
import config

class LoggerManager:
    def __init__(self, log_name="DeserterBot", logging_level=logging.DEBUG):
        self.log_dir = "logs"
        self._ensure_log_dir()
        self.log_file = os.path.join(self.log_dir, config.LOGGER_FILE_NAME)

        self._logger = logging.getLogger(log_name)
        self._logger.setLevel(logging_level)

        logging.getLogger('nicegui.binding').setLevel(logging.WARNING)

        # Запобігаємо дублюванню логів, якщо об'єкт створюється двічі
        if not self._logger.handlers:
            self._setup_handlers()

    def debug(self, message: str):
        self._logger.debug(message)
    def warning(self, message: str):
        self._logger.warning(message)
    def error(self, message: str):
        self._logger.error(message)
    def info(self, message: str):
        self._logger.info(message)
    def getEffectiveLoggerLevel(self):
        return self._logger.getEffectiveLevel()
    def setEffectiveLoggerLevel(self, level):
        self._logger.setLevel(level)

    def _ensure_log_dir(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _setup_handlers(self):
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Файловий хендлер
        self.file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        self.file_handler.setFormatter(formatter)
        self._logger.addHandler(self.file_handler)

        # Консольний хендлер
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

    def clear_log(self, keep_lines=5):
        try:
            if os.path.exists(self.log_file):
                # 1. Читаємо всі рядки
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # 2. Залишаємо тільки хвіст (наприклад, останні 5 рядків)
                tail = lines[-keep_lines:] if len(lines) > keep_lines else lines

                # 3. Перезаписуємо файл цим хвостом
                with open(self.log_file, 'w', encoding='utf-8') as f:
                    f.writelines(tail)

                self._logger.debug(f"--- 🔄 Лог очищено. Залишено останніх рядків: {len(tail)} ---")
        except Exception as e:
            # Важливо не дати скрипту впасти, якщо лог зайнятий іншим процесом
            print(f"Помилка при очищенні логу: {e}")

    def get_logger(self):
        return self._logger

    def get_log_path(self):
        return self.log_file
