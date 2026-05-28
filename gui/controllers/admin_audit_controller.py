from typing import List

from domain.audit_log_filter import AuditLogFilter
from domain.db.AuditLogDB import AuditLogDB
from gui.services.auth_manager import AuthManager
from gui.services.request_context import RequestContext
from service.processing.MyWorkFlow import MyWorkFlow

class AdminAuditController:
    def __init__(self, workflow: MyWorkFlow, auth_manager: AuthManager):
        self.log_manager = workflow.log_manager
        self.auth_manager = auth_manager
        self.audit_service = workflow.audit_log_service

    def search_logs(self, ctx: RequestContext, filters: AuditLogFilter) -> List[AuditLogDB]:
        self.log_manager.debug(f"UI:{ctx.user_name}: Запит системних логів.")
        return self.audit_service.search_logs(filters)

    def count_logs(self, filters: AuditLogFilter):
        return self.audit_service.count_logs(filters)

