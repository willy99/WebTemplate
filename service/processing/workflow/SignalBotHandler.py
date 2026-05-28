"""
SignalBotHandler
================
Обробляє вхідні текстові повідомлення від Signal-бота.
Відповідає за:
  - перевірку авторизації відправника (тільки верифіковані 2FA-користувачі)
  - стейт-машину меню
  - формування текстових відповідей і звітів

Навмисно НЕ знає про:
  - SignalClient (не відправляє сам — повертає текст, викликач відправляє)
  - ExcelProcessor напряму (звертається через ExcelReporter)
  - MyWorkFlow (отримує залежності через __init__)
"""

from datetime import date
from typing import Optional
from domain.user import User
from service.connection.MyDataBase import MyDataBase
from service.users.UserService import UserService
from service.storage.LoggerManager import LoggerManager
import html

class SignalBotHandler:

    # ------------------------------------------------------------------
    # Константи меню
    # ------------------------------------------------------------------
    _MAIN_MENU  = (
        "Головне меню:\n"
        "1. Операції з файлами\n"
        "2. Статистика і звіти\n"
        "0. Вихід\n"
        "пошук ПІБ - шукає інформацію за введеними даними\n"
        "щоденний за dd.mm.YYYY - щоденний звіт за дату"

    )
    _PROCESS_MENU = (
        "Операції:\n"
        "1. Batch-обробка файлів\n"
        "2. Конвертація полів\n"
        "0. Назад"
    )
    _STAT_MENU = (
        "Статистика і звіти:\n"
        "1. Щоденний зведений звіт (сьогодні)\n"
        "0. Назад"
    )
    _MENU_PROMPT = ("Напишіть 'меню' для початку роботи.\n"
        "пошук ПІБ - шукає інформацію за введеними даними\n"
        "щоденний за dd.mm.YYYY - щоденний звіт за дату"
    )

    def __init__(
        self,
        user_service: UserService,
        log_manager: LoggerManager,
        db: MyDataBase
    ):
        self.user_service  = user_service
        self.log_manager   = log_manager

    # ------------------------------------------------------------------
    # Авторизація
    # ------------------------------------------------------------------

    def authorize(self, phone_number: str) -> Optional[object]:
        """
        Повертає User якщо номер верифіковано через 2FA,
        або None якщо доступ заборонено.
        Не повідомляє зловмисника про причину відмови.
        """
        user = self.user_service.get_user_by_phone(phone_number)
        if user:
            self.log_manager.debug(
                f" ✅ Signal-бот: авторизація OK — {user.username} ({phone_number[-4:]}****)"
            )
        else:
            self.log_manager.warning(
                f" ❌ Signal-бот: СПРОБА ДОСТУПУ від незнайомого номера {phone_number}"
            )
        return user

    # ------------------------------------------------------------------
    # Основний обробник
    # ------------------------------------------------------------------

    async def handle(self, phone_number: str, text: str) -> str:
        """
        Головний метод: перевіряє авторизацію і повертає текстову відповідь.
        Нічого не відправляє сам — відправка залишається у MyWorkFlow.

        Returns:
            Рядок-відповідь або None якщо відповідати не треба.
        """
        # 1. Перевірка авторизації
        user:User = self.authorize(phone_number)
        if not user:
            return "❌ Доступ заборонено. Ваш номер не верифіковано в системі."

        # 2. Швидкі відповіді (не залежать від стану)
        normalized = text.lower().strip()
        if normalized in ("привіт", "hello", "hi"):
            return f"Привіт, {user.full_name or user.username}! Напишіть 'меню' для роботи."

        # 3. Стейт-машина
        return await self._process_state(phone_number, normalized)

    # ------------------------------------------------------------------
    # Стейт-машина
    # ------------------------------------------------------------------

    async def _process_state(self, phone_number: str, text: str) -> str:
        state = self.user_service.get_user_state(phone_number)
        self.log_manager.debug('>>>> text from signal ' + str(html.escape(text)))

        # Глобальна команда — скидання в меню
        if text in ("меню", "start", "menu", "/start"):
            self.user_service.set_user_state(phone_number, "MAIN_MENU")
            return self._MAIN_MENU

        if state == "MAIN_MENU":
            return self._handle_main_menu(phone_number, text)

        elif state == "PROCESS":
            return self._handle_process_menu(phone_number, text)

        elif state == "STAT":
            return self._handle_stat_menu(phone_number, text)

        # Невідомий стан або START
        return self._MENU_PROMPT

    def _handle_main_menu(self, phone_number: str, text: str) -> str:
        if text == "1":
            self.user_service.set_user_state(phone_number, "PROCESS")
            return self._PROCESS_MENU
        if text == "2":
            self.user_service.set_user_state(phone_number, "STAT")
            return self._STAT_MENU
        if text in ("0", "вихід"):
            self.user_service.set_user_state(phone_number, "START")
            return self._MENU_PROMPT
        return self._MAIN_MENU

    def _handle_process_menu(self, phone_number: str, text: str) -> str:
        if text == "0":
            self.user_service.set_user_state(phone_number, "MAIN_MENU")
            return self._MAIN_MENU
        return ''

    def _handle_stat_menu(self, phone_number: str, text: str) -> str:
        if text == "0":
            self.user_service.set_user_state(phone_number, "MAIN_MENU")
            return self._MAIN_MENU
        return self._STAT_MENU


    @staticmethod
    def _format_awol_line(num: int, r: dict) -> str:
        """Форматує один рядок нового СЗЧ для Signal-повідомлення."""
        name = r.get('name', '—')
        title = r.get('title', '—')
        subunit = r.get('subunit', '—')
        des_dt = r.get('des_date', '—')
        locality = r.get('desertion_locality') or r.get('desertion_place') or '—'
        return (
            f"  {num}. {title} {name}\n"
            f"     {subunit}\n"
            f"     СЗЧ: {des_dt} | {locality}"
        )


