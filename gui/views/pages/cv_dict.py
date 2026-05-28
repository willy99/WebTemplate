CV_CATEGORIES_DATA = {
    'en': [
        {"id": "exp", "label": "Experience", "icon": "work_history", "color": "primary"},
        {"id": "proj", "label": "Projects", "icon": "code", "color": "secondary"},
        {"id": "skills", "label": "Skills (Stack)", "icon": "terminal", "color": "accent"},
        {"id": "edu", "label": "Education", "icon": "school", "color": "positive"},
        {"id": "lang", "label": "Languages", "icon": "language", "color": "info"},
        {"id": "hobby", "label": "Hobbies", "icon": "sports_esports", "color": "warning"},
        {"id": "contact", "label": "Contacts", "icon": "perm_contact_calendar", "color": "negative"},
    ],
    'uk': [
        {"id": "exp", "label": "Досвід роботи", "icon": "work_history", "color": "primary"},
        {"id": "proj", "label": "Проекти", "icon": "code", "color": "secondary"},
        {"id": "skills", "label": "Навички (Стек)", "icon": "terminal", "color": "accent"},
        {"id": "edu", "label": "Освіта", "icon": "school", "color": "positive"},
        {"id": "lang", "label": "Мови", "icon": "language", "color": "info"},
        {"id": "hobby", "label": "Хоббі", "icon": "sports_esports", "color": "warning"},
        {"id": "contact", "label": "Контакти", "icon": "perm_contact_calendar", "color": "negative"},
    ]
}

CV_ABOUT_DATA = {
    'en': {
        'title': 'About Me',
        'born': 'Born on 24th November, 1979, in Odessa, Ukraine.',
        'about': 'Highly motivated and responsible person, considering every problem as a task that can be solved. Looking for some fun and challenge, working in a creative team in an agile style, where I could learn something new.',
        'credo': 'Credo: public class PavelZhelnov implements TalentsFromGod!',
        'aims': 'Aims: Problem solving (finding bottlenecks, performance problems, refactoring, suggesting more optimized solutions etc). Interest in creating projects on Java, using stable frameworks with a good track record mixed with experimental ones.',
        'approach': 'Usually find useful resources like StackOverflow to get proper and quick solutions for puzzles in any unfamiliar area.'
    },
    'uk': {
        'title': 'Про мене',
        'born': 'Зроблено: 24 листопада 1979 року в Одесі, Україна.',
        'about': 'Високомотивована та відповідальна людина, що розглядає кожну проблему як завдання, яке можна вирішити. Шукаю виклики, працюючи в креативній команді за методологією Agile, де можна постійно навчатися чомусь новому.',
        'credo': 'Кредо: Рухатися вперед і робити все краще!',
        'aims': 'Цілі: Вирішення проблем (пошук вузьких місць, оптимізація продуктивності, рефакторинг, впровадження ефективних рішень). Цікавлюся створенням проектів на Java, поєднуючи стабільні фреймворки з перевіреною репутацією та елементами експериментальних рішень.',
        'approach': 'Завжди знаходжу корисні ресурси, як-от StackOverflow, щоб отримати швидкі та правильні рішення для задач у будь-якій незнайомій галузі.'
    }
}

CV_CONTACT_DATA = {
    'en': {
        'address': '38 Sakharova st, Odessa, 65123, Ukraine',
        'phone': '+38 (093) 851 32 01',
        'email': 'willy2005@gmail.com',
        'linkedin': 'https://www.linkedin.com/in/pavel-zhelnov-69386864/',
        'labels': {
            'title': 'Contact Info', 'address': 'Address', 'phone': 'Phone', 'email': 'Email'
        }
    },
    'uk': {
        'address': 'Вул. Сахарова 38, 65123, Одеса, Україна',
        'phone': '+38 (093) 851 32 01',
        'email': 'willy2005@gmail.com',
        'linkedin': 'https://www.linkedin.com/profile/view?id=229064655',
        'labels': {
            'title': 'Контакти', 'address': 'Адреса', 'phone': 'Телефон', 'email': 'Email'
        }
    }
}

