from nicegui import ui, run

from i18n import t
from service.connection.AnthropicClient import AnthropicClient, CHAT_SYSTEM_PROMPT


def render_chat_page():
    client = AnthropicClient(system_prompt=CHAT_SYSTEM_PROMPT)

    with ui.column().classes('w-full max-w-3xl mx-auto px-4 py-4 gap-3').style('height: calc(100vh - 72px); display: flex; flex-direction: column;'):

        ui.label(t('chat.title')).classes('text-2xl font-bold text-slate-800 shrink-0')

        chat_scroll = ui.scroll_area().classes('flex-1 border border-gray-200 rounded-xl bg-gray-50').style('min-height: 0;')

        with chat_scroll:
            messages_col = ui.column().classes('w-full gap-3 p-3')

        with ui.row().classes('w-full gap-2 items-center shrink-0'):
            msg_input = ui.input(placeholder=t('chat.placeholder')) \
                .classes('flex-1').props('outlined dense')
            send_btn = ui.button(icon='send').props('color=primary round')

        async def send():
            text = msg_input.value.strip()
            if not text:
                return

            msg_input.value = ''
            msg_input.disable()
            send_btn.disable()

            with messages_col:
                with ui.row().classes('w-full justify-end'):
                    ui.label(text).classes(
                        'bg-blue-500 text-white rounded-2xl px-4 py-2 text-sm max-w-[75%] whitespace-pre-wrap'
                    )

            with messages_col:
                with ui.row().classes('w-full justify-start') as thinking_row:
                    ui.spinner('dots', size='sm').classes('text-gray-400')

            chat_scroll.scroll_to(percent=1.0)

            try:
                reply = await run.io_bound(client.chat_with_tools, text)
            except Exception as exc:
                reply = t('chat.error', error=exc)

            thinking_row.delete()

            with messages_col:
                with ui.row().classes('w-full justify-start'):
                    with ui.card().classes('max-w-[80%] shadow-sm bg-white rounded-2xl px-1 py-1'):
                        ui.markdown(reply).classes('text-sm')

            chat_scroll.scroll_to(percent=1.0)
            msg_input.enable()
            send_btn.enable()
            msg_input.run_method('focus')

        msg_input.on('keydown.enter', send)
        send_btn.on_click(send)
