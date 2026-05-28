from domain.db.AuditLogDB import *
from gui.services.auth_manager import AuthManager
from gui.services.request_context import RequestContext
from service.processing.MyWorkFlow import MyWorkFlow


class AuditController:
    def __init__(self, workflow: MyWorkFlow, auth_manager: AuthManager):
        self.log_manager = workflow.log_manager
        self.auth_manager = auth_manager
        self.audit_service = workflow.audit_log_service


    def add_audit_entry(self, ctx: RequestContext, domain: EventDomain, level: LogLevel, event_type: EventType, message: str, event_id: int = None, details:dict = {}):
        self.audit_service.log_event(AuditLogDB(
            level=level,
            domain=domain,
            event_type=event_type,
            username=ctx.user_login,
            ip_address=ctx.ip_address,
            entity_id=event_id,
            action_summary=message,
            details=details
        ))


