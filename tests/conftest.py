import os
import pytest
from unittest.mock import MagicMock

from gui.services.request_context import RequestContext
from service.connection.MyDataBase import MyDataBase
from service.constants import DB_TABLE_TASK
from service.storage.LoggerManager import LoggerManager
import time


# Шлях до вашого порожнього шаблону
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "fixtures", "template.xlsx")

@pytest.fixture
def mock_logger():
    logger_manager = MagicMock(spec=LoggerManager)
    logger = MagicMock()

    # Функція, яка буде імітувати запис у консоль
    def print_to_console(msg, *args, **kwargs):
        # Додаємо колір або префікс, щоб бачити, що це саме з логера
        print(f"\n[LOG-DEBUG] {msg}")

    # Прив'язуємо функцію до методу debug (можна і до info/error)
    logger.debug.side_effect = print_to_console
    logger.info.side_effect = print_to_console
    logger.error.side_effect = print_to_console

    logger_manager.get_logger.return_value = logger
    return logger_manager

@pytest.fixture
def mock_db():
    """Створює тимчасову БД в пам'яті на основі реального schema.sql"""
    db = MyDataBase(":memory:")

    # Визначаємо шлях до schema.sql (корегуйте шлях під вашу структуру папок)
    # Припустимо, schema.sql лежить у папці service/connection/
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Піднімаємось на потрібний рівень, якщо conftest.py лежить у папці tests/
    project_root = os.path.dirname(current_dir)
    schema_path = os.path.join(project_root, 'service', 'connection', 'schema.sql')

    # Читаємо та виконуємо схему
    with open(schema_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    # Використовуємо внутрішній метод вашого MyDataBase або прямий доступ до sqlite
    # Якщо MyDataBase має доступ до курсору, можна так:
    with db._connect() as conn:  # припускаю наявність такого методу
        conn.executescript(sql_script)

    update_path = os.path.join(project_root, 'service', 'connection', 'update.sql')
    if os.path.exists(update_path):
        with open(update_path, 'r', encoding='utf-8') as f:
            db._connect().executescript(f.read())

    # Додаємо тестового користувача, щоб працювали JOIN-и
    db.insert_record("users", {"id": 1, "username": "test_user", "password_hash":"asdklfjasdlfkajsdlnskjdfksjadlkfjlaksjdf", "role":"admin"})
    yield db

    try:
        db.__execute_sql__("DELETE FROM " + DB_TABLE_TASK)
        db.__execute_sql__("DELETE FROM users")
    except Exception:
        pass
    print("\n🧹 Тестова база очищена")


@pytest.fixture
def mock_ctx():
    """Імітація контексту запиту користувача"""
    ctx = RequestContext(user_login="test_user", user_id=1, user_name="test", user_role="Admin", last_activity=time.time())
    return ctx