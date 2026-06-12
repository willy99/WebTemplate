import os
import stat
from typing import Final
from dotenv import load_dotenv
import sys

load_dotenv()

def get_env_bool(var_name: str, default: bool = False) -> bool:
    val = os.getenv(var_name, str(default)).lower()
    return val in ("true", "1", "yes", "on")

def is_win()->bool:
    return sys.platform == "win32"

def _validate_env_win() -> None:
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

    if not os.path.exists(env_path):
        print("⚠️  .env файл не знайдено. Змінні оточення мають бути встановлені вручну.")
        return
    file_mode = os.stat(env_path).st_mode & 0o777
    if file_mode & 0o077:  # group або other мають хоч якийсь доступ
        print(f"🚨 SECURITY: .env має небезпечні права {oct(file_mode)}. Виправляю на 600...")
        os.chmod(env_path, stat.S_IRUSR | stat.S_IWUSR)  # 0o600
        print("✅ Права .env виправлено: тепер тільки власник може читати файл.")

    required = {
        'UI_SECRET_KEY': 'Ключ підпису сесій (обов\'язковий для безпеки UI)',
        'NET_PASSWORD':  'Пароль до мережевого сховища',
        'EMAIL_PASSWORD': 'Пароль до SMTP (потрібен для 2FA через Email)',
    }
    missing = [f"  • {var}  ({desc})" for var, desc in required.items() if not os.getenv(var)]
    if missing:
        print("🚨 SECURITY: Відсутні обов'язкові змінні оточення:")
        for m in missing:
            print(m)
        if not os.getenv('UI_SECRET_KEY'):
            print("💀 UI_SECRET_KEY відсутній — сесії непідписані. Зупиняю запуск.")
            sys.exit(1)
        print("   Деякі функції можуть не працювати. Заповніть .env файл.")


def _validate_env_mac() -> None:
    """
    Перевіряє безпеку .env файлу при кожному старті.
    1. Автоматично виправляє права доступу якщо вони надто широкі.
    2. Попереджає про відсутні обов'язкові змінні.
    """
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')

    if not os.path.exists(env_path):
        print("⚠️  .env файл не знайдено. Змінні оточення мають бути встановлені вручну.")
        return

    # --- Перевірка прав доступу ---
    file_mode = os.stat(env_path).st_mode & 0o777
    if file_mode & 0o077:  # group або other мають хоч якийсь доступ
        print(f"🚨 SECURITY: .env має небезпечні права {oct(file_mode)}. Виправляю на 600...")
        os.chmod(env_path, stat.S_IRUSR | stat.S_IWUSR)  # 0o600
        print("✅ Права .env виправлено: тепер тільки власник може читати файл.")

    # --- Перевірка наявності обов'язкових змінних ---
    required = {
        'UI_SECRET_KEY': 'Ключ підпису сесій (обов\'язковий для безпеки UI)',
        'NET_PASSWORD':  'Пароль до мережевого сховища',
        'EMAIL_PASSWORD': 'Пароль до SMTP (потрібен для 2FA через Email)',
    }
    missing = [f"  • {var}  ({desc})" for var, desc in required.items() if not os.getenv(var)]
    if missing:
        print("🚨 SECURITY: Відсутні обов'язкові змінні оточення:")
        for m in missing:
            print(m)
        if not os.getenv('UI_SECRET_KEY'):
            print("💀 UI_SECRET_KEY відсутній — сесії непідписані. Зупиняю запуск.")
            sys.exit(1)
        print("   Деякі функції можуть не працювати. Заповніть .env файл.")

if is_win():
    _validate_env_win()
else:
    _validate_env_mac()

PROJECT_TITLE = "Web Template"
IS_DEV = '--dev' in sys.argv

NET_SERVER_IP = os.getenv("NET_SERVER_IP", "192.168.0.53")
NET_USERNAME = os.getenv("NET_USERNAME")
NET_PASSWORD = os.getenv("NET_PASSWORD")
UI_SECRET_KEY = os.getenv("UI_SECRET_KEY")

EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER")
EMAIL_SMTP_PORT = os.getenv("EMAIL_SMTP_PORT")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

if IS_DEV:
    UI_PORT=8081
    UI_RELOAD=False
else:
    UI_PORT=8080
    UI_RELOAD=False

SECURITY_SESSION_TIMEOUT = 60 * 60  # хвилини у секундах
SECURITY_MAX_ATTEMPTS = 5
SECURITY_LOCKOUT_DURATION_MINS = 15

