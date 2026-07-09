# Backend — FastAPI (Python)

The backend is a **FastAPI** service. It owns **all** business logic and
authentication and is the only thing that talks to the database. The app (web +
native) calls it over HTTP. PostgreSQL is hosted on Supabase, but we use
Supabase **only as a managed database** — none of its API, Row-Level Security,
or Auth features.

```
backend/
├── app/
│   ├── main.py            FastAPI app + CORS + router wiring
│   ├── config.py          settings from .env (DATABASE_URL, JWT_SECRET, CORS)
│   ├── database.py        SQLAlchemy engine + session
│   ├── security.py        bcrypt password hashing + JWT tokens
│   ├── deps.py            get_db() and get_current_user() dependencies
│   ├── models.py          SQLAlchemy ORM models (the schema, in Python)
│   ├── schemas.py         Pydantic request/response models
│   ├── services/
│   │   ├── strength.py    relationship-strength algorithm
│   │   └── reminders.py   birthday/anniversary reminder generation
│   └── routers/
│       ├── auth.py         signup / login / me / settings
│       ├── people.py       contacts CRUD (+ computed strength)
│       ├── interactions.py timeline; logging returns new strength
│       ├── reminders.py    upcoming feed, CRUD, generate
│       └── connections.py  edges for the relationship map
├── alembic/               database migrations (Alembic)
├── requirements.txt
└── .env.example
```

## Architecture

```
Expo app (web + iOS + Android)  ──HTTP/JSON──▶  FastAPI  ──SQLAlchemy──▶  PostgreSQL (on Supabase)
        Authorization: Bearer <JWT>              auth + logic here
```

Access control is enforced **in code**: every query filters by the authenticated
user's id, and each endpoint 404s on rows the caller doesn't own. There is no
RLS — FastAPI is the gatekeeper.

## Data model (SQLAlchemy models in `app/models.py`)

| Table          | Purpose (mvp.md)                                                             |
|----------------|------------------------------------------------------------------------------|
| `users`        | Accounts + **Settings** (email, hashed password, reminders/notifications toggles, relationship categories). |
| `people`       | Contacts — name, relationship, location, phone, email, social, squad color, birthday, anniversary, notes, favorite. |
| `interactions` | Timeline — calls, messages, meetings, events, notes.                         |
| `reminders`    | Follow-ups, birthdays, anniversaries, gifts (`type` column).                 |
| `connections`  | Edges between two contacts for the relationship map.                         |

## Business logic (the "algorithms")

Both live in `app/services/` as plain Python, unit-testable on their own:

**Relationship strength** (`strength.py`) — drives node size / the map legend:

```
strength = min(100, interaction_count * 12 + recency_bonus)
recency_bonus = 40 (<=1 week) | 25 (<=1 month) | 10 (<=3 months) | else 0
```

**Reminder generation** (`reminders.py`) — `generate_date_reminders()` ensures
every contact with a birthday/anniversary has an upcoming reminder for its next
occurrence. Idempotent, so it's safe to call on every app launch.

## API endpoints

Interactive docs (auto-generated): run the server and open **`/docs`**.

| Method | Path | What |
|--------|------|------|
| POST | `/auth/signup` | Create account, returns a JWT |
| POST | `/auth/login` | Email + password → JWT (OAuth2 form) |
| GET / PATCH | `/auth/me` | Current user + settings |
| GET / POST | `/people` | List (with `?q=`, `?relationship=`, `?favorite=`) / create |
| GET / PATCH / DELETE | `/people/{id}` | Read / update / delete a contact |
| GET / POST | `/people/{id}/interactions` | Timeline / log (returns new strength) |
| DELETE | `/interactions/{id}` | Delete an interaction |
| GET / POST | `/reminders` | Feed (`?days=`, `?include_completed=`) / create |
| PATCH / DELETE | `/reminders/{id}` | Update (e.g. complete) / delete |
| POST | `/reminders/generate` | Generate birthday/anniversary reminders |
| GET / POST | `/connections` | List / create an edge |
| DELETE | `/connections/{id}` | Delete an edge |
| GET | `/health` | Liveness check |

All routes except `/health`, `/auth/signup`, and `/auth/login` require
`Authorization: Bearer <token>`.

## Running locally

Full step-by-step (get the Supabase connection string, etc.) is in
**[../docs/setup.md](../docs/setup.md)**. Quick version:

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # then edit: set DATABASE_URL + JWT_SECRET

alembic upgrade head        # create the tables
uvicorn app.main:app --reload
```

Open **http://localhost:8000/docs** to try the API. The Expo web dev server
runs on a different port, which is why CORS is enabled (see `CORS_ORIGINS`).

## Migrations (Alembic)

The schema lives in `app/models.py`; Alembic turns model changes into versioned
migrations.

```bash
alembic upgrade head                                   # apply all migrations
alembic revision --autogenerate -m "add X to people"   # after editing models.py
alembic downgrade -1                                    # roll back one
```

The initial migration (all five tables) is already committed under
`alembic/versions/`.
