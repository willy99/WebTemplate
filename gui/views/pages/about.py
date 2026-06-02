import asyncio
from nicegui import ui


async def about_page():
    # Задаємо базові стилі для body сторінки
    ui.query('body').style('background-color: #111; font-family: "Courier New", Courier, monospace; margin: 0; padding: 0; overflow-x: hidden;')

    raw_content = (
        "=== SYSTEM ACCESS GRANTED ===\\n"
        "PROJECT   : Web Template\\n\\t"
        "BUILT     : (С) 2026. На колінці\\n"
        "TECHNOLOGY: Python / NiceGUI\\t / Cyber Security\\n"
        "ASSIGNMENT: Веб проект-шаблон для бізнес задач\\n"
        "MISSION   : Фортеця для даних. \\tШвидка інтелектуальна обробка. \\tПаперово-табличне пекло - в сміття!\\n"
        "-----------------------------------------\\n\\n"
        "DEVELOPER : 👨‍🦱Papashon\\n"        
        "EMAIL     : willy2005@gmail.com\\n"
        "SIGNAL    : +38 093 \\tXXX XX X1\\n"
        "ADDRESS   : << ACCESS DENIED >>\\n"
        "-----------------------------------------\\n\\n"
        "STATUS    : Модернізація фасаду Nginx завершена успішно.\\n\\t"
        "Очікування ТЗ на нові звіти, що потрібні ще на позавчора.\\n\\n"
        "\\t\\t\\tПитання є?\\t\\t Питань немає!\\n"
    )

    # Використовуємо адаптивну верстку: на десктопах рядок (row), на мобілках — стовпчик (column)
    ui.html('''
            <style>
                /* Головний контейнер: за замовчуванням для великих екранів */
                .about-container {
                    display: flex;
                    flex-direction: row;
                    flex-wrap: nowrap;
                    align-items: center;
                    justify-content: center;
                    width: 100vw;
                    height: 90vh;
                    padding: 2rem;
                    box-sizing: border-box;
                }
                .left-block {
                    width: 50%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 1.5rem;
                    box-sizing: border-box;
                }
                .right-block {
                    width: 50%;
                    height: 80vh;
                    min-width: 300px;
                    border-radius: 0.75rem;
                    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
                    overflow: hidden;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 1rem;
                    box-sizing: border-box;
                }

                /* МЕДІА-ЗАПИТ: Якщо екран менший за 768px (планшети та телефони) */
                @media (max-width: 768px) {
                    .about-container {
                        flex-direction: column; /* Перемикаємо в режим стовпчика */
                        height: auto;           /* Звільняємо висоту, щоб контент не тиснувся */
                        padding: 1rem;
                        overflow-y: auto;       /* Дозволяємо вертикальний скрол */
                    }
                    .left-block {
                        width: 100%;            /* Текст займає всю ширину */
                        height: auto;
                        padding: 0.5rem;
                        margin-bottom: 2rem;    /* Відступ перед 3D моделькою */
                    }
                    .right-block {
                        width: 100%;            /* 3D канвас падає вниз і стає на всю ширину */
                        height: 50vh;           /* Обмежуємо висоту на мобілці, щоб не займав весь екран */
                        min-height: 300px;
                    }
                }
            </style>

            <div class="about-container">

                <!-- Лівий блок: Текст -->
                <div class="left-block">
                    <div id="hacker-text" style="font-size: 1.2rem; color: #4ade80; line-height: 1.6; white-space: pre-wrap; font-family: monospace; width: 100%;"></div>
                </div>

                <!-- Правий блок: 3D канвас (на мобілці забігає під текст) -->
                <div class="right-block">
                    <div id="3d-canvas" style="width: 100%; height: 100%; position: relative;"></div>
                </div>

            </div>
        ''', sanitize=False)

    # Невелика пауза, щоб браузер встиг зарендерити наш HTML-рядок
    await asyncio.sleep(0.3)

    # Викликаємо скрипт (піднімаємо версію до v=1.0.6)
    await ui.run_javascript(f'''
        import('/static/about_effects.js?v=1.0.20')
            .then(module => {{
                console.log('>>> Модуль v1.0.6 успішно імпортовано. Запуск функцій...');
                module.initTypewriter(`{raw_content}`);
                module.init3DCanvas();
            }})
            .catch(err => console.error("Помилка динамічного імпорту:", err));
    ''', timeout=5.0)