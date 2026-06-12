"""
🧩 AI Chat feature module.

Demonstrates a module that ships its own translations and renders as a
top-level menu button (menu_section = None).
"""
from nicegui import ui

from dics.security_config import MODULE_SEARCH, PERM_READ
from gui.auth_routes import require_access
from modules.base import AppModule, MenuItem, ModuleContext
from modules.chat.view import render_chat_page


class ChatModule(AppModule):
    id = 'chat'
    permission_module = MODULE_SEARCH   # reuses the core "general access" permission
    permission_label = ''               # core module — no new permission entry
    menu_section = None                 # top-level button, not a dropdown

    translations = {
        'uk': {
            'menu.chat': 'Chat',
            'chat.title': 'AI Chat',
            'chat.placeholder': 'Напишіть повідомлення… (Enter — надіслати)',
            'chat.error': '**Помилка:** {error}',
        },
        'en': {
            'menu.chat': 'Chat',
            'chat.title': 'AI Chat',
            'chat.placeholder': 'Type a message… (Enter to send)',
            'chat.error': '**Error:** {error}',
        },
    }

    def menu_items(self) -> list[MenuItem]:
        return [MenuItem('menu.chat', 'smart_toy', '/chat', order=5)]

    def register_pages(self, ctx: ModuleContext) -> None:
        auth_manager = ctx.auth_manager
        app_menu = ctx.app_menu

        @ui.page('/chat')
        @require_access(auth_manager, MODULE_SEARCH, PERM_READ)
        def chat_page():
            app_menu.render(auth_manager)
            render_chat_page()


MODULE = ChatModule()
