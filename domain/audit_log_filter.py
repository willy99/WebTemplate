from dataclasses import dataclass
from typing import Optional, Final, List
import config

YES: Final[str] = 'Yes'
NO: Final[str] = 'No'

@dataclass
class AuditLogFilter:
    username: Optional[str] = None
    domain: Optional[str] = None
    event_type: Optional[str] = None
    level: Optional[str] = None
    date_from: Optional[str] = None
    date_to: Optional[str] = None
    entity_id: Optional[int] = None
    text: Optional[str] = None
    limit: int = config.RECORDS_PER_PAGE
    offset: int = 0