# Keep in Touch — From Zero to a Working Skeleton

### A step-by-step guide for the Hack Your Summer team

This white paper walks a student team from an empty folder to a working,
single-user prototype of a personal relationship manager — running on a real
phone, backed by a real Postgres database, with private per-user data. It pairs
with the starter files in this repo and the `SPRINT.md` checklist. Everything
here uses free tools.

---

## 1. What you're building

A personal relationship manager — an external brain for the people in your life.
The product runs one loop:

> **Capture → AI structure → Sense → Resurface.**
> You say or type one sentence about an interaction. The app pulls out the facts
> and attaches them to a person. A cadence engine notices who's drifting. The app
> resurfaces the right context at the right time.

This skeleton implements the first three quarters of that loop end to end:
capture a sentence, structure it (optionally with a free LLM), and store it
against a person. The "sense / resurface" half — relationship-health scoring,
the home feed, nudges — is weeks 2–4 work and is intentionally out of scope here.

### The data model

| Table | Holds | Notes |
|---|---|---|
| `people` | the hub record | name, age, relationship, birthday |
| `relationships` | who-knows-whom | self-referential edges between two people |
| `attributes` | flexible facts | key/value (interests, prefs, kids' names) |
| `interactions` | logged events | calls, texts, meetups |
| `cadences` | desired frequency | drives "who's going cold" later |
| `notes` | free text + embedding | `vector(768)` column for semantic recall |

Everything hangs off `people`, and every row carries a `user_id` so one
database safely holds every user's private graph.

---

## 2. The stack and why

| Layer | Tool | Why this one |
|---|---|---|
| App (iOS/Android/web) | **Expo + React Native + TypeScript** | one codebase, three platforms; test on a real phone in seconds |
| Backend | **Supabase** (free tier) | Postgres + Auth + Realtime + Storage in one box; the prototype stack is the production stack |
| Privacy | **Row-Level Security** | the database itself enforces per-user isolation |
| AI (optional) | **Gemini free tier** | turns a sentence into structured facts at zero cost |
| Source + CI | **GitHub** (+ Student Pack) | private repos, free Copilot Pro, free Actions |

A note on "free": the Supabase free tier gives a 500 MB Postgres database and
50,000 monthly active users — far more than a prototype needs. The one catch:
**a free project pauses after about a week with no activity** and must be
manually restored from the dashboard, which takes ~30 seconds. Restore it before
any demo, or keep a scheduled request hitting it.

---

## 3. Before you start — accounts (15 minutes)

1. **GitHub** — every teammate signs up and claims the **Student Developer Pack**
   with their Stony Brook email. It unlocks Copilot Pro for free.
2. **Supabase** — one teammate creates a free account and a new project. Save the
   database password somewhere safe.
3. **Node.js** — install the current LTS on each machine.
4. **Expo Go** — install the app on each teammate's phone (App Store / Play Store).
5. **(Optional) Google AI Studio** — for the Day 4 AI step, grab a free Gemini
   API key at https://ai.google.dev.

---

## 4. Step 1 — Repo and team workflow

```bash
# one teammate, in the GitHub org:
# - create a private repo "keep-in-touch"
# - Settings -> Branches -> add a rule for `main`: require a pull request before merging
```

Everyone clones it. Agree on one rule now: **nothing lands on `main` without a
PR**. It feels heavy for a four-person team, but it's the habit that keeps the
build from breaking silently, and it's what the CI in Step 9 hooks into.

Drop the MVP scope into a GitHub Projects board as issues so work is visible.

---

## 5. Step 2 — Scaffold the app and install dependencies

```bash
npx create-expo-app@latest keep-in-touch --template blank-typescript
cd keep-in-touch
```

Then add the libraries. Use `npx expo install` (not plain `npm install`) so the
versions match your Expo SDK:

```bash
npx expo install @supabase/supabase-js @react-native-async-storage/async-storage \
  react-native-url-polyfill @react-navigation/native @react-navigation/native-stack \
  react-native-screens react-native-safe-area-context
```

Now copy the starter files from this repo into the scaffolded project:
`App.tsx`, `env.d.ts`, `lib/`, `navigation/`, `screens/`, `supabase/`,
`.env.example`, and `.github/`.

---

## 6. Step 3 — Database schema and Row-Level Security

In the Supabase dashboard, open the **SQL editor**, paste the entire contents of
`supabase/migrations/0001_init.sql`, and run it. This creates the six tables,
turns on `pgvector`, and — most importantly — enables RLS with an `owner_all`
policy on every table.

### What RLS is actually doing

Each table has a `user_id` column that defaults to `auth.uid()` — the id of
whoever is signed in. The policy says:

```sql
using (auth.uid() = user_id) with check (auth.uid() = user_id)
```

`using` filters what you can read; `with check` constrains what you can write.
Together they mean a signed-in user can only ever touch their own rows — enforced
inside the database, not in app code you might forget to write. This is the
single most important thing to get right, because it's the privacy backbone of
the whole product. You verify it for real in Step 6.

---

## 7. Step 4 — Connect the app to Supabase

Copy `.env.example` to `.env` and fill in the two values from Supabase
(**Settings → API**):

```
EXPO_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=your-anon-public-key
```

The `EXPO_PUBLIC_` prefix is what makes these readable from the app at runtime.
`lib/supabase.ts` reads them and configures the client to persist the session on
the device with AsyncStorage. Start the app:

```bash
npx expo start
```

Scan the QR code with Expo Go. You should see the sign-in screen.

---

## 8. Step 5 — Auth (passwordless email codes)

`screens/SignInScreen.tsx` uses email OTP: you enter your email, Supabase emails
a 6-digit code, you type it in. We chose this over magic links on purpose —
magic links need deep-link configuration in Expo, which is the most common place
beginners lose a day. OTP needs none of that.

`App.tsx` listens to `supabase.auth.onAuthStateChange`. The moment the code
verifies, the session flips and the app routes you from the sign-in screen into
the people list. No manual navigation needed.

> If the code email never arrives, check spam, and confirm email auth is enabled
> under **Authentication → Providers** in Supabase (it is by default).

---

## 9. Step 6 — Read path, and proving RLS works

`screens/PeopleListScreen.tsx` queries `people` and renders the list. Notice the
query has **no `where user_id = ...` clause** — it doesn't need one, because RLS
filters the rows server-side. Add a couple of people with the input at the top.

Now the test that matters. **Sign in as a second teammate (a different email) on
another phone and add different people.** Each account must see only its own
list. If account A can ever see account B's data, stop everything and fix the
policy — that bug is the difference between a product people trust and one they
don't.

---

## 10. Step 7 — Write path and the AI capture spike

`screens/PersonDetailScreen.tsx` shows a person's attributes and interaction
history. `screens/LogInteractionScreen.tsx` is where the loop closes:

1. You type a sentence.
2. `lib/extract.ts` (if a Gemini key is set) asks the model to return JSON with a
   summary, a channel, and a list of facts.
3. The app writes the interaction, plus any extracted facts into `attributes`.

If no Gemini key is set, `extractFacts()` returns `null` and the app just stores
the raw sentence — nothing breaks. That's deliberate: the AI is an enhancement,
not a dependency.

To turn it on, set `EXPO_PUBLIC_GEMINI_API_KEY` in `.env` and restart. Confirm
the current free model name at https://ai.google.dev and update `MODEL` in
`lib/extract.ts` if needed.

> **Security:** calling the model directly from the app exposes your API key in
> the client bundle. That's acceptable for a prototype on your own device. Before
> you ship to anyone else, move this call into a **Supabase Edge Function** so the
> key stays server-side. That's a weeks-2–4 task; don't let it block the spike.

---

## 11. Step 8 — Seed some real data (optional)

The fastest way to get data is to use the app's "Add person" button while signed
in — `user_id` fills itself in. If you'd rather bulk-load, open
`supabase/seed.sql`, run `select id, email from auth.users;` to find your id,
paste it into the file, and run it.

---

## 12. Step 9 — Continuous integration

`.github/workflows/ci.yml` runs `tsc --noEmit` on every pull request, so type
errors get caught before they reach `main`. It's intentionally tiny — one job,
one check. Add lint or tests later if you want; don't gold-plate CI in week one.

---

## 13. Step 10 — Design and talk to humans

With the skeleton working, spend Day 5 on the things that decide whether anyone
keeps using this:

- **Wireframe four screens** in Figma's free tier or Excalidraw: the home feed,
  the person card, the capture screen, and the pre-interaction brief. Don't build
  them yet — sketch them.
- **Interview 8–12 real people.** Ask: "Show me how you currently remember to
  follow up with someone." Watch what they actually do. This is worth more than
  any feature you'd add the same day.

---

## 14. Verify your setup

A quick set of checks that mirror how this skeleton was validated. Run them in
order; each has a clear pass signal.

**1. The app compiles.** From the project root:

```bash
npx tsc --noEmit
```

Expect no output and exit code 0. This checks every screen against the real
Supabase and navigation types, and — thanks to `env.d.ts` — passes even before
your first `expo start`. If you see errors, you're most likely missing a
dependency; re-run the `npx expo install ...` line from Step 2.

**2. The database is wired correctly.** In the Supabase SQL editor:

```sql
select tablename, rowsecurity
from pg_tables
where schemaname = 'public'
order by tablename;
```

Expect six rows — `attributes`, `cadences`, `interactions`, `notes`, `people`,
`relationships` — each with `rowsecurity = true`. If any row shows `false`,
re-run the `enable row level security` lines from the migration.

**3. RLS actually isolates users — the test that matters.** Sign in on one phone
as user A and add a person. Sign in on a second phone (or simulator) as user B
with a different email and add a different person. Each account must see only its
own list. If user B can ever see user A's data, stop and fix the policy before
going further — this is the privacy guarantee the whole product rests on.

**4. The capture loop works end to end.** Open a person, tap "Log an
interaction," type a sentence, and save. It should appear in that person's
history. With a Gemini key set, any facts in the sentence (e.g. an interest)
should also show up under "What you know."

If all four pass, your environment matches the tested baseline (Expo SDK 56,
React 19, supabase-js 2.x) and you're clear to start building.

---

## 15. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| App crashes on launch with a "Missing EXPO_PUBLIC_..." error | `.env` not filled in or app not restarted | Fill `.env`, stop and re-run `npx expo start` |
| People list is always empty | RLS working as intended but no rows for this user, **or** you're signed in as a different user than you seeded | Add people in-app while signed in; check `auth.users` for your id |
| Can see another user's data | RLS not enabled or policy missing | Re-run the `alter table ... enable row level security` and `create policy` lines |
| OTP email never arrives | spam, or wrong email | Check spam; confirm email provider is enabled in Supabase |
| App was working, now every request fails | Supabase free project **paused after 7 days idle** | Restore it from the dashboard (~30s) |
| AI extraction does nothing | no key, or stale model name | Set `EXPO_PUBLIC_GEMINI_API_KEY`; verify `MODEL` at ai.google.dev |

---

## 16. What's next (weeks 2–4)

- **Sense + Resurface:** compute a relationship-health signal from `cadences` and
  recent `interactions`; build the "your people" home feed and gentle nudges.
- **Embeddings:** fill the `notes.embedding` column and add semantic
  "who do I know who…" search.
- **Voice capture:** the real friction-killer — make logging a 5-second action.
- **Harden the AI path:** move the LLM call into a Supabase Edge Function.
- **Push notifications:** Expo push → FCM/APNs.

Keep the discipline from week one: scope to the loop, dogfood relentlessly, and
measure whether people come back on day 3 and day 7. That number is the product.
