# 🧩 Feature Modules

A feature module is a **fully isolated vertical slice**: domain models, business
logic, controller, views, pages, menu entries, permissions, header widgets and
translations — all in **one package**. The core (`gui/navigation.py`,
`gui/components.py`, core `i18n/`) is never touched when adding a feature.

**Dependency rule:** modules import from core (shared infrastructure), core
never imports from `modules/`.

## Reference example: `modules/tasks/`

```
modules/tasks/
├── __init__.py    # MANIFEST: pages, menu, permission, header badge
├── i18n.py        # uk/en translations of the module
├── domain.py      # Task, Subtask (pydantic) + statuses + task types
├── service.py     # TaskService — business logic / SQL
├── controller.py  # TaskController — glue between views and service
└── views/
    ├── task_list_view.py   # kanban board
    ├── task_edit_view.py   # task editor
    └── calendar_view.py    # calendar
```

## How it works

At startup `navigation.init_nicegui()` calls `modules.register_all(ctx)`, which
for every package under `modules/` exposing a `MODULE` manifest:

1. **Merges translations** (`mod.translations`) into the i18n dictionaries
2. **Registers the permission entry** (`mod.permission_module` + label) into `AVAILABLE_MODULES`
3. **Registers pages** via `mod.register_pages(ctx)`

At render time `AppMenu`:
- builds the menu from `modules.menu_tree(auth_manager)` — permission-filtered per user, desktop + mobile
- renders header widgets via `modules.render_header_widgets()` — e.g. the tasks
  badge with new/in-progress counters and the deadline alarm

## Adding a new feature

Copy the layout of `modules/tasks/` (or `modules/chat/` for a minimal one):

```python
# modules/reports/__init__.py
from nicegui import ui
from dics.security_config import PERM_READ
from gui.auth_routes import require_access
from modules.base import AppModule, MenuItem, MenuSection, ModuleContext

MODULE_REPORTS = 'reports'

class ReportsModule(AppModule):
    id = 'reports'
    permission_module = MODULE_REPORTS
    permission_label = 'Звітність'
    menu_section = MenuSection(id='reports', label_key='menu.reports', icon='bar_chart', order=20)
    translations = {
        'uk': {'menu.reports': 'Звіти', 'menu.monthly': 'Місячний звіт'},
        'en': {'menu.reports': 'Reports', 'menu.monthly': 'Monthly report'},
    }

    def menu_items(self):
        return [MenuItem('menu.monthly', 'calendar_month', '/reports/monthly', order=10)]

    def register_pages(self, ctx: ModuleContext):
        @ui.page('/reports/monthly')
        @require_access(ctx.auth_manager, MODULE_REPORTS, PERM_READ)
        def monthly():
            ctx.app_menu.render(ctx.auth_manager)
            ui.label('Monthly report')

MODULE = ReportsModule()
```

Restart the app — route, menu entry (translated), permission row in
**Admin → Roles & permissions** all appear automatically. Grant the new
permission to the roles that need it.

To remove a feature: delete the folder. Done.

## Manifest reference (`modules/base.py`)

| Member | Meaning |
|---|---|
| `id` | unique module id (used in startup log) |
| `permission_module` | security module for `require_access` / menu filtering |
| `permission_label` | label merged into `AVAILABLE_MODULES`; empty = reuse a core permission |
| `menu_section` | `MenuSection(...)` for a dropdown, or `None` for top-level buttons |
| `translations` | `{'uk': {...}, 'en': {...}}` merged into i18n at startup; convention: keep in `i18n.py` |
| `menu_items()` | list of `MenuItem(label_key, icon, route, order)` |
| `register_pages(ctx)` | register `@ui.page` routes; create your controller here |
| `header_widgets(ctx)` | optional: render badges/buttons into the app header (see tasks badge) |

`ModuleContext` gives you `workflow` (db, services, log_manager),
`auth_manager` (sessions, permissions, users) and `app_menu`
(call `app_menu.render(auth_manager)` at the top of each page).

## What stays in core

- DB schema (`schema.sql` / `update.sql`) and table-name constants — the DB is shared infrastructure
- `gui/tools/ui_components.py` (date inputs, confirm dialog, `ServerPagination`) — shared UI toolkit
- Auth, users, roles, permissions, audit — platform services every module relies on

## Current modules

- **tasks** — full vertical slice: kanban board, editor, calendar, header badge (`MODULE_TASK`)
- **chat** — minimal example: one view + own translations (`MODULE_SEARCH`)