# Налаштування структури папок
FOLDER_YEAR_FORMAT : Final = "%Y"         # Наприклад: 2026
FOLDER_MONTH_FORMAT : Final = "%m"        # Наприклад: 01
FOLDER_DAY_FORMAT : Final = "%d.%m.%Y"    # Наприклад: 2026.01.28
# Година, після якої дата вважається наступним днем (0-23)
DAY_ROLLOVER_HOUR : Final = 16
BACKUP_KEEP_DAYS = 30 # тримати бекапи не старіше ніж N діб

# Логірування подій
LOGGER_FILE_NAME = 'bot_log.log'
LOG_MONITORING_MAX_LINES = 1000 # tail -f

EXCEL_DATE_FORMAT : Final = "%d.%m.%Y"
UI_DATE_FORMAT : Final = "DD.MM.YYYY"

EXCEL_DATE_FORMATS_REPORT = ["%m/%d/%y", "%d.%m.%Y", "%-m/%-d/%y", "%#m/%#d/%y", "%Y-%m-%d"]
EXCEL_CHUNK_SIZE = 2000 # reading data by chunks for stability

EXCEL_LIGHT_GRAY_COLOR: Final[str] = 'EEEEEE'
EXCEL_BLUE_COLOR: Final[str] = 'bdd7ee'
EXCEL_SUPPORT_COLOR: Final[str] = 'e8fffe'

CHECK_INBOX_EVERY_SEC: Final[float] = 60.0 # перевіряти інбокс кожні ? секунд

ANTHROPIC_API_KEY: str | None = os.getenv("ANTHROPIC_API_KEY")
AI_CLAUDE_MODEL: str = os.getenv("AI_CLAUDE_MODEL", "claude-haiku-4-5-20251001")

UI_SSL_KEYFILE: str | None = os.getenv("UI_SSL_KEYFILE")
UI_SSL_CERTFILE: str | None = os.getenv("UI_SSL_CERTFILE")

# Основна функціональність
SIGNAL_BOT: Final[bool] = get_env_bool("SIGNAL_BOT", False)
DAILY_BACKUPS: Final[bool] = get_env_bool("DAILY_BACKUPS", True)
SIGNAL_WORKFLOW_STRATEGY: str = os.getenv("SIGNAL_WORKFLOW_STRATEGY", "COPY")  # COPY or FULL

if is_win():
    DOC_DIR: Final[str] = os.getenv("DOC_DIR", "C:/tmp/webtemplate/dd")
    DOCUMENT_STORAGE_PATH: Final = DOC_DIR
    BACKUP_STORAGE_PATH: Final = f"{DOC_DIR}/backups"
    INBOX_DIR_PATH: Final[str] = f"{DOC_DIR}/inbox"
    OUTBOX_DIR_PATH: Final[str] = f"{DOC_DIR}/outbox"
    INBOX_LOCAL_DIR_PATH = f"{DOC_DIR}/inbox"
    OUTBOX_LOCAL_DIR_PATH = f"{DOC_DIR}/outbox"

    SOCKET_PATH: Final = None  # Unix sockets not supported on Windows
    TCP_HOST: Final = '127.0.0.1'
    TCP_PORT: Final = 1234

    DB_NAME = os.path.join(os.path.expanduser("~/work/python/WebTemplate/signal-data"), "bot_data.db")
    MAX_QUERY_RESULTS = 50
    RECORDS_PER_PAGE = 10

    SIGNAL_ATTACHMENTS_DIR: Final = os.path.expanduser("~/AppData/Local/signal-cli/attachments/")
    TMP_DIR: Final = os.path.expanduser("~/AppData/Local/Temp/")

else:
    DOC_DIR: Final[str] = "/tmp/webtemplate/дд"
    DOCUMENT_STORAGE_PATH: Final = "/tmp/webtemplate/дд"
    BACKUP_STORAGE_PATH: Final = "/tmp/webtemplate/дд/backups"
    INBOX_DIR_PATH: Final[str] = "/tmp/webtemplate/дд/inbox"
    OUTBOX_DIR_PATH: Final[str] = "/tmp/webtemplate/дд/outbox"
    INBOX_LOCAL_DIR_PATH = f"{DOC_DIR}/inbox"
    OUTBOX_LOCAL_DIR_PATH = f"{DOC_DIR}/outbox"

    SOCKET_PATH: Final = "/tmp/signal-bot.sock"
    TCP_HOST: Final = '127.0.0.1'
    TCP_PORT: Final = 1234

    DB_NAME = os.path.join(os.path.expanduser("~/work/python/WebTemplate/signal-data"), "bot_data.db")
    MAX_QUERY_RESULTS = 50
    RECORDS_PER_PAGE = 10

    SIGNAL_ATTACHMENTS_DIR: Final = os.path.expanduser("~/.local/share/signal-cli/attachments/")
    TMP_DIR: Final = os.path.expanduser("~/tmp/")

