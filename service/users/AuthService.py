from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

from dics.security_config import MODULE_ADMIN, MODULE_SEARCH, MODULE_TASK, MODULE_REPORT_GENERAL
from domain.user import User
import uuid
import secrets
import string
from datetime import datetime, timedelta
import config
from service.constants import DB_TABLE_USER, DB_TABLE_ROLES
import asyncio

class AuthService:

    def __init__(self, db, user_service):
        self.db = db
        self.user_service = user_service

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """Перевірка логіну/пароля."""
        # Використовуємо SELECT *, або чітко перелічуємо поля
        query = f"SELECT * FROM {DB_TABLE_USER} WHERE username = ? AND is_active = 1"
        row = self.db.__execute_fetch__(query, (username,))
        if not row:
            check_password_hash(generate_password_hash("dummy_password"), password)
            # Штучна затримка, щоб уповільнити brute-force (наприклад, 1 секунда)
            await asyncio.sleep(1)
            return None

        user_id = row['id']

        if row['lockout_until']:
            lockout_time = datetime.fromisoformat(row['lockout_until'])
            if datetime.now() < lockout_time:
                remaining = int((lockout_time - datetime.now()).total_seconds() / 60)
                await asyncio.sleep(0.5)
                raise PermissionError(f"Акаунт заблоковано. Спробуйте через {remaining} хв.")


        if row and check_password_hash(row['password_hash'], password):
            user = self.user_service.map_to_user(row)
            if user:
                # УСПІХ: Скидаємо лічильник помилок
                self.reset_failed_attempts(user_id)

                user.permissions = self.user_service.get_user_permissions(user.role)
                new_token = str(uuid.uuid4())
                update_query = f"UPDATE {DB_TABLE_USER} SET session_token = ? WHERE id = ?"
                self.db.__execute_query__(update_query, (new_token, row['id']))
                user.session_token = new_token
                return user
        else:
            self.register_failed_attempt(user_id)
            await asyncio.sleep(1)
        return None


    def clear_force_password_change(self, user_id: int):
        return self.db.__execute_query__(f"UPDATE {DB_TABLE_USER} SET force_password_change = ? WHERE id = ?", (0, user_id))

    def invalidate_session_token(self, user_id: int) -> None:
        """
        Скидає session_token у БД при logout.
        Перехоплений токен стає недійсним негайно, не чекаючи таймауту сесії.
        """
        self.db.__execute_query__(
            f"UPDATE {DB_TABLE_USER} SET session_token = NULL WHERE id = ?",
            (user_id,)
        )

    def init_default_admin(self):
        """
        Створює адміна при першому запуску, якщо БД порожня.
        Пароль генерується криптографічно безпечним способом і виводиться ОДИН РАЗ.
        При першому вході система примусово вимагає змінити пароль.
        """
        if not self.user_service.get_user_by_username('admin'):
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            temp_password = ''.join(secrets.choice(alphabet) for _ in range(16))

            self.user_service.create_user('admin', temp_password, 'admin', 'Адміністратор',
                             force_password_change=True)

            print("=" * 60)
            print("✅  ПЕРШИЙ ЗАПУСК: створено адміністратора")
            print(f"    Логін:  admin")
            print(f"    Пароль: {temp_password}")
            print("⚠️   Збережіть цей пароль! Після входу система")
            print("     одразу вимагатиме його замінити на власний.")
            print("=" * 60)

    def seed_default_role_permissions(self):
        """
        Inserts initial permissions for all default roles using INSERT OR IGNORE,
        so manual changes made via the admin panel are never overwritten.
        Safe to call on every startup.
        """
        defaults = [
            ('admin',    MODULE_SEARCH,          1, 1, 1),
            ('admin',    MODULE_ADMIN,            1, 1, 1),
            ('admin',    MODULE_TASK,             1, 1, 1),
            ('admin',    MODULE_REPORT_GENERAL,   1, 1, 1),
            ('Командір', MODULE_SEARCH,           1, 0, 0),
            ('Командір', MODULE_TASK,             1, 1, 0),
            ('Командір', MODULE_REPORT_GENERAL,   1, 0, 0),
            ('Офіс',     MODULE_SEARCH,           1, 0, 0),
            ('Офіс',     MODULE_TASK,             1, 1, 0),
            ('Бджілка',  MODULE_SEARCH,           1, 0, 0),
            ('Гість',    MODULE_SEARCH,           1, 0, 0),
        ]
        query = '''
            INSERT OR IGNORE INTO role_permissions (role, module_name, can_read, can_write, can_delete)
            VALUES (?, ?, ?, ?, ?)
        '''
        for row in defaults:
            self.db.__execute_query__(query, row)

    def get_roles(self) -> list[str]:
        """Returns role names from the DB. Falls back to hardcoded list on error."""
        rows = self.db.__execute_fetchall__(f"SELECT name FROM {DB_TABLE_ROLES} ORDER BY name")
        if rows:
            return [row['name'] for row in rows]
        return ['admin', 'Командір', 'Офіс', 'Бджілка', 'Гість']

    def get_roles_full(self) -> list[dict]:
        """Returns roles with name and description for the admin panel."""
        rows = self.db.__execute_fetchall__(
            f"SELECT name, description FROM {DB_TABLE_ROLES} ORDER BY name"
        )
        return [dict(row) for row in rows] if rows else []

    def add_role(self, name: str, description: str) -> tuple[bool, str]:
        try:
            self.db.__execute_query__(
                f"INSERT INTO {DB_TABLE_ROLES} (name, description) VALUES (?, ?)",
                (name.strip(), description.strip())
            )
            return True, f'Роль "{name}" успішно додано'
        except Exception as e:
            return False, f'Помилка: роль вже існує або невірні дані'

    def delete_role(self, name: str) -> tuple[bool, str]:
        if name == 'admin':
            return False, 'Роль "admin" захищена від видалення'
        row = self.db.__execute_fetch__(
            "SELECT COUNT(*) AS cnt FROM users WHERE role = ?", (name,)
        )
        if row and row['cnt'] > 0:
            return False, f'Неможливо видалити: {row["cnt"]} користувач(ів) мають цю роль'
        self.db.__execute_query__("DELETE FROM role_permissions WHERE role = ?", (name,))
        self.db.__execute_query__(f"DELETE FROM {DB_TABLE_ROLES} WHERE name = ?", (name,))
        return True, f'Роль "{name}" видалено'

    def set_permissions(self, role: str, module_name: str, can_read: int, can_write: int, can_delete: int):

        """
        Встановлює або оновлює права доступу для конкретної ролі у модулі.
        Використовує UPSERT: якщо запис для (role, module_name) вже є, він оновиться.
        """
        query = '''
            INSERT INTO role_permissions (role, module_name, can_read, can_write, can_delete)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(role, module_name) DO UPDATE SET 
                can_read = excluded.can_read,
                can_write = excluded.can_write,
                can_delete = excluded.can_delete
        '''
        return self.db.__execute_query__(query, (role, module_name, can_read, can_write, can_delete))


    def register_failed_attempt(self, user_id: int):
        """Збільшує лічильник помилок та блокує юзера, якщо ліміт вичерпано."""
        user:User = self.user_service.get_user_by_id(user_id)
        new_attempts = (user.failed_login_attempts or 0) + 1
        lockout_until = None

        if new_attempts >= config.SECURITY_MAX_ATTEMPTS:
            lockout_until = (datetime.now() + timedelta(minutes=config.SECURITY_LOCKOUT_DURATION_MINS)).isoformat()
            print(f"SECURITY: User ID {user_id} locked out until {lockout_until}")

        self.db.__execute_query__(
            f"UPDATE {DB_TABLE_USER} SET failed_login_attempts = ?, lockout_until = ? WHERE id = ?",
            (new_attempts, lockout_until, user_id)
        )

        return new_attempts, lockout_until

    def reset_failed_attempts(self, user_id: int):
        query = f"UPDATE {DB_TABLE_USER} SET failed_login_attempts = 0, lockout_until = NULL WHERE id = ?"
        self.db.__execute_query__(query, (user_id,))


    def is_ip_blocked(self, ip: str, max_attempts=config.SECURITY_MAX_ATTEMPTS, window_seconds=300) -> bool:
        """Checks whether an IP has exceeded the failed-login limit within the rolling window."""
        row = self.db.__execute_fetch__(
            "SELECT COUNT(*) AS cnt FROM login_attempts WHERE ip_address = ? AND attempted_at > datetime('now', ?)",
            (ip, f'-{window_seconds} seconds')
        )
        return bool(row and row['cnt'] >= max_attempts)

    def register_ip_attempt(self, ip: str):
        """Records a failed login attempt for an IP and prunes records outside the window."""
        self.db.__execute_query__(
            "DELETE FROM login_attempts WHERE attempted_at < datetime('now', '-300 seconds')"
        )
        self.db.__execute_query__(
            "INSERT INTO login_attempts (ip_address) VALUES (?)",
            (ip,)
        )