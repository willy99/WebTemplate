"""
🧩 Tasks & Calendar feature module — the reference vertical slice.

Everything task-related lives inside this package:

    modules/tasks/
    ├── __init__.py   ← this manifest (pages, menu, permission, header badge)
    ├── i18n.py       ← uk/en translations
    ├── domain.py     ← Task, Subtask models + statuses + types
    ├── service.py    ← TaskService (business logic / SQL)
    ├── controller.py ← TaskController
    └── views/        ← task board, task editor, calendar

The core (navigation.py / components.py) knows nothing about it.
"""
from nicegui import ui, app, run

from dics.security_config import MODULE_TASK, PERM_READ, PERM_EDIT
from gui.auth_routes import require_access
from gui.services.auth_manager import AuthManager
from i18n import t
from modules.base import AppModule, MenuItem, MenuSection, ModuleContext
from modules.tasks.controller import TaskController
from modules.tasks.i18n import TRANSLATIONS
from modules.tasks.views import task_list_view, task_edit_view, calendar_view
import config


class TasksModule(AppModule):
    id = 'tasks'
    permission_module = MODULE_TASK
    permission_label = 'Менеджер задач'
    menu_section = MenuSection(id='plans', label_key='menu.plans', icon='follow_the_signs', order=10)
    translations = TRANSLATIONS

    def __init__(self):
        self._ctrl: TaskController | None = None

    def menu_items(self) -> list[MenuItem]:
        return [
            MenuItem('menu.my_tasks', 'person_pin', '/tasks/today', order=10),
            MenuItem('menu.all_tasks', 'assignment', '/tasks/all', order=20),
            MenuItem('menu.calendar', 'calendar_month', '/calendar', order=30),
        ]

    def register_pages(self, ctx: ModuleContext) -> None:
        auth_manager: AuthManager = ctx.auth_manager
        app_menu = ctx.app_menu
        self._ctrl = task_ctrl = TaskController(ctx.workflow, auth_manager)

        @ui.page('/tasks')
        @require_access(auth_manager, MODULE_TASK, PERM_READ)
        def task_list():
            app_menu.render(auth_manager)
            task_list_view.render_task_list_page(task_ctrl, auth_manager)

        @ui.page('/tasks/today')
        @require_access(auth_manager, MODULE_TASK, PERM_READ)
        def task_list_today():
            app_menu.render(auth_manager)
            task_list_view.render_tasks_today(task_ctrl, auth_manager)

        @ui.page('/tasks/all')
        @require_access(auth_manager, MODULE_TASK, PERM_READ)
        def task_list_all():
            app_menu.render(auth_manager)
            task_list_view.render_tasks_all(task_ctrl, auth_manager)

        @ui.page('/tasks/edit/{task_id}')
        @require_access(auth_manager, MODULE_TASK, PERM_EDIT)
        def edit_task_page(task_id: str = 'new'):
            actual_id = None if task_id == 'new' else int(task_id)
            app_menu.render(auth_manager)
            task_edit_view.render_task_edit_page(task_ctrl, auth_manager, actual_id)

        @ui.page('/calendar')
        @require_access(auth_manager, MODULE_TASK, PERM_READ)
        def calendar_general():
            ctx_user = auth_manager.get_current_context()
            app_menu.render(auth_manager)
            calendar_view.render_calendar_page(task_ctrl, ctx_user)

    def header_widgets(self, ctx: ModuleContext) -> None:
        """Бейдж задач у хедері: лічильники нових/в роботі + будильник дедлайнів."""
        auth_manager: AuthManager = ctx.auth_manager
        task_ctrl = self._ctrl
        if task_ctrl is None:
            return

        if not hasattr(app, 'alarmed_tasks'):
            app.alarmed_tasks = set()

        with ui.button(icon='assignment', on_click=lambda: ui.navigate.to('/tasks/today')).props('flat color=white'):
            badge_new = ui.badge(color='red').props('floating rounded').classes('text-[10px] font-bold')
            badge_new.set_visibility(False)
            badge_prog = ui.badge(color='orange-8').props('floating rounded').classes('text-[10px] font-bold').style('top: auto; bottom: -4px;')
            badge_prog.set_visibility(False)

            with ui.tooltip().classes('bg-gray-800 text-white text-sm'):
                with ui.column().classes('gap-0'):
                    lbl_new = ui.label(t('tasks.badge_new', n=0))
                    lbl_prog = ui.label(t('tasks.badge_in_progress', n=0))

            async def update_my_tasks():
                try:
                    if not app.storage.user.get('authenticated') or not auth_manager.get_current_context():
                        return
                    counts = await run.io_bound(task_ctrl.get_my_task_counts, auth_manager.get_current_context())
                    if not counts:
                        return
                    new_count, prog_count = counts

                    badge_new.set_text(str(new_count))
                    badge_new.set_visibility(new_count > 0)
                    badge_prog.set_text(str(prog_count))
                    badge_prog.set_visibility(prog_count > 0)
                    lbl_new.set_text(t('tasks.badge_new', n=new_count))
                    lbl_prog.set_text(t('tasks.badge_in_progress', n=prog_count))

                    alarms = await run.io_bound(task_ctrl.get_my_alarms, auth_manager.get_current_context())
                    for alarm in alarms:
                        task_id = alarm['id']
                        if task_id not in app.alarmed_tasks:
                            app.alarmed_tasks.add(task_id)
                            ui.notify(t('tasks.overdue_notify', subject=alarm['subject']), type='negative', position='top', timeout=0, multi_line=True,
                                      close_button=t('tasks.acknowledge'))
                            ui.run_javascript("new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg').play().catch(e => console.log('Audio blocked'));")
                except Exception:
                    pass

            ui.timer(config.CHECK_INBOX_EVERY_SEC, update_my_tasks)
            ui.timer(0.1, update_my_tasks, once=True)


MODULE = TasksModule()
