from dics.deserter_xls_dic import REGEX_ANSWERS
from service.admin.AuditLogService import AuditLogService
from service.connection.EmailClient import EmailClient
from service.connection.SignalClient import SignalClient
from service.processing.workflow.AttachmentHandler import AttachmentHandler
from service.connection.MyDataBase import MyDataBase
import traceback

from service.processing.workflow.SignalBotHandler import SignalBotHandler
from service.storage.LoggerManager import LoggerManager
from service.storage.BackupData import BackupData
from service.users.AuthService import AuthService
from service.users.UserService import UserService
import regex as re

class MyWorkFlow:

    def __init__(self, db: MyDataBase = None):
        self.log_manager = LoggerManager()
        self.attachmentHandler:AttachmentHandler = None
        self.signalClient:SignalClient = SignalClient()
        self.emailClient:EmailClient = EmailClient()
        self.db: MyDataBase = db if db is not None else MyDataBase()
        self.audit_log_service: AuditLogService = None
        self.user_service = None
        self.auth_service = None

        self.backuper = BackupData(self.log_manager)
        self._bot_handler: SignalBotHandler = None

    def initWorkflow(self):
        self.user_service = UserService(self.db, self.signalClient, self.emailClient)
        self.auth_service = AuthService(self.db, self.user_service)

        self.audit_log_service = AuditLogService(self.db)

        self._bot_handler = SignalBotHandler(
            user_service=self.user_service,
            log_manager=self.log_manager,
            db=self.db
        )
        self.user_service.init_user_folders()
        self.audit_log_service.clear_old_logs()

    async def parseSignalData(self, data: dict):
        """Розбирає JSON-RPC пакет від Signal та запускає відповідну логіку."""
        try:
            params = data.get("params", {})
            envelope = params.get("envelope", {})

            if "dataMessage" in envelope:
                msg = envelope["dataMessage"]
                source = (envelope.get("source")
                          or envelope.get("sourceNumber")
                          or "Невідомий")
                source_uuid = envelope.get("sourceUuid")
                timestamp = msg.get("timestamp")
                group_info = msg.get("groupInfo")
                group_id = group_info.get("groupId") if group_info else None
                message_text = msg.get("message", "")
                attachments = msg.get("attachments", [])
                if attachments:
                    self._handle_attachments(attachments, group_id, source, source_uuid, timestamp)
                if message_text:
                    await self._handle_text_message(source, group_id, message_text)


            elif "syncMessage" in envelope:
                sync_msg = envelope["syncMessage"]
                if "sentMessage" in sync_msg:
                    sent = sync_msg["sentMessage"]
                    dest = (sent.get("destinationNumber")
                            or sent.get("destinationUuid")
                            or "когось")
                    text = sent.get("message", "")
                    if text:
                        return f"📤 ВИ НАПИСАЛИ до {dest}: {text}"

        except Exception as e:
            self.log_manager.debug("--- ПОВНИЙ СТЕК ПОМИЛКИ ---")
            self.log_manager.debug(traceback.format_exc())
            return f"❌ Помилка парсингу: {e}"

        return None

    async def _handle_text_message(self, source: str, group_id, message_text: str) -> None:
        """Обробляє вхідне текстове повідомлення."""
        if group_id is not None:
            self.log_manager.debug(f"🔇 Ігнорую текст з групи {group_id} від {source}.")
            return

        normalized = message_text.lower().strip()

        # Швидкі відповіді без авторизації (привітання тощо)
        for pattern, responses in REGEX_ANSWERS:
            if re.search(pattern, normalized):
                import random
                response = random.choice(responses)
                self.signalClient.send_message(source, response)
                return
        # Повна обробка з авторизацією та стейт-машиною
        if self._bot_handler is None:
            self.log_manager.warning("Signal-бот: _bot_handler не ініціалізовано")
            response = "⚠️ Система ще не готова. Спробуйте пізніше."
        else:
            response = await self._bot_handler.handle(source, message_text)

        self.log_manager.debug(f"🤖 Відповідаю {source}: {response[:60]}...")

        # Відповідаємо тільки в особистих повідомленнях, не в групах
        if group_id is None and response:
            self.signalClient.send_message(source, response)


    def _handle_attachments(self, attachments: list, group_id, source: str, source_uuid, timestamp) -> None:
        """Обробляє вхідні вкладення."""
        self.log_manager.debug("--- ПОЧАТОК ОБРОБКИ ВКЛАДЕНЬ ---")
        for att in attachments:
            att_id   = att.get("id")
            filename = att.get("filename")
            self.log_manager.debug(f"📎 Отримано файл: {filename} (ID: {att_id})")

            handler = AttachmentHandler(self)
            messages = handler.handle_attachment(att_id, filename)

            emoji = "➕" if len(messages) == 0 else "⚠️"
            #self.signalClient.send_reaction(
            #    group_id, source, emoji, source_uuid, timestamp
            #)
        self.log_manager.debug("--- КІНЕЦЬ ОБРОБКИ ВКЛАДЕНЬ ---")