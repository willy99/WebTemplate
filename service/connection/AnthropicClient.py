import json
from datetime import datetime

from anthropic import Anthropic
from anthropic.types import Message
import config

MILITARY_SYSTEM_PROMPT = """Ти — AI-асистент у системі обліку самовільно залишивших частину (СЗЧ) \
та інших порушень дисципліни у військовій частині ЗСУ.

Мова спілкування: УКРАЇНСЬКА. Але якщо питають англійською, відповідай Англійською.

Контекст:
- Ти спілкуєшся з офіцерами та персоналом через месенджер Signal.
- Допомагаєш з питаннями, що не охоплені командним меню бота: роз'яснення процедур, \
правові питання, загальні запити.
- До системи вже вбудовано: пошук особового складу, щоденні звіти по СЗЧ, \
batch-обробка документів.

Стиль відповідей:
- Відповідай лаконічно, по суті, без зайвої води.
- Де доречно — додай трохи армійського гумору та жаргону: \
"4.5.0" замість "все добре", "сракопад" для опису хаосу, \
"зберись" для підбадьорення, "тихої ночі" на прощання, \
"я на зв'язку" / "слухаю уважно", "панове" у зверненні тощо.
- Гумор — лише де справді пасує. На серйозні питання відповідай серйозно.
- Ніколи не вигадуй юридичні норми або накази — якщо не знаєш точно, скажи про це чесно.
"""

CHAT_SYSTEM_PROMPT = """You are a helpful AI assistant built into a web application.
Answer clearly and concisely. Use markdown formatting when appropriate.
You have access to tools — use them when they would genuinely help answer the user's question.
"""

TOOLS = [
    {
        "name": "get_current_time",
        "description": "Returns the exact current date and time on the server.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    }
]


class AnthropicClient:

    def __init__(self, system_prompt: str | None = None):
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = config.AI_CLAUDE_MODEL
        self.system_prompt = system_prompt if system_prompt is not None else MILITARY_SYSTEM_PROMPT
        self.user_messages = []

    def add_user_message(self, text: str):
        self.user_messages.append({"role": "user", "content": text})

    def add_assistant_message(self, text: str):
        self.user_messages.append({"role": "assistant", "content": text})

    def chat(self, question: str) -> str:
        self.add_user_message(question)
        message: Message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=self.system_prompt,
            messages=self.user_messages
        )
        answer = message.content[0].text
        self.add_assistant_message(answer)
        return answer

    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        if tool_name == "get_current_time":
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Unknown tool: {tool_name}"

    def chat_with_tools(self, question: str) -> str:
        self.add_user_message(question)

        while True:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.system_prompt,
                tools=TOOLS,
                messages=self.user_messages,
            )

            if response.stop_reason == "tool_use":
                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = self._execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        })

                self.user_messages.append({"role": "assistant", "content": response.content})
                self.user_messages.append({"role": "user", "content": tool_results})

            else:
                answer = "".join(block.text for block in response.content if hasattr(block, "text"))
                self.add_assistant_message(answer)
                return answer
