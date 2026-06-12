"""
Module registry: discovers feature packages under modules/ and wires them
into the app (pages, menu, permissions, translations).

Adding a feature = dropping a package into modules/ with a MODULE manifest.
Core files are not touched.
"""
import importlib
import pkgutil

from modules.base import AppModule, MenuItem, MenuSection, ModuleContext

_discovered: list[AppModule] | None = None
_ctx: ModuleContext | None = None


def discover() -> list[AppModule]:
    """Imports every package under modules/ and collects MODULE manifests. Cached."""
    global _discovered
    if _discovered is not None:
        return _discovered

    import modules as pkg
    found: list[AppModule] = []
    for info in pkgutil.iter_modules(pkg.__path__):
        if not info.ispkg:
            continue
        py_mod = importlib.import_module(f'modules.{info.name}')
        manifest = getattr(py_mod, 'MODULE', None)
        if isinstance(manifest, AppModule):
            found.append(manifest)
        elif manifest is not None:
            print(f'⚠️  modules/{info.name}: MODULE is not an AppModule — skipped')

    _discovered = found
    return found


def register_all(ctx: ModuleContext) -> None:
    """Called once at startup (navigation.init_nicegui). Wires every module in."""
    from i18n import register_translations
    from dics.security_config import register_module

    global _ctx
    _ctx = ctx

    for mod in discover():
        if mod.translations:
            register_translations(mod.translations)
        if mod.permission_module and mod.permission_label:
            register_module(mod.permission_module, mod.permission_label)
        mod.register_pages(ctx)
        print(f'🧩 module loaded: {mod.id}')


def render_header_widgets() -> None:
    """Renders all modules' header widgets into the current UI container.
    Called by AppMenu inside the header row."""
    if _ctx is None:
        return
    for mod in discover():
        mod.header_widgets(_ctx)


def menu_tree(auth_manager=None) -> tuple[list[tuple[MenuSection, list[MenuItem]]], list[MenuItem]]:
    """
    Builds the menu structure for AppMenu.
    Returns (sections, top_level_items). Modules whose permission the current
    user lacks are filtered out when auth_manager is given.
    """
    from dics.security_config import PERM_READ

    sections: dict[str, tuple[MenuSection, list[MenuItem]]] = {}
    top_level: list[MenuItem] = []

    for mod in discover():
        if auth_manager and mod.permission_module \
                and not auth_manager.has_access(mod.permission_module, PERM_READ):
            continue
        items = mod.menu_items()
        if not items:
            continue
        if mod.menu_section is None:
            top_level.extend(items)
        else:
            entry = sections.setdefault(mod.menu_section.id, (mod.menu_section, []))
            entry[1].extend(items)

    ordered = sorted(sections.values(), key=lambda s: s[0].order)
    for _, items in ordered:
        items.sort(key=lambda i: i.order)
    top_level.sort(key=lambda i: i.order)
    return ordered, top_level
