"""Inbox controller — bridges views and InboxService."""
from modules.inbox.service import InboxService
from gui.services.request_context import RequestContext
from typing import Dict, List
from gui.services.auth_manager import AuthManager
from service.processing.DocumentProcessingService import DocumentProcessingService
from service.processing.MyWorkFlow import MyWorkFlow
from service.storage.StorageFactory import StorageFactory
import io
import config


class InboxController:
    def __init__(self, workflow: MyWorkFlow, auth_manager: AuthManager):
        self.auth_manager = auth_manager
        self.workflow = workflow
        self.db = workflow.db
        self.log_manager = workflow.log_manager

    def get_user_inbox_messages(self, ctx: RequestContext) -> Dict[str, List[str]]:
        return InboxService(self.log_manager, ctx).get_user_inbox_messages()

    def download_file(self, ctx: RequestContext, filename: str, root_dir: str, is_personal: bool) -> io.BytesIO:
        service = InboxService(self.log_manager, ctx)
        return service.download_file(ctx.user_login if is_personal else None, filename, root_dir)

    def assign_file(self, ctx: RequestContext, filename: str, is_personal: bool, target_username: str, source_folder=None):
        service = InboxService(self.log_manager, ctx)
        source_user = ctx.user_login if is_personal else None
        service.assign_file(source_user, filename, target_username, source_folder)

    def delete_file(self, ctx: RequestContext, user_login: str, folder: str, filename: str):
        InboxService(self.log_manager, ctx).delete_file(user_login, folder, filename)

    def upload_root_file(self, ctx: RequestContext, filename: str, file_data: bytes):
        InboxService(self.log_manager, ctx).upload_file_to_root(filename, file_data)

    def archive_file(self, ctx, personal_folder: str, filename: str) -> bool:
        client = StorageFactory.create_client(config.INBOX_DIR_PATH, self.log_manager)
        folder_str = f"{client.get_separator()}{personal_folder}" if personal_folder else ''
        source_file = f"{config.INBOX_DIR_PATH}{folder_str}{client.get_separator()}{filename}"
        dservice = DocumentProcessingService(self.log_manager)
        return dservice.archive_document(source_file, filename) is not None
