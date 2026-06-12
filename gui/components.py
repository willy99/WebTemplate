from nicegui import app
import urllib.parse

from config import PROJECT_TITLE
from gui.services.auth_manager import AuthManager
from dics.security_config import MODULE_REPORT_GENERAL, MODULE_ADMIN, PERM_READ, PERM_EDIT

from nicegui import ui, app, run
from gui.auth_routes import logout
from datetime import datetime
import config
from i18n import t, set_language, get_language, LANGUAGES
from modules import menu_tree, render_header_widgets


class AppMenu:
    def __init__(self, auth_manager: AuthManager):
        self.auth_manager = auth_manager

    def render(self, auth_manager: AuthManager):
        dark = ui.dark_mode()
        ui.add_head_html('<link rel="stylesheet" href="/static/style.css">')
        ui.add_head_html(
            '<style>.animate-spin { animation: spin 1s linear infinite; } @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }</style>')

        ui.add_head_html('''
                <script>
                    window.isDirty = false;
                    window.addEventListener('beforeunload', function (e) {
                        if (window.isDirty) {
                            e.preventDefault();
                            e.returnValue = '';
                        }
                    });
                </script>
            ''')

        # Отримуємо дані юзера та дозволи
        user_info = app.storage.user.get('user_info', {})
        user_role = user_info.get('role', '')
        user_name = user_info.get('full_name') or user_info.get('username') or t('menu.guest')

        can_report_general = self.auth_manager.has_access(MODULE_REPORT_GENERAL, PERM_READ)
        can_report_general_edit = self.auth_manager.has_access(MODULE_REPORT_GENERAL, PERM_EDIT)
        can_admin = self.auth_manager.has_access(MODULE_ADMIN, PERM_READ)

        # 🧩 Меню з модулів-фіч (permission-filtered для поточного юзера)
        module_sections, module_top_items = menu_tree(self.auth_manager)

        # ==========================================
        # 📱 МОБІЛЬНЕ МЕНЮ (БОКОВА ПАНЕЛЬ - DRAWER)
        # ==========================================
        with ui.right_drawer(fixed=True).props('bordered').classes('bg-slate-50 p-0') as mobile_drawer:
            mobile_drawer.hide()

            with ui.row().classes('w-full bg-slate-800 p-4 items-center gap-3 m-0'):
                ui.icon('account_circle', size='md', color='white')
                with ui.column().classes('gap-0'):
                    ui.label(user_name).classes('text-white font-bold text-sm')
                    ui.label(user_role).classes('text-slate-400 text-xs')

            def make_mobile_item(title: str, icon_name: str, route: str):
                ui.button(title, icon=icon_name, on_click=lambda: ui.navigate.to(route)) \
                    .props('flat align="left"').classes('w-full no-caps text-gray-700 ml-2 font-medium')

            def make_mobile_label(title: str):
                ui.label(title).classes('text-[10px] font-bold text-gray-400 uppercase tracking-wider ml-6 mt-2 mb-1')

            with ui.column().classes('w-full gap-0 p-2'):

                # 🧩 Пункти з модулів-фіч
                for item in module_top_items:
                    make_mobile_item(t(item.label_key), item.icon, item.route)
                if module_top_items:
                    ui.separator().classes('my-1')

                for section, items in module_sections:
                    with ui.expansion(t(section.label_key), icon=section.icon).classes('w-full border-b border-gray-200').props('header-class="font-bold text-slate-800"'):
                        for item in items:
                            make_mobile_item(t(item.label_key), item.icon, item.route)

                if can_admin:
                    with ui.expansion(t('menu.admin'), icon='admin_panel_settings').classes('w-full border-b border-gray-200').props('header-class="font-bold text-yellow-600"'):
                        make_mobile_item(t('menu.permissions'), 'vpn_key', '/admin/permissions')
                        make_mobile_item(t('menu.users'), 'manage_accounts', '/admin/users')
                        make_mobile_item(t('menu.sys_config'), 'build', '/admin/settings')
                        make_mobile_item(t('menu.logs'), 'history', '/logs')
                        make_mobile_item(t('menu.audit'), 'fact_check', '/admin/audit')

                with ui.expansion(t('menu.settings'), icon='settings').classes('w-full border-b border-gray-200').props('header-class="font-bold text-slate-800"'):
                    make_mobile_item(t('menu.profile_settings'), 'manage_accounts', '/user_settings')
                    make_mobile_item(t('menu.twofa'), 'security', '/user_settings_2fa')
                    ui.button(t('menu.logout'), icon='logout', on_click=lambda: logout(self.auth_manager)) \
                        .props('flat align="left" color="negative"').classes('w-full no-caps ml-2 mt-2 font-bold')

        # ==========================================
        # 💻 ГОЛОВНИЙ HEADER
        # ==========================================
        with ui.header().classes('bg-slate-800 items-center justify-between px-2 sm:px-4'):

            # --- ЛІВА ЧАСТИНА ---
            with ui.row().classes('items-center gap-1 sm:gap-2 flex-nowrap'):
                if config.IS_DEV:
                    title = 'DEVMODE!'
                    props = 'color="red" stack'
                else:
                    title = '🏃‍♂️' + PROJECT_TITLE + ' 👨‍🚀'
                    props = 'flat'

                ui.button(title, on_click=lambda: ui.navigate.to('/')) \
                    .props(props).classes('font-bold text-md sm:text-xl text-white normal-case shrink-0')

            # --- ПРАВА ЧАСТИНА ---
            with ui.row().classes('items-center gap-1 sm:gap-2 flex-nowrap'):

                # 🧩 Віджети хедера з модулів-фіч (mail badge, task badge, etc.)
                render_header_widgets()

                # ==========================================
                # 🖥 ДЕСКТОПНЕ МЕНЮ (Використовуємо надійний клас gt-sm)
                # ==========================================
                def make_menu_item(title: str, icon_name: str, route: str):
                    with ui.menu_item(on_click=lambda: ui.navigate.to(route)):
                        with ui.row().classes('items-center gap-3 w-full'):
                            ui.icon(icon_name, size='sm').classes('text-primary')
                            ui.label(title).classes('font-medium')

                def make_menu_label(title: str):
                    ui.separator().classes('my-1')
                    with ui.menu_item().props('disabled').classes('q-py-none'):
                        ui.label(title).classes('text-xs font-bold text-gray-500 uppercase tracking-wider ml-1')

                # Замість 'hidden lg:flex' використовуємо 'gt-sm' (видимо тільки на планшетах і ПК)
                with ui.row().classes('gt-sm items-center gap-1'):

                    # 🧩 Пункти з модулів-фіч
                    for item in module_top_items:
                        ui.button(t(item.label_key), icon=item.icon,
                                  on_click=lambda r=item.route: ui.navigate.to(r)) \
                            .props('flat text-white no-caps')

                    for section, items in module_sections:
                        with ui.button(t(section.label_key), icon=section.icon).props('flat text-white icon-right="expand_more"'):
                            with ui.menu():
                                for item in items:
                                    make_menu_item(t(item.label_key), item.icon, item.route)

                    if can_admin:
                        with ui.button(t('menu.admin'), icon='admin_panel_settings').props('flat text-yellow-400 font-bold icon-right="expand_more"'):
                            with ui.menu():
                                make_menu_item(t('menu.permissions'), 'vpn_key', '/admin/permissions')
                                make_menu_item(t('menu.users'), 'manage_accounts', '/admin/users')
                                make_menu_item(t('menu.sys_config'), 'build', '/admin/settings')
                                make_menu_item(t('menu.logs'), 'history', '/logs')
                                make_menu_item(t('menu.audit'), 'fact_check', '/admin/audit')

                    ui.separator().props('vertical dark').classes('mx-2 h-8')

                    with ui.button(icon='account_circle').props('flat text-white no-caps icon-right="expand_more"').classes('mr-2') as profile_btn:
                        ui.label(user_name).classes('ml-2 font-medium')
                        with ui.menu().classes('w-64'):
                            with ui.menu_item(on_click=lambda: ui.navigate.to('/user_settings')):
                                with ui.row().classes('items-center gap-3'):
                                    ui.icon('manage_accounts', color='primary')
                                    ui.label(t('menu.profile_settings'))
                            with ui.menu_item(on_click=lambda: ui.navigate.to('/user_settings_2fa')):
                                with ui.row().classes('items-center gap-3'):
                                    ui.icon('security', color='warning')
                                    ui.label(t('menu.twofa_full'))
                            ui.separator()
                            with ui.menu_item(on_click=lambda: logout(self.auth_manager)):
                                with ui.row().classes('items-center gap-3'):
                                    ui.icon('logout', color='negative')
                                    ui.label(t('menu.logout'))
                            make_menu_item(t('menu.developer'), 'info', '/pages/about')

                # ==========================================
                # 🌐 ПЕРЕМИКАЧ МОВИ
                # ==========================================
                def switch_language(code: str):
                    set_language(code)
                    ui.navigate.reload()

                current_lang = get_language()
                with ui.button(icon='language').props('flat round color="white"').tooltip(t('menu.language')):
                    with ui.menu():
                        for code, label in LANGUAGES.items():
                            with ui.menu_item(on_click=lambda c=code: switch_language(c)):
                                with ui.row().classes('items-center gap-2'):
                                    ui.label(label).classes('font-medium' if code == current_lang else '')
                                    if code == current_lang:
                                        ui.icon('check', size='xs', color='primary')

                # ==========================================
                # 🍔 КНОПКА ГАМБУРГЕР (Використовуємо надійний клас lt-md)
                # ==========================================
                # Замість 'lg:hidden' використовуємо 'lt-md' (видимо тільки на мобільних)
                ui.button(icon='menu', on_click=mobile_drawer.toggle).props('flat round color="white"').classes('lt-md ml-1')

        # inject_watermark()


def inject_watermark():
    user_info = app.storage.user.get('user_info', {})
    user_name = user_info.get('full_name') or user_info.get('username') or 'Невідомий користувач'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    watermark_text = f"{user_name} | {current_time}"

    svg = f"""
    <svg xmlns='http://www.w3.org/2000/svg' width='350' height='200'>
        <text x='50%' y='50%' 
              dominant-baseline='middle' text-anchor='middle' 
              transform='rotate(-30, 175, 100)' 
              fill='rgba(225, 225, 225, 0.15)' 
              font-size='16' font-family='sans-serif' font-weight='bold'>
            {watermark_text}
        </text>
    </svg>
    """
    encoded_svg = urllib.parse.quote(svg)
    ui.add_head_html(f'''
        <style>
            .security-watermark {{
                position: fixed;
                top: 0; left: 0; width: 150vw; height: 150vh;
                pointer-events: none;
                z-index: 9999;
                background-image: url("data:image/svg+xml;utf8,{encoded_svg}");
                background-repeat: repeat;
            }}
        </style>
    ''')
    ui.element('div').classes('security-watermark')