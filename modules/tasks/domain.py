"""Domain models and constants of the Tasks module. Module-private."""
from pydantic import BaseModel, Field
from typing import Optional, Final, Dict, List
from datetime import datetime

TASK_STATUS_NEW: Final[str] = 'NEW'
TASK_STATUS_IN_PROGRESS: Final[str] = 'IN_PROGRESS'
TASK_STATUS_COMPLETED: Final[str] = 'COMPLETED'
TASK_STATUS_CANCELED: Final[str] = 'CANCELED'

# Тип задачі -> material icon
TASK_TYPES: Final[Dict[str, str]] = {
    'Документація': 'description',
    'Запити': 'contact_support',
    'Фікс Даних': 'bug_report',
    'Програмірувай': 'flutter_dash',
    'Звіти': 'menu_book'
}


class Subtask(BaseModel):
    title: str
    is_done: bool = False
    id: Optional[int] = None
    task_id: Optional[int] = None


class Task(BaseModel):
    id: Optional[int] = None
    task_subject: str
    task_details: Optional[str] = ''
    task_type: Optional[str] = 'Інше'
    assignee: Optional[int] = None
    task_status: str = TASK_STATUS_NEW
    task_deadline: Optional[datetime] = None
    created_by: Optional[int] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None
    subtasks: List[Subtask] = Field(default_factory=list)
