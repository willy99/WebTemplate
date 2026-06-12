"""
🧩 Inbox feature module.

Owns: InboxService, InboxController, inbox triage view, mail badge in header.
Permission reuses MODULE_TASK (existing DB grant — no migration needed).
"""
from nicegui import ui, app, run

from dics.security_config import MODULE_TASK, PERM_READ
from gui.auth_routes import require_access
from gui.controllers.audit_controller import AuditController
from modules.base import AppModule, MenuItem, ModuleContext
from modules.inbox.i18n import TRANSLATIONS
from modules.inbox.controller import InboxController
from modules.inbox.views.inbox_triage_view import render_inbox_page
import config


class InboxModule(AppModule):
    id = 'inbox'
    permission_module = MODULE_TASK   # reuses the existing task-module grant
    permission_label = ''             # no new permission row in admin
    menu_section = None               # top-level button

    translations = TRANSLATIONS

    def menu_items(self) -> list[MenuItem]:
        return [MenuItem('menu.inbox', 'mail', '/inbox', order=1)]

    def register_pages(self, ctx: ModuleContext) -> None:
        self._ctrl = InboxController(ctx.workflow, ctx.auth_manager)
        self._audit_ctrl = AuditController(ctx.workflow, ctx.auth_manager)
        auth_manager = ctx.auth_manager
        app_menu = ctx.app_menu

        @ui.page('/inbox')
        @require_access(auth_manager, MODULE_TASK, PERM_READ)
        def inbox_page():
            app_menu.render(auth_manager)
            render_inbox_page(self._ctrl, self._audit_ctrl, auth_manager)

    def header_widgets(self, ctx: ModuleContext) -> None:
        """Mail badge: personal-inbox count (red, top) + shared-inbox count (grey, bottom)."""
        auth_manager = ctx.auth_manager

        with ui.button(icon='mail', on_click=lambda: ui.navigate.to('/inbox')).props('flat round color="white"'):
            badge_personal = ui.badge(color='red').props('floating rounded').classes('text-[10px] font-bold')
            badge_personal.set_visibility(False)
            badge_root = (
                ui.badge(color='grey-5')
                .props('floating rounded')
                .classes('text-[10px] font-bold text-gray-800')
                .style('top: auto; bottom: -4px;')
            )
            badge_root.set_visibility(False)

            async def update_inbox():
                try:
                    if not app.storage.user.get('authenticated'):
                        return
                    inbox_data = await run.io_bound(
                        self._ctrl.get_user_inbox_messages,
                        auth_manager.get_current_context(),
                    )
                    if not inbox_data:
                        return
                    p_count = len(inbox_data['personal_files'])
                    r_count = len(inbox_data['root_files'])
                    badge_personal.set_text(str(p_count))
                    badge_personal.set_visibility(p_count > 0)
                    badge_root.set_text(str(r_count))
                    badge_root.set_visibility(r_count > 0)
                except Exception:
                    pass

            ui.timer(config.CHECK_INBOX_EVERY_SEC, update_inbox)
            ui.timer(0.1, update_inbox, once=True)


MODULE = InboxModule()
