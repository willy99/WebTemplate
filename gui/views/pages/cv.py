from nicegui import ui, app
import math

from gui.views.pages.cv_dict import *


# Хелпер для визначення класів та кольорів залежно від обраної теми/мови
def get_theme(lang: str):
    if lang == 'uk':
        return {
            'card_bg': 'bg-white',
            'border': 'border-green-600',
            'title': 'text-green-700',
            'text': 'text-gray-900',
            'text_muted': 'text-gray-700',
            'text_sub': 'text-gray-600',
            'icon': 'text-green-600',
            'badge_color': 'green-200',
            'badge_text': 'text-green-900',
            'btn_flat': 'black'
        }
    else:
        return {
            'card_bg': 'bg-[#1e1e1e]',
            'border': 'border-green-500',
            'title': 'text-green-400',
            'text': 'text-white',
            'text_muted': 'text-gray-300',
            'text_sub': 'text-gray-400',
            'icon': 'text-green-500',
            'badge_color': 'green-800',
            'badge_text': 'text-white',
            'btn_flat': 'white'
        }


def education_content_ui(lang: str, dialog):
    data = CV_EDU_DATA[lang]
    theme = get_theme(lang)

    with ui.column().classes('w-full gap-3'):
        ui.label(data['title']).classes(f'text-3xl font-bold {theme["title"]} font-mono')
        ui.separator().classes('bg-gray-500')

        with ui.row().classes('items-start justify-between w-full mt-2'):
            ui.label(data['uni']).classes(f'text-xl font-semibold w-2/3 {theme["text"]}')
            ui.badge(data['period'], color=theme['badge_color']).classes(f'text-base px-3 py-1 font-mono {theme["badge_text"]}')

        with ui.column().classes(f'gap-2 mt-2 {theme["text_muted"]} text-lg'):
            with ui.row().classes('items-center gap-3'):
                ui.icon('computer', size='md').classes(theme['icon'])
                ui.label(data['faculty'])

            with ui.row().classes('items-center gap-3'):
                ui.icon('security', size='md').classes(theme['icon'])
                ui.label(data['specialty'])

            with ui.row().classes('items-center gap-3'):
                ui.icon('school', size='md').classes(theme['icon'])
                ui.label(data['degree']).classes(f'font-medium {theme["text"]}')
    ui.button(CLOSE_BT[lang], on_click=dialog.close).classes('mt-8 px-6 py-2 text-lg')


def contact_content_ui(lang: str, dialog):
    data = CV_CONTACT_DATA[lang]
    labels = data['labels']
    theme = get_theme(lang)

    with ui.column().classes('w-full gap-5'):
        ui.label(labels['title']).classes(f'text-4xl font-bold {theme["title"]} font-mono mb-2')

        with ui.column().classes(f'gap-3 {theme["text"]} text-xl'):
            ui.label(f"{labels['address']}:").classes(f'{theme["icon"]} font-bold')
            ui.label(data['address']).classes(theme["text_muted"])

            ui.separator().classes('my-2 w-full')

            ui.label(f"{labels['phone']}:").classes(f'{theme["icon"]} font-bold')
            ui.link(data['phone'], f'tel:{data["phone"].replace(" ", "")}').classes('text-blue-500 hover:text-blue-400')

            ui.label(f"{labels['email']}:").classes(f'{theme["icon"]} font-bold')
            ui.link(data['email'], f'mailto:{data["email"]}').classes('text-blue-500 hover:text-blue-400')

            ui.label('LinkedIn:').classes(f'{theme["icon"]} font-bold')
            ui.link('View Profile', data['linkedin'], new_tab=True).classes('text-blue-500 hover:text-blue-400')

    ui.button(CLOSE_BT[lang], on_click=dialog.close).classes('mt-8 px-6 py-2 text-lg')


