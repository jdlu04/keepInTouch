# Keep in Touch — starter

A cross-platform (iOS / Android / web) personal relationship manager. This repo
is the Day 1–4 skeleton: passwordless auth, a per-user Postgres schema with
row-level security, and the capture → structure → store loop in its thinnest form.

- **`WHITEPAPER.md`** — the step-by-step guide. Start here.
- **`SPRINT.md`** — the 5-day checklist to work through.
- **`supabase/migrations/0001_init.sql`** — schema + RLS. Run once in Supabase.

## Important: scaffold first, then drop these files in

These are source files, not a full project. Create a fresh Expo app, then copy
this repo's `App.tsx`, `env.d.ts`, `lib/`, `navigation/`, `screens/`, `supabase/`,
`.env.example`, and `.github/` into it.

```bash
npx create-expo-app@latest keep-in-touch --template blank-typescript
cd keep-in-touch
# copy the files from this starter into the project, then:
npx expo install @supabase/supabase-js @react-native-async-storage/async-storage \
  react-native-url-polyfill @react-navigation/native @react-navigation/native-stack \
  react-native-screens react-native-safe-area-context
cp .env.example .env   # then fill in your Supabase URL + anon key
npx expo start
```

Open **Expo Go** on your phone and scan the QR code. Full details, including the
Supabase setup and how to verify RLS, are in `WHITEPAPER.md`.
