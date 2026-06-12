"""
Lightweight i18n for the NiceGUI app.

Usage:
    from i18n import t
    ui.label(t('users.title'))
    ui.notify(t('users.role_changed', username='vlad', role='admin'))

The current language is stored per-user in app.storage.user['lang'],
so t() must be called inside a page/client context (which is the case
for all view-rendering code). Outside a context it falls back to the
default language.
"""
from nicegui import app

from i18n.uk import UK
from i18n.en import EN

DEFAULT_LANGUAGE = 'uk'

LANGUAGES = {
    'uk': '🇺🇦 Українська',
    'en': '🇬🇧 English',
}

_translations: dict[str, dict[str, str]] = {
    'uk': UK,
    'en': EN,
}


def register_translations(translations: dict[str, dict[str, str]]):
    """Merge translations contributed by a feature module: {'uk': {...}, 'en': {...}}."""
    for lang, entries in translations.items():
        _translations.setdefault(lang, {}).update(entries)


def get_language() -> str:
    try:
        return app.storage.user.get('lang', DEFAULT_LANGUAGE)
    except Exception:
        # Called outside a client context (background task, startup)
        return DEFAULT_LANGUAGE


def set_language(lang: str):
    if lang in _translations:
        app.storage.user['lang'] = lang


def t(key: str, **kwargs) -> str:
    """Translate a key. Falls back to the default language, then to the key itself."""
    lang = get_language()
    text = _translations.get(lang, {}).get(key) \
        or _translations[DEFAULT_LANGUAGE].get(key) \
        or key
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
