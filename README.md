# WebTemplate Project

A Python web application skeleton built on **NiceGUI** (FastAPI-based), providing a ready-made foundation for admin panels, user management, task tracking, document inbox, calendar, and audit logging. Optionally integrates with a **Signal messenger bot** for receiving and processing document attachments.

---

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Roles & Permissions](#roles--permissions)
- [Signal Bot Integration](#signal-bot-integration)
- [Development Notes](#development-notes)
- [Testing](#testing)

---

## Features

| Module | Description |
|---|---|
| **User Management** | Create/edit users, assign roles, enforce password policy, force password reset |
| **Authentication** | Username + password login, optional 2FA via Email or Signal, session tokens, IP-based lockout |
| **Role-Based Access** | Per-module read/write/delete permissions configurable per role through the admin panel |
| **Task Manager** | Kanban-style tasks with subtasks, assignees, deadlines, status flow (NEW → IN_PROGRESS → COMPLETED / CANCELED) |
| **Document Inbox** | Receive files, triage and process documents; inbox/outbox directory workflow |
| **Calendar** | Timeline view of tasks and scheduled events |
| **Audit Log** | All security-relevant events (logins, updates, deletes, searches) logged with user, IP, and details |
| **System Config** | Key-value configuration store editable from the admin panel at runtime |
| **Signal Bot** | Optional background worker that connects to a signal-cli daemon, parses incoming messages and attachments, and runs them through the document processing pipeline |
| **Document Processing** | Multi-format parser pipeline: PDF, DOCX, DOC, TXT, images (OCR). Factory pattern makes adding new formats straightforward |
| **File Storage** | Pluggable storage backend: local filesystem or SMB/CIFS network shares |
| **Report Generation** | Template-based DOCX report generation via docxtpl |
| **Excel Integration** | Batch read/write Excel files with chunked processing (default 2000 rows) and column mapper admin tool |
| **Backup** | Scheduled daily backups, configurable retention period (default 30 days) |

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Web Framework** | [NiceGUI](https://nicegui.io) ~3.8 (built on FastAPI + Starlette) |
| **Database** | SQLite (WAL mode, thread-safe via `threading.Lock`) |
| **Data Validation** | Pydantic v2 |
| **Auth** | werkzeug password hashing, custom session tokens |
| **PDF** | PyMuPDF |
| **DOCX/DOC** | python-docx, docxtpl |
| **OCR** | EasyOCR, pytesseract, Pillow, OpenCV |
| **Data / Excel** | pandas, openpyxl |
| **Charts** | Plotly |
| **3D / About page** | Three.js |
| **Networking** | smbprotocol (SMB/CIFS), smtplib (Email) |
| **Config** | python-dotenv |
| **Testing** | pytest |
| **Runtime** | Python 3.14+ |

---

## Architecture

```
bot.py (entry point)
│
├── ConfigService      — syncs sys_config table → config.py at startup
├── MyWorkFlow         — orchestrates all services, holds shared DB reference
│
├── [Thread] bot_worker  — async Signal listener (if SIGNAL_BOT=true)
│   └── SignalBotHandler → AttachmentHandler → DocumentProcessingService
│                                               └── ParserFactory (PDF/DOCX/IMG…)
│                                               └── StorageFactory (Local/SMB)
│
└── init_nicegui()     — NiceGUI web server
    ├── auth_routes.py   — /login page + @require_access decorator
    ├── navigation.py    — registers all routes
    └── views/           — page renderers
        ├── admin/       — users, permissions, settings, audit log, column mapper
        ├── task/        — task list + task editor
        ├── inbox/       — inbox triage
        ├── calendar/    — calendar/timeline
        └── report/      — log viewer
```

### Request lifecycle

```
Route hit → @require_access → AuthManager (session token) → RequestContext
         → View → Controller → Service → MyDataBase (SQLite)
                                       → AuditLogService (all writes/deletes/searches)
```

---

## Database Schema

Six tables created by `service/connection/schema.sql`:

| Table | Purpose |
|---|---|
| `users` | Web users: credentials, role, 2FA config, session token, lockout state |
| `role_permissions` | RBAC matrix: `(role, module_name)` → can_read / can_write / can_delete |
| `task` | Tasks with assignee, deadline, status, type |
| `subtask` | Checklist items belonging to a task |
| `sys_config` | Runtime key-value configuration with type + validation rule |
| `audit_logs` | Timestamped audit trail: level, domain, event_type, user, IP, summary, JSON details |
| `user_states` | Signal bot conversation state per phone number |

Performance indexes are applied from `service/connection/update.sql` (task kanban queries, audit log queries by timestamp/user/domain).

---

## Project Structure

```
WebTemplate/
├── bot.py                          # Entry point
├── config.py                       # All configuration constants + .env validation
├── requirements.txt
├── pytest.ini
│
├── dics/
│   ├── security_config.py          # Role names, module constants, permission constants
│   └── deserter_xls_dic.py         # Excel regex patterns / column dictionaries
│
├── domain/                         # Domain models (Pydantic / dataclasses)
│   ├── user.py
│   ├── task.py
│   ├── audit_log_filter.py
│   ├── sys_config.py
│   └── db/AuditLogDB.py
│
├── gui/                            # Frontend layer (NiceGUI)
│   ├── navigation.py               # Route registration
│   ├── auth_routes.py              # Login page + @require_access decorator
│   ├── components.py               # Shared UI components (nav menu, etc.)
│   ├── services/
│   │   ├── auth_manager.py         # Session management
│   │   └── request_context.py      # Per-request context (user_id, IP)
│   ├── tools/
│   │   ├── ui_components.py
│   │   └── validation.py
│   ├── controllers/                # Thin business-logic layer between views and services
│   │   ├── task_controller.py
│   │   ├── inbox_controller.py
│   │   ├── audit_controller.py
│   │   ├── admin_audit_controller.py
│   │   ├── config_controller.py
│   │   └── user_controller.py
│   ├── views/
│   │   ├── home_view.py
│   │   ├── admin/                  # Admin panel pages
│   │   ├── task/                   # Task list + editor
│   │   ├── inbox/                  # Inbox triage
│   │   ├── calendar/               # Calendar / timeline
│   │   ├── report/                 # Log viewer
│   │   └── pages/                  # Static pages (CV, About)
│   └── static/style.css
│
├── service/                        # Core business logic & infrastructure
│   ├── constants.py                # DB column names, status values, date formats
│   ├── connection/
│   │   ├── MyDataBase.py           # Thread-safe SQLite wrapper
│   │   ├── schema.sql              # Initial schema
│   │   ├── update.sql              # Indexes
│   │   ├── SignalClient.py         # TCP connection to signal-cli daemon
│   │   └── EmailClient.py          # SMTP client
│   ├── users/
│   │   ├── UserService.py
│   │   └── AuthService.py
│   ├── docworkflow/
│   │   ├── TaskService.py
│   │   └── InboxService.py
│   ├── admin/AuditLogService.py
│   ├── config/ConfigService.py
│   ├── storage/
│   │   ├── FileStorageClient.py    # Abstract base
│   │   ├── LocalFileClient.py
│   │   ├── SMBFileClient.py
│   │   ├── StorageFactory.py
│   │   ├── LoggerManager.py
│   │   └── BackupData.py
│   └── processing/
│       ├── MyWorkFlow.py           # Service orchestrator
│       ├── DocumentProcessingService.py
│       ├── parsers/                # PDF, DOCX, DOC, TXT, IMG + ParserFactory
│       ├── processors/             # BatchProcessor, DocTemplator
│       └── workflow/               # SignalBotHandler, AttachmentHandler
│
├── resources/templates/            # DOCX report templates (docxtpl)
├── static/                         # CSS, Three.js, images
├── utils/utils.py
├── scripts/update_file_cache.py
└── tests/
```

---

## Prerequisites

- Python 3.14+
- `tesseract-ocr` system package (for pytesseract)
- `signal-cli` + Java 21 (only if using the Signal bot)
- Access to an SMTP server (only if using email 2FA)

---

## Installation

```bash
# 1. Clone / download the project
git clone <repo-url>
cd WebTemplate

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. (Optional) Ukrainian spaCy model — only needed for NLP-based document parsing
python -m spacy download uk_core_news_sm

# 5. Copy and fill in environment config
cp config_examples/.env_example .env
# Edit .env — see Configuration section below
```

---

## Configuration

All settings live in `.env` (loaded by `config.py`). The file permissions are automatically set to `600` on startup.

| Variable | Required | Description |
|---|---|---|
| `UI_SECRET_KEY` | **Yes** | Secret key for signing session tokens. App will refuse to start without it. |
| `EMAIL_PASSWORD` | For email 2FA | SMTP account password |
| `EMAIL_SMTP_SERVER` | For email 2FA | e.g. `smtp.gmail.com` |
| `EMAIL_SMTP_PORT` | For email 2FA | e.g. `587` |
| `EMAIL_SENDER` | For email 2FA | Sender address |
| `NET_SERVER_IP` | For SMB storage | Network share host (default `192.168.0.53`) |
| `NET_USERNAME` | For SMB storage | Share username |
| `NET_PASSWORD` | For SMB storage | Share password |
| `SIGNAL_BOT` | No | `true` to enable Signal bot (default `false`) |
| `DAILY_BACKUPS` | No | `true` to enable daily backups (default `true`) |

**Hardcoded defaults in `config.py`** (override in the file or via sys_config at runtime):

| Constant | Default | Description |
|---|---|---|
| `UI_PORT` | `8080` (prod) / `8081` (dev) | Web server port |
| `SECURITY_SESSION_TIMEOUT` | `3600` s | Session expiry |
| `SECURITY_MAX_ATTEMPTS` | `5` | Failed logins before lockout |
| `SECURITY_LOCKOUT_DURATION_MINS` | `15` min | Lockout duration |
| `DAY_ROLLOVER_HOUR` | `16` | Hour after which the "today" folder rolls to tomorrow |
| `BACKUP_KEEP_DAYS` | `30` | Days to retain backups |
| `EXCEL_CHUNK_SIZE` | `2000` | Rows per Excel read chunk |
| `CHECK_INBOX_EVERY_SEC` | `60.0` s | Inbox poll interval |

---

## Running the Application

```bash
# Production (port 8080)
python bot.py --prod

# Development (port 8081, verbose output)
python bot.py --dev
```

The app will:
1. Validate `.env` and fix file permissions if needed
2. Initialize the SQLite database (schema + indexes, idempotent `CREATE IF NOT EXISTS`)
3. Sync default values into `sys_config`
4. Start the Signal bot background thread (if `SIGNAL_BOT=true`)
5. Start the NiceGUI web server

Open `http://localhost:8080` (or `8081` in dev mode).

---

## Roles & Permissions

Roles are defined in `dics/security_config.py`. Default roles:

| Role | Intended for |
|---|---|
| `admin` | Full access including admin panel |
| `Командір` | Supervisor-level access |
| `Офіс` | Office staff |
| `Бджілка` | Field / limited access |
| `Гість` | Read-only guest |

**Modules** that permissions can be granted on:

| Module key | Display name |
|---|---|
| `search` | General access (home / search) |
| `task` | Task manager |
| `report_general` | Reporting |
| `admin_panel` | Admin panel |

Permissions (`read`, `write`, `delete`) per role + module are managed through the **Admin → Permissions** page and stored in the `role_permissions` table.

---

## Signal Bot Integration

The Signal bot is optional. When enabled it:

1. Connects to a running `signal-cli` daemon over TCP
2. Parses incoming JSON-RPC messages
3. Routes attachments through the document processing pipeline
4. Maintains per-phone conversation state in `user_states`

**Starting signal-cli daemon:**

```bash
# Install Java 21 first (e.g. via jenv)
jenv local 21

# TCP mode (used by default)
signal-cli -u +<YOUR_NUMBER> daemon --tcp 127.0.0.1:1234

# Socket mode (macOS alternative)
signal-cli -u +<YOUR_NUMBER> daemon --socket /tmp/signal-bot.sock
```

**Linking a device:**

```bash
signal-cli link -n "WebTemplate Bot"
```

**Troubleshooting — reset signal-cli state:**

```bash
rm -rf ~/.local/share/signal-cli
mkdir -p ~/.local/share/signal-cli
```

**Running a second Signal instance on macOS (for testing):**

```bash
/Applications/Signal.app/Contents/MacOS/Signal \
  --user-data-dir="$HOME/Library/Application Support/Signal-2"
```

---

## Document Processing Pipeline

```
Incoming file (Signal attachment or inbox upload)
    │
    ▼
ParserFactory.get_parser(file_extension)
    │
    ├── PdfParser      (PyMuPDF)
    ├── DocxParser     (python-docx)
    ├── DocOldParser   (.doc via legacy conversion)
    ├── TxtParser
    └── ImgParser      (EasyOCR + pytesseract fallback)
    │
    ▼
Extracted text / structured data
    │
    ▼
BatchProcessor / DocTemplator (report generation)
    │
    ▼
StorageFactory.get_client()
    ├── LocalFileClient   (DOCUMENT_STORAGE_PATH)
    └── SMBFileClient     (network share)
```

Folder structure for stored files: `YYYY/MM/dd.mm.yyyy/original_filename`.

---

## Development Notes

- **Single DB connection** — `MyDataBase` is created once in `main()` and injected everywhere. Do not create additional connections to the same SQLite file.
- **Thread safety** — `MyDataBase` wraps every query in a `threading.Lock`. The Signal bot runs in a separate thread with its own asyncio event loop.
- **Adding a new parser** — implement `BaseFileParser`, register in `ParserFactory`.
- **Adding a new storage backend** — implement `FileStorageClient`, register in `StorageFactory`.
- **Adding a new page** — create a view in `gui/views/`, a controller in `gui/controllers/`, and register the route in `gui/navigation.py`. Protect with `@require_access`.
- **Adding a role** — add the string to `AVAILABLE_ROLES` in `dics/security_config.py`, then configure its permissions via the admin panel.
- **Excel pivot tables** — before processing Excel files that contain pivot tables, right-click the pivot → PivotTable Options → Data tab → uncheck "Save source data with file".

---

## Testing

```bash
# Run all tests
pytest

# Verbose output
pytest -v
```

Test fixtures and temporary output live in `tests/fixtures/` and `tests/tests_tmp/`. Keep tests green — they are the safety net for the document processing pipeline.
