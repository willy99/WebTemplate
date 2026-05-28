from typing import List

from domain.db.AuditLogDB import *
from domain.sys_config import SysConfig
from gui.services.auth_manager import AuthManager
from service.config.ConfigService import ConfigService
from gui.services.request_context import RequestContext
from service.processing.MyWorkFlow import MyWorkFlow

class ConfigController:
    def __init__(self, workflow: MyWorkFlow, auth_manager: AuthManager):
        self.log_manager = workflow.log_manager
        self.auth_manager = auth_manager
        self.cfg_service = ConfigService(workflow.db)
        self.audit_service = workflow.audit_log_service

    def get_all_configs(self, ctx: RequestContext) -> List[SysConfig]:
        """Отримує всі налаштування з бази"""
        # 💡 Тут можна додати перевірку: if not ctx.is_admin: raise Exception(...)
        self.log_manager.debug(f"UI:{ctx.user_name}: Запит системних налаштувань.")
        self.audit_service.log_event(AuditLogDB(
            level=LogLevel.INFO,
            domain=EventDomain.SYSTEM,
            event_type=EventType.GET,
            username=ctx.user_login,
            ip_address=ctx.ip_address,
            entity_id=None,
            action_summary="Запит системних налаштувань.",
            details={}
        ))

        return self.cfg_service.get_all()

    def update_config_value(self, ctx: RequestContext, key_name: str, new_value: str) -> bool:
        """Оновлює значення та логує цю дію"""
        self.log_manager.info(f"⚠️ UI:{ctx.user_name}: Змінює налаштування [{key_name}] на [{new_value}]")
        self.audit_service.log_event(AuditLogDB(
            level=LogLevel.INFO,
            domain=EventDomain.SYSTEM,
            event_type=EventType.UPDATE,
            username=ctx.user_login,
            ip_address=ctx.ip_address,
            entity_id=None,
            action_summary="Змінюються налаштування",
            details={"keyname":key_name, "value":new_value}
        ))

        return self.cfg_service.update_value(key_name, new_value)

    def apply_configs_to_runtime(self, ctx: RequestContext):
        """Застосовує зміни в пам'ять"""
        self.log_manager.info(f"🔄 UI:{ctx.user_name}: Застосовує нові налаштування системи в config.py")
        self.audit_service.log_event(AuditLogDB(
            level=LogLevel.INFO,
            domain=EventDomain.SYSTEM,
            event_type=EventType.UPDATE,
            username=ctx.user_login,
            ip_address=ctx.ip_address,
            entity_id=None,
            action_summary="Застосовує нові налаштування системи в config.py",
            details={}
        ))

        self.cfg_service.apply_to_runtime()