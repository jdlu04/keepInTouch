# Keep in Touch (KiT)

A relationship management app that helps you stay connected with the people who
matter — track interactions, remember details, and get reminded to reach out.

Full product spec: [docs/mvp.md](docs/mvp.md).
**Setup / how to run:** [docs/setup.md](docs/setup.md).

## Repository layout

```
keep-in-touch/
├── frontend/      Expo (React Native) app — blank starter, built by the frontend team
├── backend/       FastAPI (Python) API — auth + all business logic
├── docs/          Product spec (mvp.md) and setup guide (setup.md)
└── README.md
```

## Tech stack

| Layer          | Technology                             |
|----------------|----------------------------------------|
| Frontend       | React Native (Expo) — web + iOS + Android |
| Backend / API  | FastAPI (Python)                       |
| Database       | PostgreSQL (hosted on Supabase)        |
| ORM / Migrations | SQLAlchemy + Alembic                 |
| Authentication | FastAPI + JWT (email + password, bcrypt) |

> The app calls a FastAPI server over HTTP; FastAPI owns all logic and auth and
> is the only thing that touches the database. Supabase is used **only** as a
> managed Postgres host — not its API, Auth, or RLS. Same backend for web and
> native.

## Getting started

See **[docs/setup.md](docs/setup.md)** for full instructions. In short:

1. **Backend** — `cd backend`, create a venv, `pip install -r requirements.txt`,
   copy `.env.example` to `.env` (set `DATABASE_URL` + `JWT_SECRET`), then
   `alembic upgrade head` and `uvicorn app.main:app --reload`. Open
   http://localhost:8000/docs. See [backend/README.md](backend/README.md).
2. **Frontend** — `cd frontend && npm install && npm run start`, then open in
   the browser or Expo Go.

## Team

| Name           | Role                             |
|----------------|----------------------------------|
| Sehr Abrar     | Backend Engineer                 |
| Nirath Hussan  | Frontend Engineer / UI Designer  |
| Judy Liu       | Backend Engineer / UI Designer   |
| Lily Minchala  | Frontend Engineer / UI Designer  |

## Contributing

- Branch off `main`, open a PR back into `main`.
- CI runs a TypeScript typecheck on the frontend for every PR
  (`.github/workflows/ci.yml`).
- Never commit secrets. `frontend/.env` is gitignored.
