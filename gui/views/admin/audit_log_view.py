from nicegui import ui
import json
import config

from domain.audit_log_filter import AuditLogFilter
from domain.db.AuditLogDB import LogLevel, EventDomain, EventType
from gui.controllers.admin_audit_controller import AdminAuditController
from gui.services.auth_manager import AuthManager
from gui.tools.ui_components import ServerPagination
from service.constants import DB_DATETIME_FORMAT


def render_audit_logs(admin_audit_ctrl: AdminAuditController, auth_manager: AuthManager):
    # Стан для збереження значень фільтрів
    state = {
        'username': '',
        'domain': None,
        'event_type': None,
        'level': None,
        'date_from': '',
        'date_to': '',
        'entity_id': '',
        'text': '',
    }

    # Допоміжна функція для отримання списку користувачів
    def get_user_options():
        users = auth_manager.get_all_users()
        return [user['username'] for user in users]

    # --- ЗАВАНТАЖЕННЯ ДАНИХ ТА ФІЛЬТРАЦІЯ ---
    async def apply_filters(reset_page=True):
        search_btn.props('loading')

        # Скидаємо сторінку на першу, якщо це новий пошук
        if reset_page:
            pager.reset()

        # Формуємо об'єкт фільтра
        filters = AuditLogFilter(
            username=state['username'] if state['username'] else None,
            domain=state['domain'],
            event_type=state['event_type'],
            level=state['level'],
            date_from=state['date_from'] if state['date_from'] else None,
            date_to=state['date_to'] if state['date_to'] else None,
            entity_id=int(state['entity_id']) if state['entity_id'] and state['entity_id'].isdigit() else None,
            text=state['text'] if state['text'] else None,
            limit=pager.records_per_page,
            offset=pager.offset
        )

        try:
            ctx = auth_manager.get_current_context()

            # 1. Отримуємо та оновлюємо загальну кількість записів для пейджера
            total_count = admin_audit_ctrl.count_logs(filters)
            pager.update_total(total_count)

            # 2. Отримуємо самі лог-записи
            logs = admin_audit_ctrl.search_logs(ctx, filters)

            # 3. Перепаковуємо дані для таблиці
            rows = []
            for log in logs:
                # Обробка timestamp
                ts = log.created_at
                if hasattr(ts, 'strftime'):
                    ts = ts.strftime(DB_DATETIME_FORMAT)

                rows.append({
                    'id': log.id,
                    'timestamp': ts,
                    'level': log.level,
                    'domain': log.domain,
                    'event_type': log.event_type,
                    'username': log.username or 'Система',
                    'ip_address': log.ip_address or '-',
                    'action_summary': log.action_summary,
                    'details': log.details
                })

            table.rows = rows
            table.update()

        except Exception as e:
            ui.notify(f"Помилка завантаження логів: {e}", type="negative")
        finally:
            search_btn.props(remove='loading')

    # --- ХЕНДЛЕРИ КНОПОК ---
    def on_search():
        ui.timer(0.1, lambda: apply_filters(reset_page=True), once=True)

    def on_clear():
        state['username'] = ''
        state['domain'] = None
        state['event_type'] = None
        state['level'] = None
        state['date_from'] = ''
        state['date_to'] = ''
        state['entity_id'] = ''
        state['text'] = ''
        ui.timer(0.1, lambda: apply_filters(reset_page=True), once=True)

    # --- UI ЛЕЙАУТ ---
    with ui.column().classes('w-full items-stretch p-4'):
        ui.label('Журнал аудиту (Audit Trail)').classes('text-2xl font-bold mb-2')

        # 1. БЛОК ФІЛЬТРІВ
        with ui.card().classes('w-full mb-4 shadow-sm bg-gray-50'):
            with ui.row().classes('w-full items-center gap-4'):
                ui.select(options=get_user_options(), label='Користувач', clearable=True).bind_value(state, 'username').classes('w-40')
                ui.select(options=[e.value for e in LogLevel], label='Рівень', clearable=True).bind_value(state, 'level').classes('w-32')
                ui.select(options=[e.value for e in EventDomain], label='Область (Domain)', clearable=True).bind_value(state, 'domain').classes('w-40')
                ui.select(options=[e.value for e in EventType], label='Подія', clearable=True).bind_value(state, 'event_type').classes('w-32')

                ui.input('ID запису').bind_value(state, 'entity_id').classes('w-24')
                ui.input('Текст (пошук в JSON)').bind_value(state, 'text').classes('w-48')

                ui.input('З дати', placeholder='YYYY-MM-DD').bind_value(state, 'date_from').props('type=date').classes('w-40')
                ui.input('По дату', placeholder='YYYY-MM-DD').bind_value(state, 'date_to').props('type=date').classes('w-40')

                search_btn = ui.button('Шукати', on_click=on_search, icon='search').classes('bg-primary text-white mt-4')
                ui.button('Скинути', on_click=on_clear, icon='clear').classes('bg-gray-400 text-white mt-4')

        # 2. ТАБЛИЦЯ ДАНИХ
        columns = [
            {'name': 'id', 'label': '#', 'field': 'id', 'align': 'left'},
            {'name': 'timestamp', 'label': 'Дата та час', 'field': 'timestamp', 'align': 'left', 'sortable': True},
            {'name': 'username', 'label': 'Юзер', 'field': 'username', 'align': 'left', 'classes': 'font-bold'},
            {'name': 'ip_address', 'label': 'IP Адреса', 'field': 'ip_address', 'align': 'left'},
            {'name': 'level', 'label': 'Рівень', 'field': 'level', 'align': 'center'},
            {'name': 'domain', 'label': 'Модуль', 'field': 'domain', 'align': 'left'},
            {'name': 'event_type', 'label': 'Подія', 'field': 'event_type', 'align': 'left'},
            {'name': 'action_summary', 'label': 'Суть дії', 'field': 'action_summary', 'align': 'left'},
            {'name': 'details', 'label': 'JSON', 'field': 'details', 'align': 'center'},
        ]

        table = ui.table(columns=columns, rows=[], row_key='id').classes('w-full shadow-md')

        # 3. ПЕЙДЖЕР (ServerPagination)
        with ui.row().classes('w-full justify-center mt-4'):
            pager = ServerPagination(
                records_per_page=config.RECORDS_PER_PAGE,
                on_change=lambda: ui.timer(0.1, lambda: apply_filters(reset_page=False), once=True)
            )

        # 💡 МАГІЯ СЛОТІВ: Фарбуємо бейджики залежно від рівня (level)
        table.add_slot('body-cell-level', '''
            <q-td :props="props">
                <q-badge :color="props.row.level === 'CRITICAL' ? 'red-10' : props.row.level === 'ERROR' ? 'red' : props.row.level === 'WARNING' ? 'orange' : 'green'">
                    {{ props.row.level }}
                </q-badge>
            </q-td>
        ''')

        # 💡 МАГІЯ СЛОТІВ: Кнопка для відкриття JSON-деталей
        table.add_slot('body-cell-details', '''
            <q-td :props="props">
                <q-btn v-if="props.row.details" icon="data_object" flat dense color="primary" @click="$parent.$emit('show_details', props.row)" />
                <span v-else class="text-gray-400">-</span>
            </q-td>
        ''')

        # Хендлер для кліку по кнопці деталей
        def open_details_dialog(e):
            row = e.args
            with ui.dialog() as dialog, ui.card().classes('min-w-[800px] max-w-[90vw]'):
                ui.label(f'Деталі логу #{row["id"]} ({row["event_type"]})').classes('text-xl font-bold mb-2')

                # Перевіряємо розмір JSON для коректного відображення висоти вікна
                details_json = row['details']
                json_str = json.dumps(details_json) if isinstance(details_json, dict) else str(details_json)

                if len(json_str) > 100:
                    ui.json_editor({'content': {'json': details_json}}).classes('w-full h-[500px]')
                else:
                    ui.json_editor({'content': {'json': details_json}}).classes('w-full h-64')

                ui.button('Закрити', on_click=dialog.close).classes('w-full mt-4 bg-gray-200 text-black')
            dialog.open()

        table.on('show_details', open_details_dialog)

    # Запуск першого завантаження при відкритті сторінки
    ui.timer(0.1, lambda: apply_filters(reset_page=True), once=True)