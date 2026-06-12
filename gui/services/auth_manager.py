from typing import Optional, List

from domain.db.AuditLogDB import *
from domain.user import User
from gui.services.request_context import RequestContext
from dics.security_config import PERM_READ
from service.processing.MyWorkFlow import MyWorkFlow
from service.users.AuthService import AuthService
import time
import config
from nicegui import app, run, ui

from service.users.UserService import UserService


class AuthManager:
    def __init__(self, workflow:MyWorkFlow):
        self.db = workflow.db
        self.user_service = workflow.user_service
        self.auth_service = workflow.auth_service
        # self.user_service = UserService(self.db, workflow.signalClient, workflow.emailClient)
        # self.auth_service = AuthService(self.db, self.user_service)
        self.auth_service.init_default_admin()
        self.auth_service.seed_default_role_permissions()
        self.audit_service = workflow.audit_log_service

        self.log_manager = workflow.log_manager

    def create_user(self, username: str, password: str, role: str, full_name: str):
        """Delegate entirely to AuthService — no duplicate hashing or SQL here."""
        return self.user_service.create_user(username, password, role, full_name)

    def get_user(self, username: str) -> User:
        return self.user_service.get_user_by_username(username)

    def get_all_users(self, only_active=None, limit=None, offset=None, search=None, role=None) -> List[Dict]:
        return self.user_service.get_all_users(
            only_active=only_active, limit=limit, offset=offset, search=search, role=role
        )

    def count_users(self, only_active=None, search=None, role=None) -> int:
        return self.user_service.count_users(only_active=only_active, search=search, role=role)

    def update_user(self, user_id: int, **kwargs):
        self.user_service.update_user(user_id=user_id, **kwargs)

    def update_password(self, user_id: int, new_password: str):
        self.user_service.update_password(user_id=user_id, new_password=new_password)

    def clear_force_password_change(self, user_id: int):
        """Знімає прапор примусової зміни пароля після успішної зміни."""
        self.auth_service.clear_force_password_change(user_id)

    def set_permissions(self, role: str, module_name: str, can_read: int, can_write: int, can_delete: int):
        self.auth_service.set_permissions(role=role, module_name=module_name, can_read=can_read, can_write=can_write, can_delete=can_delete)

    def get_user_permissions(self, role: str) -> dict:
        return self.user_service.get_user_permissions(role)


    def get_client_ip(self):
        client_ip = "Unknown"
        try:
            # Спробуємо отримати IP з заголовків (це те, що Nginx передає)
            # Якщо запит не знайдено (наприклад, фоновий таск), try/except врятує
            request = app.storage.user.get('request_info')  # АБО використовуємо інший спосіб, див. нижче

            # 💡 НАДІЙНИЙ СПОСІБ ДЛЯ NICEGUI:
            # Оскільки ми в контексті клієнта, у нас є доступ до його `environ` (змінних середовища ASGI)
            if hasattr(ui.context.client, 'environ'):
                environ = ui.context.client.environ

                # Заголовки в ASGI зберігаються як список кортежів байтів (ключ, значення)
                headers = environ.get('asgi.scope', {}).get('headers', [])

                # Шукаємо 'x-forwarded-for' або 'x-real-ip'
                for name, value in headers:
                    header_name = name.decode('latin1').lower()
                    if header_name == 'x-forwarded-for':
                        # X-Forwarded-For може містити кілька IP через кому (якщо багато проксі)
                        # Беремо перший IP у списку
                        client_ip = value.decode('latin1').split(',')[0].strip()
                        break
                    elif header_name == 'x-real-ip':
                        client_ip = value.decode('latin1').strip()
                        # Не робимо break, бо x-forwarded-for має вищий пріоритет

            # Якщо заголовків від Nginx не знайшли, падаємо назад на стандартний IP
            if client_ip == "Unknown":
                client_ip = ui.context.client.ip

        except Exception as e:
            # self.log_manager.error(f"Помилка визначення IP: {e}")
            client_ip = "Unknown"
        return client_ip

    async def authenticate(self, username: str, password: str) -> Optional[dict]:
        client_ip = self.get_client_ip()

        self.log_manager.debug('🔑 Спроба залогінится: ' + str(username))
        self.audit_service.log_event(AuditLogDB(
            level=LogLevel.INFO,
            domain=EventDomain.AUTH,
            event_type=EventType.LOGIN_ATTEMPT,
            username=username,
            ip_address=client_ip,
            entity_id=None,
            action_summary="Спроба залогінится",
            details={}
        ))

        user: User = await self.auth_service.authenticate(username, password)
        if not user:
            self.log_manager.warning('🔑 Спроба невдала: ' + str(username))
            self.audit_service.log_event(AuditLogDB(
                level=LogLevel.WARNING,
                domain=EventDomain.AUTH,
                event_type=EventType.LOGIN_ATTEMPT,
                username=username,
                ip_address=client_ip,
                entity_id=None,
                action_summary="Невдала спроба",
                details={}
            ))

            return None

        # Початкові дані сесії (поки без 'authenticated': True)
        session_data = {
            'user_id': user.id,
            'user_info': {
                'username': user.username,
                'role': user.role,
                'full_name': user.full_name,
                'id': user.id,
                'session_token': user.session_token,
                'ip': client_ip
            },
            'last_activity': time.time()
        }

        if user.use_2fa:
            contact_info = user.phone or user.email
            contact_type = 'Signal' if user.phone else 'Email'
            if not contact_info:
                # Якщо 2FA увімкнено, а контактів нема — це помилка конфігурації
                raise ValueError("2FA увімкнено, але не знайдено підтвердженого контакту (Signal/Email)")
            app.storage.user.update(session_data)
            app.storage.user['authenticated'] = False
            return {
                "status": "2fa_required",
                "user": user,
                "send_to": contact_info,
                "send_type": contact_type
            }

        # Примусова зміна пароля (наприклад, після першого запуску)
        if user.force_password_change:
            app.storage.user.update(session_data)
            app.storage.user['authenticated'] = False
            return {"status": "force_password_change", "user": user}

        # 2FA ВИМКНЕНА і пароль не потребує заміни — пускаємо відразу
        session_data['authenticated'] = True
        app.storage.user.update(session_data)

        self.audit_service.log_event(AuditLogDB(
            level=LogLevel.INFO,
            domain=EventDomain.AUTH,
            event_type=EventType.LOGIN_SUCCESS,
            username=user.username,
            ip_address=client_ip,
            entity_id=None,
            action_summary="Успішний логін (без 2fa)",
            details={}
        ))

        return {"status": "success", "user": user}

    def check_session(self, ctx: RequestContext) -> bool:
        """Перевірка, чи не застаріла сесія."""
        if not app.storage.user.get('authenticated'):
            return False
        storage_time = app.storage.user.get('last_activity', 0)
        ctx_time = ctx.last_activity if ctx else 0

        last_activity = max(storage_time, ctx_time)
        user_info = app.storage.user.get('user_info', {})
        client_token = user_info.get('session_token')

        if time.time() - last_activity > config.SECURITY_SESSION_TIMEOUT:
            self.logout()
            return False

        new_now = time.time()
        app.storage.user['last_activity'] = new_now
        if ctx:
            ctx.last_activity = new_now

        user = self.user_service.get_user_by_username(user_info.get('username'))

        if not user or user.session_token != client_token:
            uname = user.username if user else user_info.get('username', '?')
            self.log_manager.warning(f"ОЙ! Токени не збігаються для користувача: {uname}!")
            self.logout()
            return False

        if not user or not user.is_active:
            self.logout()
            return False
        return True

    async def execute(self, func, ctx: RequestContext, *args, **kwargs):
        """
        Централізований запуск важких функцій у фоновому потоці
        з автоматичним менеджментом сесії.
        """
        if not self.check_session(ctx):
            return None  # Або raise PermissionError

        try:
            result = await run.io_bound(func, ctx, *args, **kwargs)

            app.storage.user['last_activity'] = time.time()
            if ctx:
                ctx.last_activity = app.storage.user['last_activity']

            return result

        except Exception as e:
            # Тут можна централізовано логувати помилки всіх звітів
            print(f"❌ Помилка при виконанні {func.__name__}: {e}")
            raise e

    def logout(self):
        """
        Інвалідує session_token у БД і очищує локальну сесію.
        Перехоплений токен стає недійсним одразу після logout,
        а не лише після закінчення таймауту.
        """

        user_info = app.storage.user.get('user_info', {})
        self.log_manager.debug(f"Logout {user_info}")
        user_id = user_info.get('id')
        if user_id:
            try:
                self.auth_service.invalidate_session_token(user_id)
            except Exception as e:
                self.log_manager.warning(f"Не вдалося інвалідувати токен для user_id={user_id}: {e}")

        try:
            # Намагаємося видалити файл сесії (стандартна поведінка NiceGUI)
            app.storage.user.clear()
        except PermissionError:
            # Якщо Windows заблокував файл (WinError 32), обходимо проблему:
            # просто видаляємо всі ключі зі словника в пам'яті.
            # Наступне збереження просто перезапише цей файл порожнім JSON-ом.
            for key in list(app.storage.user.keys()):
                app.storage.user.pop(key, None)
        except Exception as e:
            # На випадок інших непередбачуваних помилок, щоб сторінка не падала
            print(f"Попередження: не вдалося очистити storage.user: {e}")

    def has_access(self, module_name: str, action: str = PERM_READ) -> bool:
        user_info = app.storage.user.get('user_info', None)
        if not user_info:
            return False

        perms = self.get_user_permissions(user_info.get('role'))
        module_perms = perms.get(module_name, {})
        return bool(module_perms.get(action, False))

    def get_current_context(self) -> RequestContext:
        user_info = app.storage.user.get('user_info', {})
        client_ip = self.get_client_ip()
        ctx = RequestContext(
            user_name=user_info.get('full_name') or user_info.get('username') or 'Гість',
            user_role=user_info.get('role'),
            user_id=user_info.get('id'),
            user_login=user_info.get('username'),
            last_activity=app.storage.user.get('last_activity', time.time()),
            session_token=user_info.get('session_token'),
            ip_address=client_ip
        )
        return ctx


    def is_ip_blocked(self, ip: str, max_attempts=config.SECURITY_MAX_ATTEMPTS, window_seconds=300) -> bool:
        return self.auth_service.is_ip_blocked(ip, max_attempts, window_seconds)

    def register_ip_attempt(self, ip: str):
        self.log_manager.debug('🔑 Логін невірний. IP: ' + str(ip))
        return self.auth_service.register_ip_attempt(ip)

    def get_available_roles(self) -> list[str]:
        """Returns role names from the DB (falls back to hardcoded defaults on error)."""
        return self.auth_service.get_roles()

    def get_roles_full(self) -> list[dict]:
        return self.auth_service.get_roles_full()

    def add_role(self, name: str, description: str) -> tuple[bool, str]:
        return self.auth_service.add_role(name, description)

    def delete_role(self, name: str) -> tuple[bool, str]:
        return self.auth_service.delete_role(name)
