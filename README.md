# Keep in Touch (KiT)

A relationship management app that helps you stay connected with the people who
matter — track interactions, remember details, and get reminded to reach out.

Full product spec: [docs/mvp.md](docs/mvp.md).
**Setup / how to run:** [docs/setup.md](docs/setup.md).

## Repository layout

```
keep-in-touch/
├── frontend/      Expo (React Native) app — blank starter, built by the frontend team
├── backend/       Supabase (PostgreSQL) schema + seed data
├── docs/          Product spec (mvp.md) and setup guide (setup.md)
└── README.md
```

## Tech stack

| Layer          | Technology                       |
|----------------|----------------------------------|
| Frontend       | React Native (Expo)              |
| Database       | Supabase (PostgreSQL)            |
| Authentication | Supabase Auth (email + password) |

> The [spec](docs/mvp.md) lists FastAPI as a future backend layer. For now the
> app talks directly to Supabase, with Row-Level Security enforcing per-user
> data isolation — there is no separate API server yet.

## Getting started

See **[docs/setup.md](docs/setup.md)** for full instructions. In short:

1. **Backend** — create a Supabase project and run
   [backend/supabase/migrations/0001_init.sql](backend/supabase/migrations/0001_init.sql).
2. **Frontend** — `cd frontend && npm install && npm run start`, then open in Expo Go.

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