# Словник з даними про освіту
CV_EDU_DATA = {
    'en': {
        'title': 'Education',
        'period': '1996 - 2001',
        'uni': 'Odessa National University of I. I. Mechnikov',
        'faculty': 'Faculty: Information technology',
        'specialty': 'Specialty: Protection of information in computer networks',
        'degree': 'Degree: Specialist (2001)'
    },
    'uk': {
        'title': 'Освіта',
        'period': '1996 - 2001',
        'uni': 'Одеський Національний Університет ім. І. І. Мечникова',
        'faculty': 'Факультет: Інформаційних технологій',
        'specialty': 'Фах: Захист інформації в комп\'ютерних мережах',
        'degree': 'Ступінь: Спеціаліст (2001)'
    }
}


CV_PROJECTS_DATA = {
    'en': [
        {
            'id': 'runaway',
            'title': 'Runaway',
            'role': 'Full-stack Dev',
            'date': 'Feb 2026 - Present',
            'description': 'The service for military data',
            'details': 'It is a powerful analytic tool to gather accounting information about mil-unit staff, represent charts and helps organize work\n'
                       "- A bot monitors signal groups and retrieve messages with attachments\n"
                       "- Retrieve necessary part of information from incoming attachments and make appropriate flow\n"
                       "- Sync data from excel to a database\n"
                       "- Represent current state in many reports and charts.\n"
                       "- Filecacher, indexing 100k+ files to search information on a hot-spot.\n"
                       "- Notify with alerts about scheduled tasks.\n",
            'icon': '/static/images/cv/runaway.png'
        },
        {
            'id': 'artinlog',
            'title': 'Artinlog',
            'role': 'Java Dev',
            'date': 'Jul 2017 - Present',
            'description': 'Logistics in Ukraine, tracking, calculators, flex database',
            'details': 'We\'ve got this project together with my companion, when AI has not yet been started. \n'
                       "- The math formulas has been involved to calculate the placement of goods in containers\n"
                       "- There is 3d representation of calculation\n"
                       "- Flex database.\n"
                       "- Also mobile app has been developed. To communicate REST API is provided.\n",
            'icon': '/static/images/cv/artinlog.svg'
        },
        {
            'id': 'gpm',
            'title': 'GPM',
            'role': 'Apex Developer',
            'date': 'Jul 2017 - Present',
            'description': 'At ModelN, Salesforce platform focus. Apex, Javascript, Python and Heroku management.',
            'details': 'Yes, Java is perfect, but sometimes we need to step out of comfort zone. Ideally - with Salesforce platform. Apex, Javascript, Python and Heroku management, - the Big Four I need to deal now with. And that\'s really a challenge!\n'
                " The major responsibilities were in the following areas:\n"
                "- Data export to EXCEL format. As Apex supports only csv, we should use customized version of a third-party js library, followed by fixing its own bugs.\n"
                "- Competitor Module implementation from scratch. That was a time, I learned the basics of react.\n"
                "- GPI integration - the prices are coming from a vendor, which sends them in a huge json blocks. The process was divided into pieces - updating/creating competitor products, indications, external prices and cost of treatments. As APEX has a lot of governor limits, we still managed the issue with handling pieces in a sequential batches. Each could process files up to 10 Mb because of special implementation of a JSON parsing.\n" 
                "- Applying a custom formula calculation engine into GLE (Global Launch Excellene) area (python implementation)\n"
                "And many more...\n",
            'icon': '/static/images/cv/gpm.jpeg'
        },
        {
            'id': 'mens',
            'title': 'Men\'s Wearhouse',
            'role': 'Senior Java Developer',
            'date': 'Jan 2016 - Jul 2017',
            'description': 'Men\'s Wearhouse is one of the largest specialty retailers of men\'s apparel and formalwear in the United States.',
            'details': 'That\'s the project of my dream: plenty of places to refactor, no tests, but smart technologies which allow to take control over and knuckle down to it! Everyday scrums, supportive team and creative tasks - keep me in a good shape. Used technologies: Backend: Java, Hibernate, RESTfull services, Oracle; UI: AngularJS, JQuery;',
            'icon': '/static/images/cv/mens.jpeg'
        },
        {
            'id': 'selectica',
            'title': 'Selectica',
            'role': 'Senior Java Developer',
            'date': 'Sep 2014 - Jan 2016',
            'description': 'Selectica is a contract lifecycle management application.',
            'details': 'I got the position when the refactoring was in the progress, so immediately started diving deeply into Spring framework. Particularly – Spring Security (implemented login/logout feature), MVC – the application is built using REST. Used technologies: Backend: Java, Spring, Oracle, QueryDSL; UI: Ajax, Backbone; JBoss application server.',
            'icon': '/static/images/cv/selectica.jpeg'
        },
        {
            'id': 'tis',
            'title': 'TIS',
            'role': 'Senior Java Developer, Tech Lead',
            'date': 'Feb 2010 - Sep 2014',
            'description': 'TIS is a banking platform to help customers to communicate with banks',
            'details': 'Because of a heterogeneous infrastructure and multiple protocols, it’s really hard to maintain all the payment transactions, track the liquidity, control the balance of bank accounts ets. TIS provides the solution. Main customers are Hugo Boss, Fujitsu, BWM, Swiss etc. (http://www.tis.biz/en/customers/)',
            'icon': '/static/images/cv/tis.jpeg'
        },
        {
            'id': 'srp',
            'title': 'Shared Royalty Platform',
            'role': 'Jr Java Developer',
            'date': 'Jan 2006 - Jan 2010',
            'description': 'Shared Royalty Platform was the project that helped to calculate the royalties and commission from sales in music industry',
            'details': 'There were nearly 9 domains, separated from each other and interacting by gate interfaces – contract, sales, product, subledger, security, workflow, etc. The key role in this project had been accomplished in Subledger area, where accounting calculations, month-end process took place. The project had many technologies wrapped by exigen frameworks that helped to use them in a more convenient way, but cut some features. Also it held away developers from using the original technologies. Mastered some design patterns, unit testing (JUnit), functional testing (used exigen framework), Oracle PL/SQL and got an amazing experience in cooperative work in a big distributed team. Participated in meetings, seminars. Has improved English knowledge to upper-intermediate level.',
            'icon': '/static/images/cv/exigen.jpeg'
        }

    ],

'uk': [
    {
        'id': 'runaway',
        'title': 'Runaway',
        'role': 'Full-stack Розробник',
        'date': 'Лют 2026 - Теперішній час',
        'description': 'Сервіс для роботи з військовими даними',
        'details': 'Це потужний аналітичний інструмент для збору облікової інформації про особовий склад, побудови графіків та організації роботи.\n'
                   "- Бот моніторить групи в Signal та завантажує повідомлення з вкладеннями.\n"
                   "- Вилучення необхідної інформації з вхідних файлів та її подальша маршрутизація.\n"
                   "- Синхронізація даних з Excel до бази даних.\n"
                   "- Відображення поточного стану у вигляді різноманітних звітів та графіків.\n"
                   "- Filecacher: індексування понад 100 тисяч файлів для миттєвого пошуку інформації.\n"
                   "- Сповіщення та алерти про заплановані завдання.\n",
        'icon': '/static/images/cv/runaway.png'
    },
    {
        'id': 'artinlog',
        'title': 'Artinlog',
        'role': 'Java Розробник',
        'date': 'Лип 2017 - Теперішній час',
        'description': 'Логістика в Україні, трекінг, калькулятори, гнучка база даних',
        'details': 'Ми розпочали цей проект разом з моїм партнером ще до того, як ШІ став мейнстрімом. \n'
                   "- Використання математичних формул для розрахунку розміщення товарів у контейнерах.\n"
                   "- 3D-візуалізація розрахунків.\n"
                   "- База даних по флексам.\n"
                   "- Також розроблено мобільний додаток. Для комунікації реалізовано REST API.\n",
        'icon': '/static/images/cv/artinlog.svg'
    },
    {
        'id': 'gpm',
        'title': 'GPM',
        'role': 'Apex Розробник',
        'date': 'Лип 2017 - Теперішній час',
        'description': 'Робота в ModelN, фокус на платформі Salesforce. Apex, Javascript, Python та управління Heroku.',
        'details': 'Так, Java — це чудово, але іноді потрібно виходити із зони комфорту. В ідеалі — з платформою Salesforce. Apex, Javascript, Python та Heroku — це "Велика Четвірка", з якою я зараз працюю. І це справжній виклик!\n'
            " Основні обов'язки у таких сферах:\n"
            "- Експорт даних у формат EXCEL. Оскільки Apex підтримує лише csv, ми використовували кастомізовану версію сторонньої js-бібліотеки, паралельно виправляючи її баги.\n"
            "- Розробка модуля Competitor з нуля. Саме тоді я вивчив основи React.\n"
            "- Інтеграція GPI: ціни надходять від постачальника у величезних JSON-блоках. Процес було розділено на частини — оновлення/створення продуктів конкурентів, показань, зовнішніх цін та вартості лікування. Через велику кількість лімітів (governor limits) в Apex, ми вирішили цю проблему шляхом послідовної обробки частин у батчах. Кожен з них міг обробляти файли до 10 МБ завдяки спеціальній реалізації парсингу JSON.\n" 
            "- Впровадження кастомного рушія для розрахунку формул у сфері GLE (Global Launch Excellence) (реалізація на Python).\n"
            "Та багато іншого...\n",
        'icon': '/static/images/cv/gpm.jpeg'
    },
    {
        'id': 'mens',
        'title': 'Men\'s Wearhouse',
        'role': 'Senior Java Розробник',
        'date': 'Січ 2016 - Лип 2017',
        'description': 'Men\'s Wearhouse — один із найбільших спеціалізованих ритейлерів чоловічого та офіційного одягу в США.',
        'details': 'Це проект моєї мрії: безліч місць для рефакторингу, відсутність тестів, але розумні технології, які дозволяють взяти все під контроль і плідно працювати! Щоденні скрами, дружна команда та креативні завдання тримали в тонусі. Використані технології: Backend: Java, Hibernate, RESTful services, Oracle; UI: AngularJS, JQuery;',
        'icon': '/static/images/cv/mens.jpeg'
    },
    {
        'id': 'selectica',
        'title': 'Selectica',
        'role': 'Senior Java Розробник',
        'date': 'Вер 2014 - Січ 2016',
        'description': 'Selectica — це додаток для управління життєвим циклом контрактів.',
        'details': 'Я прийшов на проект під час активного рефакторингу, тому одразу глибоко занурився у Spring framework. Зокрема — Spring Security (реалізував функцію login/logout), MVC — додаток побудований з використанням REST. Використані технології: Backend: Java, Spring, Oracle, QueryDSL; UI: Ajax, Backbone; сервер додатків JBoss.',
        'icon': '/static/images/cv/selectica.jpeg'
    },
    {
        'id': 'tis',
        'title': 'TIS',
        'role': 'Senior Java Розробник, Tech Lead',
        'date': 'Лют 2010 - Вер 2014',
        'description': 'TIS — це банківська платформа, що допомагає клієнтам взаємодіяти з банками.',
        'details': 'Через гетерогенну інфраструктуру та безліч протоколів дуже складно підтримувати всі платіжні транзакції, відстежувати ліквідність, контролювати баланс банківських рахунків тощо. TIS надає рішення для цього. Основні клієнти: Hugo Boss, Fujitsu, BMW, Swiss та ін. (http://www.tis.biz/en/customers/)',
        'icon': '/static/images/cv/tis.jpeg'
    },
    {
        'id': 'srp',
        'title': 'Shared Royalty Platform',
        'role': 'Junior Java Розробник',
        'date': 'Січ 2006 - Січ 2010',
        'description': 'Shared Royalty Platform — проект для розрахунку роялті та комісійних з продажів у музичній індустрії.',
        'details': 'Було близько 9 доменів, відокремлених один від одного, що взаємодіяли через шлюзові інтерфейси — контракти, продажі, продукти, субкнига (subledger), безпека, робочі процеси (workflow) тощо. Ключова роль у цьому проекті була виконана в зоні Subledger, де відбувалися бухгалтерські розрахунки та процеси закриття місяця. Проект використовував багато технологій, загорнутих у фреймворки Exigen, що робило їх використання зручнішим, але обмежувало деякі функції (і віддаляло розробників від оригінальних технологій). Опанував патерни проектування, модульне тестування (JUnit), функціональне тестування (на базі фреймворку Exigen), Oracle PL/SQL, та отримав неймовірний досвід командної роботи у великій розподіленій команді. Брав участь у мітингах та семінарах. Покращив рівень англійської до Upper-Intermediate.',
        'icon': '/static/images/cv/exigen.jpeg'
    }
    ]
}

