# Backend — Supabase (PostgreSQL)

The backend is a Supabase project. There is no separate API server yet; the app
talks to Supabase directly, and **Row-Level Security** scopes every row to the
signed-in user.

```
backend/
└── supabase/
    ├── migrations/
    │   └── 0001_init.sql   Full schema + RLS
    └── seed.sql            Optional demo data
```

## Data model

Aligned with [../docs/mvp.md](../docs/mvp.md):

| Table          | Purpose (mvp.md name)                                             |
|----------------|------------------------------------------------------------------|
| `people`       | Contacts — name, relationship, location, phone, email, social, squad color, birthday |
| `interactions` | Interaction history — calls, messages, meetings, events          |
| `reminders`    | Follow-ups, birthdays, and other upcoming events                 |
| `connections`  | Relationships between two contacts (Relationship Connection)     |

## Running the SQL

Step-by-step (create project, run schema, disable email confirmation, add a
test user, seed) lives in **[../docs/setup.md](../docs/setup.md)**.

Quick version — in the Supabase **SQL Editor**:

1. Run `supabase/migrations/0001_init.sql` (creates all tables + RLS).
2. Optionally run `supabase/seed.sql` for demo data (needs a user in
   `auth.users` first).
