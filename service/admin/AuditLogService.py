import json
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime

from domain.audit_log_filter import AuditLogFilter
from domain.db.AuditLogDB import AuditLogDB, LogLevel, EventDomain, EventType
from service.constants import DB_DATETIME_FORMAT


class AuditLogService:
    def __init__(self, db):
        """
        db: екземпляр вашого MyDataBase
        """
        self.db = db
        self.table_name = "audit_logs"

    def log_event(self, entry: AuditLogDB) -> int:
        """
        Створює новий запис у журналі аудиту.
        Повертає ID створеного запису.
        """
        # Перетворюємо Pydantic модель у словник.
        # exclude_unset=True гарантує, що ми не запишемо зайві None у БД
        data = entry.model_dump(by_alias=True, exclude={"id"}, exclude_none=True)

        # Конвертуємо словник details у JSON-рядок для SQLite
        if 'details' in data and data['details'] is not None:
            data['details'] = json.dumps(data['details'], ensure_ascii=False)

        # Якщо timestamp є datetime, конвертуємо в рядок ISO
        if isinstance(data.get('timestamp'), datetime):
            data['timestamp'] = data['timestamp'].strftime(DB_DATETIME_FORMAT)

        # Використовуємо ваш існуючий метод для запису
        record_id = self.db.insert_record(self.table_name, data)
        return record_id

    def _build_where_conditions(self, filters: AuditLogFilter) -> Tuple[str, list]:
        """Допоміжний метод для формування умов WHERE та параметрів."""
        query_parts = ["1=1"]
        params = []

        if filters.username:
            query_parts.append("username = ?")
            params.append(filters.username)
        if filters.domain:
            query_parts.append("domain = ?")
            params.append(filters.domain)
        if filters.event_type:
            query_parts.append("event_type = ?")
            params.append(filters.event_type)
        if filters.level:
            query_parts.append("level = ?")
            params.append(filters.level)
        if filters.entity_id:
            query_parts.append("entity_id = ?")
            params.append(filters.entity_id)
        if filters.text:
            query_parts.append("LOWER_UA(details) LIKE ?")
            params.append('%' + filters.text.lower() + '%')
        if filters.date_from:
            query_parts.append("timestamp >= ?")
            params.append(filters.date_from)
        if filters.date_to:
            query_parts.append("timestamp <= ?")
            params.append(filters.date_to)

        return " AND ".join(query_parts), params

    def count_logs(self, filters: AuditLogFilter) -> int:
        """
        Повертає загальну кількість записів за заданими фільтрами (для пейджера).
        """
        where_clause, params = self._build_where_conditions(filters)
        query = f"SELECT COUNT(*) as cnt FROM {self.table_name} WHERE {where_clause}"

        records = self.db.__execute_fetchall__(query, tuple(params))
        if records:
            # Дістаємо значення COUNT(*) з результату
            return dict(records[0]).get('cnt', 0)
        return 0

    def search_logs(self, filters: AuditLogFilter) -> List[AuditLogDB]:
        """
        Пошук по логах з пагінацією.
        """
        where_clause, params = self._build_where_conditions(filters)

        # Сортування: найновіші зверху, плюс пагінація
        query = f"SELECT * FROM {self.table_name} WHERE {where_clause} ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([filters.limit, filters.offset])

        records = self.db.__execute_fetchall__(query, tuple(params))

        results = []
        for row in records:
            row_dict = dict(row)
            if row_dict.get('details'):
                try:
                    row_dict['details'] = json.loads(row_dict['details'])
                except json.JSONDecodeError:
                    row_dict['details'] = {"raw_error": row_dict['details']}
            results.append(AuditLogDB(**row_dict))

        return results

    def clear_old_logs(self, days_to_keep: int = 30) -> bool:
        """
        Видаляє логи, які старіші за вказану кількість днів.
        Рекомендується викликати раз на місяць через планувальник (cron).
        """
        query = f"DELETE FROM {self.table_name} WHERE timestamp < datetime('now', '-{days_to_keep} days')"
        # Оскільки це DELETE без конкретного ID, використовуємо прямий execute
        result_id = self.db.__execute_query__(query)
        print(f"✅ Старі логи за {days_to_keep} днів видалено")
        return result_id is not None