CV_HOBBY_DATA = {
    'en': {
        'title': 'My Hobbies & Interests',
        'items': [
            {'icon': 'code', 'text': 'Programming: Making clients’ life easier'},
            {'icon': 'music_note', 'text': 'Music: Piano (> 5 years), Drums (5 years), Guitar (one-string-one-finger)'},
            {'icon': 'fitness_center', 'text': 'Sport: Gymnastics, bicycle riding'},
            {'icon': 'pets', 'text': 'Nature: Animals (cats & dogs), walking tours, photography'},
            {'icon': 'carpenter', 'text': 'Crafting: Modeling and cutting doll furniture from wood'},
            {'icon': 'edit', 'text': 'Writing: Short stories and books, based on life experience', 'url': 'https://tinyurl.com/pashkinson'},
            {'icon': 'translate', 'text': 'Languages: Ukrainian - reading history books, English (movies/books), Spanish & German'},
            {'icon': 'menu_book', 'text': 'Reading: Classic books in original'}
        ]
    },
    'uk': {
        'title': 'Мої хобі та захоплення',
        'items': [
            {'icon': 'code', 'text': 'Програмування: Робити життя клієнтів простішим'},
            {'icon': 'music_note', 'text': 'Музика: Фортепіано (> 5 років), барабани (5 років), гітара (стиль - на одній струні)'},
            {'icon': 'fitness_center', 'text': 'Спорт: Гімнастика, їзда на велосипеді'},
            {'icon': 'pets', 'text': 'Природа: Тварини (особливо коти та собаки), прогулянки, фотосесії'},
            {'icon': 'carpenter', 'text': 'Майстерність: Моделювання та вирізання меблів для ляльок з дерева'},
            {'icon': 'edit', 'text': 'Письмова творчість: Короткі оповідання', 'url': 'https://tinyurl.com/pashkinson'},
            {'icon': 'translate', 'text': 'Мови: Українська - обожнюю Остапа Вишню читати, Англійська, іспанська та німецька'},
            {'icon': 'menu_book', 'text': 'Читання: Класична література в оригіналі'}
        ]
    }
}


