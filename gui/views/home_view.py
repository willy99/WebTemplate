from nicegui import ui

from dics.security_config import PERM_READ, PERM_EDIT, MODULE_SEARCH, MODULE_TASK, \
    MODULE_REPORT_GENERAL, MODULE_ADMIN
from gui.auth_routes import logout
from gui.services.auth_manager import AuthManager
from utils.utils import get_build_info


def create_nav_card(title: str, description: str, icon_name: str, route: str, color: str = 'blue'):
    """Компактна квадратна картка з адаптивним розміром"""
    with ui.card().classes(
            # Замінили стрибок вгору на плавний зум (scale-105), бо картки тепер під меню
            f'cursor-pointer hover:scale-105 hover:shadow-xl transition-all duration-300 '
            f'border-t-4 border-{color}-500 w-28 h-24 sm:w-44 sm:h-32 p-2 sm:p-3 '
            f'flex flex-col items-center justify-center text-center gap-1 '
            f'bg-white/95 backdrop-blur-md shadow-lg rounded-xl sm:rounded-2xl') \
            .on('click', lambda: ui.navigate.to(route)):
        ui.icon(icon_name, size='1.8rem', color=color).classes('mb-0 sm:mb-1')
        ui.label(title).classes('text-[11px] sm:text-sm font-bold text-gray-800 leading-tight')
        ui.label(description).classes('hidden sm:block text-[10px] text-gray-500 leading-snug')


def render_home_page(auth_manager: AuthManager):
    can_search = auth_manager.has_access(MODULE_SEARCH, PERM_READ)
    if not can_search:
        logout(auth_manager)

    build_info = get_build_info()
    bg_style = 'background-image: url("/static/images/bg_home.jpg"); background-size: cover; background-position: center; background-attachment: fixed;'

    has_search = auth_manager.has_access(MODULE_SEARCH, PERM_READ)
    has_tasks = auth_manager.has_access(MODULE_TASK, PERM_READ)
    has_admin = auth_manager.has_access(MODULE_ADMIN, PERM_READ)

    # Повертаємо класичний min-h-screen без fixed-костилів
    with ui.element('div').classes('w-full min-h-screen flex flex-col relative').style(bg_style):
        ui.element('div').classes('absolute inset-0 bg-white/60 z-0')

        # --- ВІДЖЕТ ВЕРСІЇ (Фіксовано в правому нижньому куті) ---
        with ui.element('div').classes(
                'fixed bottom-4 right-4 sm:bottom-6 sm:right-6 bg-white/80 backdrop-blur-md px-3 sm:px-5 py-1 sm:py-2 rounded-full flex items-center gap-2 sm:gap-3 shadow-md z-20 border border-white/50 hover:bg-white transition-colors duration-300'):
            ui.icon('pets', size='1.2rem', color='slate').classes('hidden sm:block')
            ui.html(f'''
                <div class="flex items-center gap-2 sm:gap-3">
                    <span class="hidden sm:inline text-gray-500 text-xs font-medium">
                        2026 (С) <a href="mailto:willy2005@gmail.com" class="text-blue-500 hover:text-blue-700 transition-colors" style="text-decoration: none;">Pashkinson</a>
                    </span>
                    <span class="text-gray-400 font-mono text-[9px] sm:text-[10px] bg-gray-100 px-2 py-1 rounded border border-gray-200">
                        {build_info}
                    </span>
                </div>
            ''')

        # Головний контейнер з подією mouseleave для закриття карток
        with ui.column().classes('w-full items-center px-2 sm:px-4 py-4 sm:py-8 relative z-10').on('mouseleave', lambda: set_tab(None)):

            # Підготовка логіки перемикання вкладок
            cat_containers = {}

            def set_tab(tab_name):
                for key, container in cat_containers.items():
                    container.set_visibility(key == tab_name)

            # --- КРОК 2: МЕНЮШКА (ОДРАЗУ ПІД ЦИФРАМИ) ---
            with ui.row().classes(
                    'px-3 py-2 sm:px-5 sm:py-3 bg-white/40 backdrop-blur-xl border border-white/60 rounded-[1.5rem] sm:rounded-[2rem] shadow-lg gap-2 sm:gap-3 items-center flex-wrap justify-center mx-2 mb-4 sm:mb-6 z-50'):

                def dock_icon(name, icon, tab_id):
                    # Прибрали -translate-y-4, залишили scale для плавності
                    with ui.column().classes(
                            'group items-center justify-center w-12 h-12 sm:w-16 sm:h-16 rounded-xl sm:rounded-2xl hover:bg-white/70 cursor-pointer transition-all duration-300 hover:scale-105 sm:hover:scale-110 hover:shadow-md bg-white/30 border border-white/50 shadow-sm') \
                            .on('mouseenter', lambda: set_tab(tab_id)) \
                            .on('click', lambda: set_tab(tab_id)):
                        ui.icon(icon, size='1.5rem').classes('text-slate-700 transition-transform duration-300 group-hover:scale-110 group-hover:text-blue-600')
                        ui.label(name).classes('hidden sm:block text-[10px] font-bold text-slate-700 tracking-tight mt-1 opacity-70 group-hover:opacity-100 transition-opacity')

                if has_search: dock_icon('Пошук', 'search', 'search')
                if has_tasks: dock_icon('Задачі', 'task_alt', 'tasks')
                if has_admin: dock_icon('Адмінка', 'admin_panel_settings', 'admin')
                dock_icon('Профіль', 'account_circle', 'profile')

            # --- КРОК 3: КАРТКИ (З'ЯВЛЯЮТЬСЯ ЗНИЗУ) ---
            cards_display = ui.element('div').classes('min-h-[180px] sm:min-h-[144px] w-full max-w-6xl flex justify-center items-start px-2')

            with cards_display:
                row_classes = 'gap-2 sm:gap-4 justify-center items-start flex-wrap'

                if has_tasks:
                    with ui.row().classes(row_classes) as c_tasks:
                        create_nav_card('Мої задачі', 'Поточні доручення', 'person_pin', '/tasks/today', 'yellow')
                        create_nav_card('Inbox/Outbox', 'Сходити на пошту', 'email', '/inbox', 'yellow')
                        create_nav_card('Календар', 'Графік дедлайнів', 'calendar_month', '/calendar', 'yellow')
                    cat_containers['tasks'] = c_tasks
                    c_tasks.set_visibility(False)

                if has_admin:
                    with ui.row().classes(row_classes) as c_admin:
                        create_nav_card('Системні логи', 'Моніторинг', 'terminal', '/logs', 'slate')
                        create_nav_card('Журнал подій', 'Журнал подій', 'fact_check', '/admin/audit', 'slate')
                        create_nav_card('Користувачі', 'Акаунти', 'manage_accounts', '/admin/users', 'slate')
                        create_nav_card('Права доступу', 'Доступи та ролі', 'vpn_key', '/admin/permissions', 'slate')
                        create_nav_card('Налаштування', 'Конфігурація', 'settings', '/admin/settings', 'slate')
                    cat_containers['admin'] = c_admin
                    c_admin.set_visibility(False)

                with ui.row().classes(row_classes) as c_profile:
                    create_nav_card('Профіль', 'Налаштування профілю', 'manage_accounts', '/user_settings', 'orange')
                    create_nav_card('2fa', 'Двофакторка', 'security', '/user_settings_2fa', 'orange')
                    create_nav_card('Розробник', 'Розробник', 'child_care', '/pages/about', 'orange')
                    cat_containers['profile'] = c_profile
                    c_profile.set_visibility(False)