def project_content_ui(lang, dialog):
    projects = CV_PROJECTS_DATA[lang]
    theme = get_theme(lang)

    with ui.card().classes(f'w-full min-h-[450px] {theme["card_bg"]} shadow-none p-4'):
        with ui.tabs().classes(f'w-full text-lg {theme["text"]}') as tabs:
            for p in projects:
                with ui.tab(p['id']):
                    with ui.row().classes('items-center'):
                        ui.image(p['icon']).classes('w-8 h-8 mr-2').props('fit=cover position=left')

        with ui.tab_panels(tabs, value=projects[0]['id']).classes('w-full bg-transparent mt-4'):
            for p in projects:
                with ui.tab_panel(p['id']).classes(f'{theme["text"]} p-0'):
                    with ui.scroll_area().classes('w-full h-[350px] pr-4'):
                        with ui.row().classes('items-center mb-4 mt-2'):
                            ui.image(p['icon']).classes('w-16 h-16 mr-6').props('fit=cover position=left')
                            with ui.column():
                                ui.label(p['title']).classes(f'text-3xl font-bold {theme["title"]}')
                                ui.label(p['role']).classes(f'text-xl {theme["icon"]}')

                        ui.label(p['date']).classes(f'text-base {theme["text_sub"]} font-mono mb-3')
                        ui.label(p['description']).classes(f'text-xl {theme["text_muted"]} mt-2 whitespace-pre-line')

                        ui.label(p['details']).classes(f'text-lg {theme["text_sub"]} mt-4 whitespace-pre-line')

    ui.button(CLOSE_BT[lang], on_click=dialog.close).classes('mt-6 px-6 py-2 text-lg')


def hobby_content_ui(lang, dialog):
    data = CV_HOBBY_DATA[lang]
    theme = get_theme(lang)

    with ui.column().classes('w-full gap-5'):
        ui.label(data['title']).classes(f'text-4xl font-bold {theme["title"]} font-mono mb-4')

        for item in data['items']:
            # Додано flex-nowrap (не розривати рядок) та items-start (вирівнювання по верху)
            with ui.row().classes('items-start flex-nowrap w-full gap-4'):

                # Додано shrink-0 (щоб іконка не сплющувалась) та mt-1 (щоб бути на рівні першого рядка тексту)
                ui.icon(item['icon'], size='lg').classes(f'{theme["icon"]} shrink-0 mt-1')

                # Додано whitespace-normal для коректного переносу тексту
                if 'url' in item:
                    ui.link(item['text'], item['url'], new_tab=True).classes(
                        'text-xl text-blue-500 hover:text-blue-400 underline font-medium whitespace-normal'
                    )
                else:
                    ui.label(item['text']).classes(f'{theme["text_muted"]} text-xl whitespace-normal')

    ui.button(CLOSE_BT[lang], on_click=dialog.close).classes('mt-8 px-6 py-2 text-lg')


def languages_content_ui(lang, dialog):
    data = CV_LANGUAGES_DATA[lang]
    theme = get_theme(lang)

    with ui.column().classes('w-full gap-5'):
        ui.label(data['title']).classes(f'text-4xl font-bold {theme["title"]} font-mono mb-4')

        for item in data['items']:
            with ui.row().classes('items-center justify-between w-full p-3 border-b border-gray-500'):
                ui.label(item['lang']).classes(f'{theme["text"]} text-2xl font-bold')
                ui.badge(item['level'], color=theme['badge_color']).classes(f'text-base px-3 py-1 font-mono {theme["badge_text"]}')

    ui.button(CLOSE_BT[lang], on_click=dialog.close).classes('mt-8 px-6 py-2 text-lg')


