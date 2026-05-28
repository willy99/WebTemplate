-- ==========================================
-- ІНДЕКСИ ДЛЯ ТАБЛИЦІ ЗАДАЧ
-- ==========================================
-- Прискорює вибірку задач для конкретного юзера (Канбан дошка)
CREATE INDEX IF NOT EXISTS idx_task_assignee_status ON task(assignee, task_status);

-- Прискорює фоновий таймер (будильник дедлайнів)
CREATE INDEX IF NOT EXISTS idx_task_assignee_deadline ON task(assignee, task_deadline);

-- Прискорює пошук всіх задач, створених певним офіцером
CREATE INDEX IF NOT EXISTS idx_task_created_by ON task(created_by);

-- ==========================================
-- ІНДЕКСИ ДЛЯ КОРИСТУВАЧІВ
-- (username вже має UNIQUE індекс під капотом)
-- ==========================================
-- Прискорює пошук активних юзерів для випадаючого списку виконавців
CREATE INDEX IF NOT EXISTS idx_users_active ON users(is_active);


-- Індекси для супер-швидкого пошуку та фільтрації логів
CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_logs_username ON audit_logs(username);
CREATE INDEX IF NOT EXISTS idx_logs_domain ON audit_logs(domain);
CREATE INDEX IF NOT EXISTS idx_logs_entity_id ON audit_logs(entity_id);