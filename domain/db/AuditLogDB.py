from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Any, Dict
from enum import Enum

class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class EventDomain(str, Enum):
    AUTH = "AUTH"
    PERSON = "PERSON"
    REPORT = "REPORT"
    DOCUMENTS = "DOCUMENTS"
    FILE = "FILE"
    SYSTEM = "SYSTEM"


class EventType(str, Enum):
    LOGIN_ATTEMPT = "LOGIN_ATTEMPT"
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    SEARCH = "SEARCH"
    GET = "GET"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    EXPORT = "EXPORT"
    PARSE_ERROR = "PARSE_ERROR"

# --- 2. Pydantic Модель Журналу ---

class AuditLogDB(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = Field(None, description="Унікальний ID запису в базі")

    # Час події (за замовчуванням береться поточний час)
    created_at: datetime = Field(default_factory=datetime.now, alias="timestamp")

    # Категоризація
    level: LogLevel = Field(default=LogLevel.INFO)
    domain: EventDomain = Field(...)
    event_type: EventType = Field(...)

    # Хто і звідки (можуть бути None, якщо це системна подія без юзера)
    username: Optional[str] = Field(None, description="Логін або ПІБ користувача (напр. Пашкінсон)")
    ip_address: Optional[str] = Field(None, description="IP адреса (напр. 192.168.110.53)")

    # Що змінилося
    entity_id: Optional[int] = Field(None, description="ID зміненого запису (наприклад, ID персони)")

    # Текстові або структуровані деталі
    action_summary: str = Field(..., description="Короткий опис (напр. 'Генеруємо щосуботній звіт')")

    # Сюди можна писати словник, який потім в БД збережеться як JSON-рядок
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Додаткові дані: параметри пошуку, старі/нові значення тощо"
    )