def skills_content_ui(lang, dialog):
    theme = get_theme(lang)
    title_text = 'Technical Skills' if lang == 'en' else 'Технічні Навички'

    LEVEL_CONFIG = {
        'expert':       {'en': 'Expert',       'uk': 'Експерт',    'color': 'green',  'icon': 'workspace_premium'},
        'advanced':     {'en': 'Advanced',     'uk': 'Просунутий', 'color': 'blue',   'icon': 'trending_up'},
        'intermediate': {'en': 'Intermediate', 'uk': 'Середній',   'color': 'orange', 'icon': 'show_chart'},
    }

    with ui.column().classes('w-full gap-3'):
        ui.label(title_text).classes(f'text-3xl font-bold {theme["title"]} font-mono mb-1')
        ui.separator().classes('bg-gray-500 mb-2')

        with ui.scroll_area().classes('w-full h-[460px] pr-3'):
            with ui.column().classes('w-full gap-3'):
                for category, data in CV_SKILLS_DATA.items():
                    card_bg = 'bg-gray-800' if lang == 'en' else 'bg-gray-50'
                    with ui.element('div').classes(
                        f'w-full rounded-xl border-l-4 {theme["border"]} {card_bg} p-4'
                    ):
                        # Header: icon + category name + optional level badge
                        with ui.row().classes('items-center justify-between w-full mb-3'):
                            with ui.row().classes('items-center gap-2'):
                                ui.icon(data['icon'], size='sm').classes(theme['icon'])
                                ui.label(category).classes(
                                    f'text-sm font-bold {theme["text"]} font-mono uppercase tracking-widest'
                                )
                            if data['level']:
                                cfg = LEVEL_CONFIG[data['level']]
                                with ui.row().classes('items-center gap-1'):
                                    ui.icon(cfg['icon'], size='xs').classes(f'text-{cfg["color"]}-400')
                                    ui.badge(cfg[lang], color=cfg['color']).classes('text-xs px-2 font-mono')

                        # Skill chips
                        with ui.row().classes('w-full flex-wrap gap-2'):
                            for skill in data['items']:
                                ui.badge(skill, color=theme['badge_color']).classes(
                                    f'px-3 py-1 text-sm rounded-full {theme["badge_text"]} font-medium'
                                )

    ui.button(CLOSE_BT[lang], on_click=dialog.close).classes('mt-6 px-6 py-2 text-lg')


def experience_content_ui(lang, dialog):
    data = CV_EXP_DATA[lang]
    theme = get_theme(lang)

    with ui.column().classes('w-full gap-4'):
        ui.label(data['title']).classes(f'text-4xl font-bold {theme["title"]} font-mono mb-4')

        with ui.scroll_area().classes('w-full h-[400px] pr-4'):
            with ui.timeline(color='green').classes('w-full text-lg'):
                for item in data['items']:
                    with ui.timeline_entry('', subtitle=''):
                        # 1. Змінено -mt-4 на -mt-6 (або -mt-8), щоб підтягнути весь блок вище до крапочки
                        with ui.column().classes('w-full gap-1 -mt-6'):
                            with ui.row().classes('w-full justify-between items-center flex-wrap gap-2'):
                                # 2. Додано leading-none, щоб прибрати зайвий відступ над великими літерами
                                ui.label(item['company']).classes(f'text-3xl font-extrabold {theme["title"]} font-mono leading-none')
                                ui.badge(item['period'], color=theme['badge_color']).classes(f'text-sm px-3 py-1 font-mono {theme["badge_text"]}')

                            ui.label(item['role']).classes(f'text-2xl font-bold {theme["text"]} mt-1')
                            ui.label(item['description']).classes(f'text-xl {theme["text_muted"]} mt-2 whitespace-pre-line')

                            ui.separator().classes('my-4 bg-gray-600')

    ui.button(CLOSE_BT[lang], on_click=dialog.close).classes('mt-8 px-6 py-2 text-lg')

def open_about_dialog():
    lang = app.storage.user.get('lang', 'en')
    theme = get_theme(lang)
    data = CV_ABOUT_DATA[lang]

    with ui.dialog() as dialog, ui.card().classes(f'w-11/12 max-w-3xl {theme["card_bg"]} border {theme["border"]} p-8'):
        ui.label(data['title']).classes(f'text-4xl font-bold {theme["title"]} font-mono mb-4')
        ui.label(data['born']).classes(f'{theme["text"]} text-xl font-bold')
        ui.label(data['about']).classes(f'{theme["text_muted"]} text-xl mt-3')
        ui.label(data['credo']).classes(f'{theme["icon"]} text-xl mt-5 italic font-medium')
        ui.label(data['aims']).classes(f'{theme["text_muted"]} text-xl mt-5')
        ui.label(data['approach']).classes(f'{theme["text_muted"]} text-xl mt-3')

        ui.button(CLOSE_BT[lang], on_click=dialog.close).classes('mt-8 px-6 py-2 text-lg')
    dialog.open()