CV_LANGUAGES_DATA = {
    'en': {
        'title': 'Languages',
        'items': [
            {'lang': 'Ukrainian', 'level': 'Native or bilingual proficiency'},
            {'lang': 'English', 'level': 'Full professional proficiency, B2'},
            {'lang': 'Spanish', 'level': 'Limited working proficiency, in progress'}
        ]
    },
    'uk': {
        'title': 'Мови',
        'items': [
            {'lang': 'Українська', 'level': 'Рідна, на рівні Остапа Вишні'},
            {'lang': 'Англійська', 'level': 'Високий професійний рівень'},
            {'lang': 'Іспанська', 'level': 'Обмежений робочий рівень, вивчаю'}
        ]
    }
}

CV_SKILLS_DATA = {
    "Java Stack": {
        "icon": "coffee",
        "level": "expert",
        "items": ["Core Java", "Spring Boot", "Spring Framework", "Spring Security", "Hibernate", "JUnit", "RESTful WebServices"]
    },
    "Python Stack": {
        "icon": "terminal",
        "level": "advanced",
        "items": ["Python 3", "NiceGUI", "Pandas", "OCR", "Telegram Bot API", "Signal Bot"]
    },
    "Salesforce / Apex": {
        "icon": "cloud",
        "level": "advanced",
        "items": ["Apex", "SOQL", "Heroku", "Salesforce Platform", "LWC"]
    },
    "Frontend": {
        "icon": "web",
        "level": "intermediate",
        "items": ["React", "AngularJS", "JavaScript", "jQuery", "CSS", "Backbone"]
    },
    "Databases": {
        "icon": "storage",
        "level": "advanced",
        "items": ["Oracle", "PostgreSQL", "MySQL", "PL/SQL"]
    },
    "Tools & DevOps": {
        "icon": "build",
        "level": None,
        "items": ["Git", "Maven", "Jira", "IntelliJ IDEA", "AI: Claude, Gemini, Copilot", "Profilers"]
    },
    "Domains": {
        "icon": "category",
        "level": None,
        "items": ["Solution Architecture", "Android Development", "FPV Engineering", "Military Analytics"]
    },
    "Methodologies": {
        "icon": "loop",
        "level": None,
        "items": ["Scrum / Kanban / XP", "TDD", "Pair Programming", "Code Review", "Algorithms"]
    },
    "Soft Skills": {
        "icon": "psychology",
        "level": None,
        "items": ["Problem Solving", "Performance Optimization", "Communication", "Mentoring", "Mind Mapping"]
    },
}


