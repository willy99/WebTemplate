from nicegui import ui, app
from fastapi.responses import JSONResponse

from dics.security_config import PERM_READ, PERM_EDIT, MODULE_SEARCH, MODULE_ADMIN
from gui.components import AppMenu
from gui.controllers.audit_controller import AuditController
from gui.controllers.admin_audit_controller import AdminAuditController
from gui.controllers.config_controller import ConfigController
from gui.controllers.user_controller import UserController
from gui.views.pages.cv import render_cv_page
from gui.views.pages import about
from gui.views.home_view import render_home_page
from gui.views.report.logs_view import render_logs_page
from gui.views.admin.admin_permissions_view import render_permissions_page
from gui.views.admin.admin_users_view import render_users_page
from gui.views.admin.admin_settings_view import render_settings_page
from gui.views.admin.user_setting_form import render_user_settings_2fa, render_profile_settings
from gui.views.admin.audit_log_view import render_audit_logs
from gui.auth_routes import create_login_page, require_access
from pathlib import Path
from service.processing.processors.DocTemplator import DocTemplator
from gui.services.auth_manager import AuthManager
from modules import register_all
from modules.base import ModuleContext
import os
import config

def init_nicegui(workflow_obj):

    current_dir = Path(__file__).parent.absolute()
    static_dir = current_dir / 'static'
    templates_form = current_dir / '../resources/templates'

    app.add_static_files('/static', str(static_dir))
    # app.add_static_files('/templates', str(templates_form))
    templates_dir = current_dir / '../resources/templates'
    doc_templator = DocTemplator(templates_dir)
    auth_manager = AuthManager(workflow_obj)

    config_ctrl = ConfigController(workflow_obj, auth_manager)
    user_ctrl = UserController(workflow_obj, auth_manager)
    admin_audit_ctrl = AdminAuditController(workflow_obj, auth_manager)
    audit_ctrl = AuditController(workflow_obj, auth_manager)

    app_menu = AppMenu(auth_manager)

    create_login_page(auth_manager, user_ctrl, workflow_obj.log_manager)

    @ui.page('/')
    @ui.page('/home')
    @require_access(auth_manager, MODULE_SEARCH, PERM_READ)
    def index():
        render_home_page(auth_manager)

    # 🧩 Feature modules (tasks, calendar, chat, ...) register their own pages,
    # menu entries, permissions and translations. See modules/README.md.
    register_all(ModuleContext(
        workflow=workflow_obj,
        auth_manager=auth_manager,
        app_menu=app_menu,
    ))

    # Доступ ТІЛЬКИ для адмінів!

    @ui.page('/admin/settings')
    @require_access(auth_manager, MODULE_ADMIN, PERM_EDIT)
    def settings_doc():
        app_menu.render(auth_manager)
        render_settings_page(config_ctrl, auth_manager)

    @ui.page('/logs')
    @require_access(auth_manager, MODULE_ADMIN, PERM_READ)
    def system_logs():
        app_menu.render(auth_manager)
        log_dir = "logs"
        log_file = os.path.join(log_dir, config.LOGGER_FILE_NAME)
        render_logs_page(log_file)

    @ui.page('/admin/permissions')
    @require_access(auth_manager, MODULE_ADMIN, PERM_EDIT)
    def admin_permissions_route():
        app_menu.render(auth_manager)
        render_permissions_page(auth_manager)

    @ui.page('/admin/users')
    @require_access(auth_manager, MODULE_ADMIN, PERM_EDIT)  # Доступ ТІЛЬКИ для адмінів!
    def admin_users_route():
        app_menu.render(auth_manager)
        render_users_page(auth_manager)

    @ui.page('/admin/audit')
    @require_access(auth_manager, MODULE_ADMIN, PERM_EDIT)
    async def admin_audit():
        app_menu.render(auth_manager)
        render_audit_logs(admin_audit_ctrl, auth_manager)

    @ui.page('/user_settings_2fa')
    @require_access(auth_manager,MODULE_SEARCH, PERM_READ)
    async def user_settings_2fa():
        app_menu.render(auth_manager)
        render_user_settings_2fa(user_ctrl, auth_manager)

    @ui.page('/user_settings')
    @require_access(auth_manager,MODULE_SEARCH, PERM_READ)
    async def user_settings():
        app_menu.render(auth_manager)
        render_profile_settings(user_ctrl, auth_manager)

    @ui.page('/pages/about')
    @require_access(auth_manager, MODULE_SEARCH, PERM_READ)
    async def pages_about():
        app_menu.render(auth_manager)
        await about.about_page()

    @ui.page('/pages/cv')
    async def pages_cv():
        await render_cv_page()

    @app.get('/health')
    def health_check():
        return JSONResponse({'status': 'ok', 'title': config.PROJECT_TITLE})

    @ui.page('/download/template/{template_path:path}')
    @require_access(auth_manager, MODULE_SEARCH, PERM_READ)
    def download_template(template_path: str):
        """Захищене завантаження шаблонів Word."""
        try:
            safe_filename = os.path.basename(template_path)

            full_path = templates_form / template_path  # Якщо довіряємо структурі підпапок

            if not str(Path(full_path).resolve()).startswith(str(templates_form.resolve())):
                ui.notify('Спроба несанкціонованого доступу до файлової системи!', type='negative')
                return

            if full_path.exists() and full_path.is_file():
                ui.download(full_path, safe_filename)
            else:
                ui.notify('Шаблон не знайдено', type='warning')

        except Exception as e:
            ui.notify(f'Помилка завантаження: {e}', type='negative')

    # native=False дозволяє працювати як веб-сервер
    # reload=False обов'язково, бо ми в потоці
    ui.run(
        host='127.0.0.1',
        port=config.UI_PORT,
        proxy_headers=True,
        forwarded_allow_ips='127.0.0.1',
        title=config.PROJECT_TITLE,
        reload=config.UI_RELOAD,
        show=False,
        storage_secret=config.UI_SECRET_KEY,
        ssl_keyfile=config.UI_SSL_KEYFILE or None,
        ssl_certfile=config.UI_SSL_CERTFILE or None,
    )