async def render_cv_page():
    @ui.refreshable
    def cv_orbit_ui():
        lang = app.storage.user.get('lang', 'en')
        categories = CV_CATEGORIES_DATA[lang]
        theme = get_theme(lang)

        if lang == 'uk':
            ui.run_javascript('document.body.classList.add("light-theme")')
        else:
            ui.run_javascript('document.body.classList.remove("light-theme")')

        # ── 1. Спочатку створюємо всі діалоги і зберігаємо посилання ──────────
        card_classes = f'w-11/12 max-w-3xl min-h-[400px] {theme["card_bg"]} border {theme["border"]} relative p-8'
        dialogs = {}
        for cat in categories:
            if cat['id'] == 'edu':
                with ui.dialog() as dialog, ui.card().classes(card_classes):
                    ui.button(icon='close', on_click=dialog.close).props(f'flat round dense color={theme["btn_flat"]}').classes('absolute top-4 right-4 z-10')
                    education_content_ui(lang, dialog)
            elif cat['id'] == 'contact':
                with ui.dialog() as dialog, ui.card().classes(card_classes):
                    ui.button(icon='close', on_click=dialog.close).props(f'flat round dense color={theme["btn_flat"]}').classes('absolute top-4 right-4 z-10')
                    contact_content_ui(lang, dialog)
            elif cat['id'] == 'proj':
                with ui.dialog() as dialog, ui.card().classes(card_classes):
                    ui.button(icon='close', on_click=dialog.close).props(f'flat round dense color={theme["btn_flat"]}').classes('absolute top-4 right-4 z-10')
                    project_content_ui(lang, dialog)
            elif cat['id'] == 'exp':
                with ui.dialog() as dialog, ui.card().classes(card_classes):
                    ui.button(icon='close', on_click=dialog.close).props(f'flat round dense color={theme["btn_flat"]}').classes('absolute top-4 right-4 z-10')
                    experience_content_ui(lang, dialog)
            elif cat['id'] == 'hobby':
                with ui.dialog() as dialog, ui.card().classes(card_classes):
                    ui.button(icon='close', on_click=dialog.close).props(f'flat round dense color={theme["btn_flat"]}').classes('absolute top-4 right-4 z-10')
                    hobby_content_ui(lang, dialog)
            elif cat['id'] == 'lang':
                with ui.dialog() as dialog, ui.card().classes(card_classes):
                    ui.button(icon='close', on_click=dialog.close).props(f'flat round dense color={theme["btn_flat"]}').classes('absolute top-4 right-4 z-10')
                    languages_content_ui(lang, dialog)
            elif cat['id'] == 'skills':
                with ui.dialog() as dialog, ui.card().classes(card_classes):
                    ui.button(icon='close', on_click=dialog.close).props(f'flat round dense color={theme["btn_flat"]}').classes('absolute top-4 right-4 z-10')
                    skills_content_ui(lang, dialog)
            else:
                with ui.dialog() as dialog, ui.card().classes(card_classes):
                    ui.button(icon='close', on_click=dialog.close).props(f'flat round dense color={theme["btn_flat"]}').classes('absolute top-4 right-4 z-10')
                    ui.label(cat['label']).classes(f'text-3xl font-bold {theme["title"]} font-mono mb-4 border-b border-gray-500 pb-2 w-full')
                    ui.label(f'{PLACEHOLDER_TEXT[lang]} {cat["label"]}...').classes(f'{theme["text_muted"]} mt-4 text-xl font-mono')
            dialogs[cat['id']] = dialog

        # ── 2. Desktop: орбітальний layout ───────────────────────────────────
        with ui.element('div').classes('cv-orbit-layout w-full'):
            with ui.element('div').classes('cv-container'):
                with ui.element('div').classes('cv-center').on('click', open_about_dialog):
                    ui.image("/static/images/cv/myphoto.jpeg").classes('cv-photo')
                    ui.label(NAME_LABEL[lang]).classes(f'text-4xl font-bold {theme["title"]} font-mono tracking-wider')
                    ui.label(ROLE_TEXT[lang]).classes(f'text-2xl {theme["text_sub"]} mt-2 font-mono')

                center_x, center_y = 400, 300
                radius_x, radius_y = 320, 220

                for i, cat in enumerate(categories):
                    angle = (i / len(categories)) * 2 * math.pi
                    x = center_x + radius_x * math.cos(angle)
                    y = center_y + radius_y * math.sin(angle)
                    with ui.element('div').classes('cv-node-wrapper cursor-pointer').style(f'left: {x}px; top: {y}px;').on('click', dialogs[cat['id']].open):
                        btn = ui.button(icon=cat['icon'], on_click=dialogs[cat['id']].open)
                        btn.props(f'round size=xl color={cat["color"]}')
                        btn.classes('shadow-lg')
                        ui.label(cat['label']).classes('node-label font-mono font-bold text-lg')

        # ── 3. Mobile: grid layout ────────────────────────────────────────────
        with ui.element('div').classes('cv-mobile-layout w-full'):
            # Шапка з фото + ім'ям — клік → about dialog
            with ui.element('div').classes('cv-mobile-header').on('click', open_about_dialog):
                ui.image("/static/images/cv/myphoto.jpeg").classes('cv-mobile-photo')
                with ui.column().classes('items-start gap-1 min-w-0'):
                    ui.label(NAME_LABEL[lang]).classes(f'text-xl font-bold {theme["title"]} font-mono tracking-wide leading-tight')
                    ui.label(ROLE_TEXT[lang]).classes(f'text-sm {theme["text_sub"]} font-mono')
                    hint = 'tap to learn more →' if lang == 'en' else 'натисніть, щоб дізнатись більше →'
                    ui.label(hint).classes(f'text-xs {theme["text_sub"]} italic mt-1')

            # Сітка категорій
            with ui.element('div').classes('cv-mobile-grid'):
                for cat in categories:
                    with ui.element('div').classes('cv-mobile-card').on('click', dialogs[cat['id']].open):
                        btn = ui.button(icon=cat['icon'])
                        btn.props(f'round size=md color={cat["color"]}')
                        btn.style('pointer-events: none;')  # клік обробляє батьківський div
                        ui.label(cat['label']).classes(f'{theme["text"]} font-mono font-bold text-xs text-center leading-tight mt-2')

    # 2. CSS стилі
    ui.add_head_html('''
        <style>
            :root {
                --bg-body: #121212;
                --bg-container: #1e1e1e;
                --border-container: #333;
                --shadow-color: rgba(74, 222, 128, 0.2);
                --node-label-bg: rgba(0, 0, 0, 0.8);
                --node-label-text: #e0e0e0;
                --node-label-border: #4ade80;
            }
            body.light-theme {
                --bg-body: #f0f2f5;
                --bg-container: #ffffff;
                --border-container: #d1d5db;
                --shadow-color: rgba(22, 163, 74, 0.3);
                --node-label-bg: rgba(255, 255, 255, 0.95);
                --node-label-text: #1f2937;
                --node-label-border: #16a34a;
            }
            body {
                background-color: var(--bg-body);
                margin: 0; padding: 0;
                transition: background-color 0.4s ease;
            }

            /* ── Desktop orbit ─────────────────────────────── */
            .cv-orbit-layout { display: block; }
            .cv-mobile-layout { display: none; }

            .cv-container {
                position: relative;
                width: 800px; height: 600px; margin: 60px auto;
                border-radius: 20px;
                background: var(--bg-container);
                box-shadow: 0 0 30px var(--shadow-color);
                border: 1px solid var(--border-container);
                transition: background 0.4s ease, box-shadow 0.4s ease, border-color 0.4s ease;
            }
            .cv-center {
                position: absolute; top: 50%; left: 50%;
                transform: translate(-50%, -50%); text-align: center;
                display: flex; flex-direction: column; align-items: center;
                cursor: pointer;
                transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                z-index: 5;
            }
            .cv-center:hover { transform: translate(-50%, -50%) scale(1.15); z-index: 20; }
            .cv-photo {
                width: 180px; height: 180px; border-radius: 50%;
                object-fit: cover; border: 4px solid var(--node-label-border);
                box-shadow: 0 0 20px var(--shadow-color); margin-bottom: 15px;
            }
            .cv-node-wrapper {
                position: absolute;
                transform: translate(-50%, -50%);
                display: flex; flex-direction: column; align-items: center; gap: 10px;
                transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                z-index: 10;
            }
            .cv-node-wrapper:hover { transform: translate(-50%, -50%) scale(1.2); z-index: 20; }
            .node-label {
                color: var(--node-label-text);
                background: var(--node-label-bg);
                padding: 4px 12px; border-radius: 8px;
                border: 1px solid var(--node-label-border);
                white-space: nowrap; transition: all 0.4s ease;
            }

            /* ── Mobile layout ─────────────────────────────── */
            @media (max-width: 860px) {
                .cv-orbit-layout { display: none; }
                .cv-mobile-layout {
                    display: block;
                    padding: 16px;
                    padding-top: 72px; /* місце для language toggle */
                }
            }

            .cv-mobile-header {
                display: flex; align-items: center; gap: 16px;
                padding: 16px; margin-bottom: 16px;
                border-radius: 16px;
                background: var(--bg-container);
                border: 1px solid var(--border-container);
                box-shadow: 0 0 20px var(--shadow-color);
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .cv-mobile-header:active { transform: scale(0.98); }

            .cv-mobile-photo {
                width: 72px; height: 72px; border-radius: 50%;
                object-fit: cover;
                border: 3px solid var(--node-label-border);
                flex-shrink: 0;
            }

            .cv-mobile-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 12px;
            }

            .cv-mobile-card {
                display: flex; flex-direction: column;
                align-items: center; justify-content: center;
                padding: 20px 12px; min-height: 110px;
                border-radius: 16px;
                background: var(--bg-container);
                border: 1px solid var(--border-container);
                box-shadow: 0 4px 12px var(--shadow-color);
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            .cv-mobile-card:active {
                transform: scale(0.96);
                box-shadow: 0 0 20px var(--shadow-color);
            }

            /* ── Діалоги на мобільному ─────────────────────── */
            @media (max-width: 860px) {
                .q-dialog__inner > .q-card {
                    width: 96vw !important;
                    max-width: 96vw !important;
                    min-height: unset !important;
                    padding: 16px !important;
                }
                .q-dialog__inner > .q-card .q-scroll-area {
                    height: 55vh !important;
                }
            }
        </style>
    ''')

    # 3. Перемикач мов
    with ui.row().classes('w-full justify-end p-6 absolute top-0 right-0 z-50'):
        def change_lang(e):
            app.storage.user['lang'] = e.value
            # Тепер ми викликаємо оновлення у ЛОКАЛЬНОЇ функції.
            # Вона гарантовано вплине лише на інтерфейс поточного браузера.
            cv_orbit_ui.refresh()

        ui.toggle({'en': '🇬🇧 EN', 'uk': '🇺🇦 UA'},
                  value=app.storage.user.get('lang', 'en'),
                  on_change=change_lang).props('size=lg outline')

    cv_orbit_ui()


if __name__ in {"__main__", "__mp_main__"}:
    @ui.page('/')
    async def index():
        app.storage.user.setdefault('lang', 'en')
        await render_cv_page()


    ui.run(title="Pavel Zhelnov - Interactive CV", port=8080, storage_secret='my_cv_secret_key')