# app-invoices

A FastAPI REST API backed by PostgreSQL (async).

---

## Stack

| Layer | Technology |
|---|---|
| API | FastAPI + Uvicorn |
| Database | PostgreSQL (async via asyncpg + SQLAlchemy) |
| Config | pydantic-settings (.env) |

---

## Setup

### 1. Run the setup script

```bash
bash setup.sh
source .venv/bin/activate
```

This creates the virtual environment and installs all dependencies from `requirements.txt`.

### 2. Configure environment

Create a `.env` file in the project root:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_super_secret_password
POSTGRES_SERVER=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_DB=app_invoices
```

### 4. Start the API

```bash
python -m uvicorn app.main:app --reload --reload-dir app
```

API available at: `http://localhost:8000`
Interactive docs: `http://localhost:8000/docs`

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/invoices/` | List invoices (optional `startDate` / `endDate` filters) |
| POST | `/invoices/` | Create an invoice |
| GET | `/invoices/{id}` | Get invoice by ID |
| DELETE | `/invoices/{id}` | Delete invoice by ID |

### Date filter example

```
GET /invoices/?startDate=2024-01-01T00:00:00&endDate=2024-12-31T23:59:59
```

---


## Project Structure

```
app/
├── api/
│   ├── health.py       # Health check route
│   ├── invoices.py     # Invoice CRUD routes
│   └── schemas.py      # Pydantic request/response models
├── core/
│   └── config.py       # Settings loaded from .env
├── db/
│   ├── database.py     # Async engine + session
│   └── models.py       # SQLAlchemy ORM models
├── worker/
│   └── tasks.py        # Celery task definitions
└── main.py             # FastAPI app entry point
```

---

