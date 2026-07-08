# Setup Guide

How to get Keep in Touch running locally. There are two pieces:

- **Backend** — a Supabase (PostgreSQL) project. Holds the data and auth.
- **Frontend** — an Expo (React Native) app you run with Expo Go on your phone.

You can set up the backend once and share the project with the team, or each
person can spin up their own. Both are covered below.

---

## Part 1 — Backend (Supabase)

### 1. Create / open the project

Go to [supabase.com](https://supabase.com) → sign in → **New project** (or open
the shared team project). Pick a name and a database password; wait ~2 minutes
for it to provision.

### 2. Run the schema

1. In the dashboard, open **SQL Editor** → **New query**.
2. Copy the entire contents of
   [`backend/supabase/migrations/0001_init.sql`](../backend/supabase/migrations/0001_init.sql).
3. Paste it into the editor and click **Run**.

This creates four tables — `people`, `interactions`, `reminders`,
`connections` — with Row-Level Security so each user only sees their own rows.

### 3. Turn off email confirmation (for now)

So sign-up / login works instantly without a confirmation email:

> **Authentication → Sign In / Providers → Email** → turn **off** *Confirm email* → Save.

(Turn it back on later for anything shared or production-like.)

### 4. Create a test user

Since the app's login screen isn't built yet, make a user by hand:

> **Authentication → Users → Add user → Create new user** → enter an email +
> password → enable *Auto Confirm User*.

### 5. (Optional) Load demo data

To get some example contacts/interactions/reminders to query against:

1. **SQL Editor** → **New query**.
2. Paste [`backend/supabase/seed.sql`](../backend/supabase/seed.sql) → **Run**.

It seeds the first user in `auth.users` (the one you just created).

### 6. Grab your API keys

**Settings → API** gives you two values the frontend will eventually need:

- **Project URL** → `EXPO_PUBLIC_SUPABASE_URL`
- **anon public** key → `EXPO_PUBLIC_SUPABASE_ANON_KEY`

The `anon` key is safe to use in the client — RLS is what protects the data.

---

## Part 2 — Frontend (Expo)

> The frontend is currently a **blank Expo starter** — the team builds the
> screens from here.

### Prerequisites

- [Node.js](https://nodejs.org) 20+
- The **Expo Go** app on your phone (App Store / Play Store), or an
  iOS Simulator / Android Emulator.

### Run it

```bash
cd frontend
npm install
npm run start
```

Then scan the QR code with Expo Go (iOS: Camera app; Android: the Expo Go
scanner). You should see the "Keep in Touch — Frontend starts here." screen.

Other commands: `npm run ios`, `npm run android`, `npm run web`.

### Connecting to Supabase (when you're ready)

When the frontend needs data, install the client and wire up env vars:

```bash
npm install @supabase/supabase-js @react-native-async-storage/async-storage react-native-url-polyfill
```

Create `frontend/.env` (it's gitignored — never commit it):

```
EXPO_PUBLIC_SUPABASE_URL=<your Project URL from step 6>
EXPO_PUBLIC_SUPABASE_ANON_KEY=<your anon key from step 6>
```

Then create a Supabase client and use email/password auth
(`supabase.auth.signUp` / `supabase.auth.signInWithPassword`). See the
[Supabase docs](https://supabase.com/docs/reference/javascript/introduction).

---

## Troubleshooting

- **`No user found in auth.users` when running the seed** — do step 4 first.
- **Expo Go can't connect** — make sure your phone and computer are on the
  same Wi-Fi network.
- **Wrong Node version** — `node -v` should be 20 or higher.
