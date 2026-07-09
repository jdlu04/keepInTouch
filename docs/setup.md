# Setup Guide

How to get Keep in Touch running locally. There are two pieces:

- **Backend** — a FastAPI (Python) server. Owns the API, auth, and all logic.
  It connects to a PostgreSQL database hosted on Supabase.
- **Frontend** — an Expo (React Native) app you run in the browser or with
  Expo Go on your phone.

You can point the whole team at one shared database, or each person can spin up
their own. Both are covered below.

---

## Part 1 — Backend (FastAPI + Postgres)

### Prerequisites

- [Python](https://www.python.org/downloads/) 3.11+
- A PostgreSQL database. Easiest: a free **Supabase** project used purely as a
  database (no Supabase API/Auth/RLS). A local Postgres works too.

### 1. Get a database connection string

**Using Supabase (recommended):** go to [supabase.com](https://supabase.com) →
sign in → open (or create) the project. Then **Project Settings → Database →
Connection string → URI**, and copy the **Session pooler** URI. It looks like:

```
postgresql://postgres.abcxyz:YOUR-PASSWORD@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

You'll adapt it for SQLAlchemy in the next step (add the driver + SSL).

> If your project still has the old `people` / `interactions` / … tables from
> the previous Supabase-SQL setup, drop them first (SQL Editor:
> `drop schema public cascade; create schema public;`). Alembic will recreate
> everything.

### 2. Install and configure

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
```

Edit `.env`:

- **`DATABASE_URL`** — your connection string, with the driver prefix and SSL:
  ```
  DATABASE_URL=postgresql+psycopg2://postgres.abcxyz:YOUR-PASSWORD@aws-0-us-east-1.pooler.supabase.com:5432/postgres?sslmode=require
  ```
  (Local Postgres: `postgresql+psycopg2://postgres:postgres@localhost:5432/kit`.)
- **`JWT_SECRET`** — a long random string. Generate one with:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```

### 3. Create the tables

```bash
alembic upgrade head
```

This creates all five tables — `users`, `people`, `interactions`, `reminders`,
`connections`. (Later, if you change `app/models.py`, run
`alembic revision --autogenerate -m "..."` then `alembic upgrade head`.)

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

- API base: **http://localhost:8000**
- Interactive docs (try every endpoint): **http://localhost:8000/docs**

Create your first account from the docs page (or curl): `POST /auth/signup` with
an email + password returns a JWT. Click **Authorize** in `/docs`, paste the
token, and you can call the protected endpoints.

See [`backend/README.md`](../backend/README.md) for the full endpoint list and
the strength/reminder logic.

---

## Part 2 — Frontend (Expo)

> The frontend is currently a **blank Expo starter** — the team builds the
> screens from here, calling the FastAPI backend over HTTP.

### Prerequisites

- [Node.js](https://nodejs.org) 20+
- The **Expo Go** app on your phone (App Store / Play Store), or an
  iOS Simulator / Android Emulator, or just the browser.

### Run it

```bash
cd frontend
npm install
npm run start
```

Press `w` for the browser, or scan the QR code with Expo Go. Other commands:
`npm run ios`, `npm run android`, `npm run web`.

### Connecting to the backend (when you're ready)

The app talks to FastAPI over plain HTTP (`fetch`), so nothing Supabase-specific
is needed. Point it at the API with an env var in `frontend/.env` (gitignored):

```
EXPO_PUBLIC_API_URL=http://localhost:8000
```

> On a physical phone, `localhost` refers to the phone, not your computer — use
> your machine's LAN IP (e.g. `http://192.168.1.20:8000`) and make sure the
> backend is started and reachable on your network. Add that origin to the
> backend's `CORS_ORIGINS` if you lock CORS down.

Log in by POSTing to `/auth/login`, store the returned `access_token`, and send
it as `Authorization: Bearer <token>` on every request.

---

## Troubleshooting

- **`alembic: command not found`** — activate the venv first
  (`source .venv/bin/activate`).
- **DB connection / SSL errors with Supabase** — make sure the URL starts with
  `postgresql+psycopg2://` and ends with `?sslmode=require`.
- **401 on every request** — you need to send the JWT:
  `Authorization: Bearer <token>` (in `/docs`, use the **Authorize** button).
- **CORS errors in the browser** — set `CORS_ORIGINS` in the backend `.env`
  (use `*` in development).
- **Expo Go can't reach the API** — phone and computer must be on the same
  Wi-Fi, and the app must use your computer's LAN IP, not `localhost`.
- **Wrong Node version** — `node -v` should be 20 or higher.
