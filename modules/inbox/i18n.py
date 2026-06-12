"""Inbox module translations."""

TRANSLATIONS: dict[str, dict[str, str]] = {
    'uk': {
        'menu.inbox': 'Пошта',

        'inbox.queue_empty': 'Черга порожня',
        'inbox.queue_count': 'В черзі на обробку: {count}',

        'inbox.archive_saving': '⏳ Архів: збереження {filename}...',
        'inbox.archive_done': '✅ {filename} архівовано!',
        'inbox.archive_error': '❌ Помилка архівації {filename}',
        'inbox.delete_done': '🗑️ {filename} успішно видалено',
        'inbox.assign_done': '👤 {filename} передано користувачу {target}',
        'inbox.action_error': '❌ Сталася помилка під час обробки {filename}: {error}',

        'inbox.added_to_queue': 'Додано в чергу: {filename}',

        'inbox.upload_done': 'Файл "{filename}" завантажено!',
        'inbox.upload_rejected': 'Файл відхилено: {error}',
        'inbox.upload_error': 'Помилка завантаження: {error}',

        'inbox.load_error': 'Помилка завантаження файлів: {error}',
        'inbox.reading': 'Читання документу...',
        'inbox.content_error': '❌ Неможливо відобразити вміст файлу.\nПомилка: {error}',

        'inbox.download_started': 'Завантаження {filename} почалося.',
        'inbox.download_failed': 'Не вдалося завантажити файл.',
        'inbox.download_error': 'Помилка завантаження: {error}',

        'inbox.upload_section': 'Завантажити у спільну папку',
        'inbox.personal_inbox': '🔴 Вхідні (Inbox) ({count})',
        'inbox.personal_outbox': '🟢 Вихідні (Outbox) ({count})',
        'inbox.shared_files': '⚪ Спільні файли ({count})',
        'inbox.no_files': 'Немає файлів',

        'inbox.select_doc': 'Оберіть документ для перегляду',
        'inbox.in_queue': 'Очікує в черзі...',

        'inbox.btn_download': 'Завант.',
        'inbox.btn_assign': 'Призначити',
        'inbox.btn_archive': 'Архів',
        'inbox.btn_delete': 'Видалити',
        'inbox.select_user': 'Кому',
        'inbox.select_user_shared': 'Оберіть юзера',
        'inbox.confirm_delete': 'Видалити "{filename}"?',

        'inbox.mobile_folders': '📁 Папки та Файли',
        'inbox.mobile_content': '📄 Вміст та Дії',
    },
    'en': {
        'menu.inbox': 'Mail',

        'inbox.queue_empty': 'Queue is empty',
        'inbox.queue_count': 'In queue: {count}',

        'inbox.archive_saving': '⏳ Archive: saving {filename}...',
        'inbox.archive_done': '✅ {filename} archived!',
        'inbox.archive_error': '❌ Archive error: {filename}',
        'inbox.delete_done': '🗑️ {filename} deleted',
        'inbox.assign_done': '👤 {filename} assigned to {target}',
        'inbox.action_error': '❌ Error processing {filename}: {error}',

        'inbox.added_to_queue': 'Added to queue: {filename}',

        'inbox.upload_done': 'File "{filename}" uploaded!',
        'inbox.upload_rejected': 'File rejected: {error}',
        'inbox.upload_error': 'Upload error: {error}',

        'inbox.load_error': 'File load error: {error}',
        'inbox.reading': 'Reading document...',
        'inbox.content_error': '❌ Cannot display file contents.\nError: {error}',

        'inbox.download_started': 'Downloading {filename}.',
        'inbox.download_failed': 'Could not download file.',
        'inbox.download_error': 'Download error: {error}',

        'inbox.upload_section': 'Upload to shared folder',
        'inbox.personal_inbox': '🔴 Inbox ({count})',
        'inbox.personal_outbox': '🟢 Outbox ({count})',
        'inbox.shared_files': '⚪ Shared files ({count})',
        'inbox.no_files': 'No files',

        'inbox.select_doc': 'Select a document to preview',
        'inbox.in_queue': 'Waiting in queue...',

        'inbox.btn_download': 'Download',
        'inbox.btn_assign': 'Assign',
        'inbox.btn_archive': 'Archive',
        'inbox.btn_delete': 'Delete',
        'inbox.select_user': 'Assign to',
        'inbox.select_user_shared': 'Select user',
        'inbox.confirm_delete': 'Delete "{filename}"?',

        'inbox.mobile_folders': '📁 Folders & Files',
        'inbox.mobile_content': '📄 Content & Actions',
    },
}