CV_EXP_DATA = {
    'en': {
        'title': 'Work Experience',
        'items': [
            {
                'company': '79 mil-unit',
                'role': 'Python Developer, FPV',
                'period': 'Sep 2025 - now',
                'description': 'Analytic software development, Building and setting up FPV with electronic components.'
            },
            {
                'company': 'Model N',
                'role': 'Apex Developer',
                'period': 'Jul 2017 - Present',
                'description': 'Salesforce platform focus. Apex, Javascript, Python and Heroku management. Major areas: Data export to EXCEL, Competitor Module (React), GPI integration (Large JSON processing), Python formula engine.'
            },
            {
                'company': 'Men\'s Wearhouse',
                'role': 'Senior Java Developer',
                'period': 'Jan 2016 - Jul 2017',
                'description': 'Backend: Java, Hibernate, RESTfull services, Oracle; UI: AngularJS, JQuery. Everyday scrums, supportive team and creative tasks.'
            },
            {
                'company': 'Selectica',
                'role': 'Senior Java Developer',
                'period': 'Sep 2014 - Jan 2016',
                'description': 'Contract lifecycle management application. Backend: Java, Spring, Oracle, QueryDSL; UI: Ajax, Backbone; JBoss application server.'
            },
            {
                'company': 'Ciclum',
                'role': 'Senior Java Developer, Tech Lead',
                'period': 'Feb 2010 - Sep 2014',
                'description': 'Two projects had been delivered: Exiqon and TIS - Banking platform.'
            },
            {
                'company': 'Exigen',
                'role': 'Jr Java Developer',
                'period': 'Jan 2006 - Jan 2010',
                'description': 'Exigen was a prominent IT consulting and global software development firm founded in 1999 by tech entrepreneurs Greg Shenkman and Alec Miloslavsky. Participated in SRP (Shared Royalty Platform). Mastered design patterns, unit testing (JUnit), Oracle PL/SQL in a big distributed team.'
            }
        ]
    },
    'uk': {
        'title': 'Досвід роботи',
        'items': [
            {
                'company': 'ЗСУ, 79 бригада',
                'role': 'Python Developer, FPV',
                'period': 'Вересень 2025 - теперішній час',
                'description': 'Розробка аналітичних продуктів для бригади. Збір та налаштування FPV і компонентів.'
            },
            {
                'company': 'Model N',
                'role': 'Apex Developer',
                'period': 'Лип 2017 - Вересень 2025',
                'description': 'Розробка на платформі Salesforce. Apex, Javascript, Python та управління Heroku. Робота з великими масивами JSON, розробка Python formula engine.'
            },
            {
                'company': 'Men\'s Wearhouse',
                'role': 'Senior Java Developer',
                'period': 'Січ 2016 - Лип 2017',
                'description': 'Backend: Java, Hibernate, RESTfull services, Oracle; UI: AngularJS, JQuery. Щоденні скрами та творчі задачі.'
            },
            {
                'company': 'Selectica',
                'role': 'Senior Java Developer',
                'period': 'Вер 2014 - Січ 2016',
                'description': 'Додаток для управління життєвим циклом контрактів. Глибоке занурення у Spring framework, Spring Security. MVC через REST.'
            },
            {
                'company': 'Ciclum',
                'role': 'Senior Java Developer, Tech Lead',
                'period': 'Лют 2010 - Вер 2014',
                'description': 'Два закінчених проекти - Exiqon і Банківська платформа TIS.'
            },
            {
                'company': 'Exigen',
                'role': 'Jr Java Developer',
                'period': 'Січ 2006 - Січ 2010',
                'description': 'Участь у проекті SRP (розрахунок роялті у музичній індустрії). Робота з Oracle PL/SQL, JUnit та патернами проектування у великій команді.'
            }
        ]
    }
}

CLOSE_BT = {
    'en': 'CLOSE',
    'uk': 'ЗАКРИТИ'
}

NAME_LABEL = {
    'en': 'Pavel Zhelnov',
    'uk': 'Павло Желнов'
}

ROLE_TEXT = {
    'en': 'Senior Java Developer',
    'uk': 'Сеньйор Java Розробник'
}
PLACEHOLDER_TEXT = {
    'en': 'Details about: ',
    'uk': 'Детальна інформація про: '
}