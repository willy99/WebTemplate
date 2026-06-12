"""
Contracts for pluggable feature modules ("puzzle pieces").

A feature module is a package under modules/ exposing a MODULE attribute
(an AppModule instance). The registry (modules/__init__.py) discovers it
automatically — no changes to navigation.py or components.py are needed.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from gui.components import AppMenu
from gui.services.auth_manager import AuthManager
from service.processing.MyWorkFlow import MyWorkFlow


@dataclass
class MenuItem:
    """One entry in the app menu (desktop dropdown + mobile drawer)."""
    label_key: str      # i18n key, e.g. 'menu.my_tasks'
    icon: str           # material icon name
    route: str          # navigation target, e.g. '/tasks/today'
    order: int = 100    # sort order inside the section


@dataclass
class MenuSection:
    """A dropdown/expansion in the menu. Modules sharing the same id are merged."""
    id: str             # e.g. 'plans'
    label_key: str      # i18n key for the section title
    icon: str
    order: int = 100    # sort order among sections


@dataclass
class ModuleContext:
    """Everything a module gets from the core at registration time."""
    workflow: MyWorkFlow         # MyWorkFlow — access to db, services, log_manager
    auth_manager: AuthManager    # AuthManager — sessions, permissions
    app_menu: AppMenu            # AppMenu — call app_menu.render(auth_manager) in pages


class AppModule(ABC):
    """
    Manifest of one feature module. Subclass it in modules/<name>/__init__.py
    and expose an instance as MODULE.
    """

    id: str = ''                       # unique module id, e.g. 'tasks'
    permission_module: str = ''        # security module name for require_access / has_access
    permission_label: str = ''         # human label, merged into AVAILABLE_MODULES
    menu_section: MenuSection | None = None  # None => items render as top-level buttons
    translations: dict[str, dict[str, str]] = {}  # {'uk': {...}, 'en': {...}}

    def menu_items(self) -> list[MenuItem]:
        return []

    @abstractmethod
    def register_pages(self, ctx: ModuleContext) -> None:
        """Register all @ui.page routes of this module."""

    def header_widgets(self, ctx: ModuleContext) -> None:
        """Optional: render widgets (badges, buttons) into the app header.
        Called by AppMenu inside the header row on every page render."""
