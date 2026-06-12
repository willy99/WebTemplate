from typing import Final

PERM_READ = 'read'
PERM_EDIT = 'write'
PERM_DELETE = 'delete'

MODULE_SEARCH:Final[str] = 'search'
MODULE_TASK:Final[str] = 'task'
MODULE_REPORT_GENERAL:Final[str] = 'report_general'
MODULE_ADMIN:Final[str] = 'admin_panel'

AVAILABLE_MODULES:Final[dict[str, str]] = {
    MODULE_SEARCH: 'Загальний доступ',
    MODULE_TASK: 'Менеджер задач',
    MODULE_REPORT_GENERAL: 'Звітність основна',
    MODULE_ADMIN: 'Адміністративна панель'
}

# Roles are managed in the DB (table: roles). AVAILABLE_ROLES is intentionally removed.

