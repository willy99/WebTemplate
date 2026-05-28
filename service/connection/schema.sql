-- Таблиця станів користувачів (для бота)
CREATE TABLE IF NOT EXISTS user_states (
    phone_number TEXT PRIMARY KEY,
    current_state TEXT DEFAULT 'START',
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблиця користувачів
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL,
    full_name TEXT,
    is_active INTEGER DEFAULT 1,
    session_token VARCHAR(50) DEFAULT '',
    failed_login_attempts INTEGER DEFAULT 0,
    lockout_until DATETIME,
    signal_last_activity DATETIME,
    email TEXT,
    phone TEXT,
    pending_contact TEXT,
    pending_type TEXT,
    verification_code TEXT,
    verification_expiry TEXT,
    use_2fa INTEGER NOT NULL DEFAULT 0,
    force_password_change INTEGER NOT NULL DEFAULT 0
);

-- Таблиця прав доступу для ролей
CREATE TABLE IF NOT EXISTS role_permissions (
    role TEXT NOT NULL,
    module_name TEXT NOT NULL,
    can_read INTEGER DEFAULT 0,
    can_write INTEGER DEFAULT 0,
    can_delete INTEGER DEFAULT 0,
    PRIMARY KEY (role, module_name)
);

-- Таблиця супровідних документів

-- Таблиця задач (Канбан)
CREATE TABLE IF NOT EXISTS task (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_by INTEGER NOT NULL,
    assignee INTEGER,
    task_status VARCHAR(50) DEFAULT 'NEW',
    task_type VARCHAR(50) DEFAULT '',
    task_subject VARCHAR(255) NOT NULL,
    task_details TEXT,
    task_deadline DATETIME,
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Зовнішні ключі
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assignee) REFERENCES users(id) ON DELETE SET NULL
);


CREATE TABLE IF NOT EXISTS subtask (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    is_done INTEGER DEFAULT 0,  -- SQLite не має типу BOOLEAN, використовуємо 0 або 1
    FOREIGN KEY (task_id) REFERENCES task (id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS sys_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    key_name TEXT NOT NULL UNIQUE,
    value TEXT,
    value_type TEXT NOT NULL,
    description TEXT,
    validation_rule TEXT
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    level TEXT NOT NULL,         -- 'INFO', 'WARNING', 'ERROR'
    domain TEXT NOT NULL,        -- 'AUTH', 'PERSON', 'REPORT'
    event_type TEXT NOT NULL,    -- 'SEARCH', 'UPDATE', 'LOGIN_ATTEMPT'
    username TEXT,
    ip_address TEXT,
    entity_id INTEGER,           -- ID прив'язаного об'єкта
    action_summary TEXT NOT NULL,
    details TEXT                 -- JSON рядок
);

