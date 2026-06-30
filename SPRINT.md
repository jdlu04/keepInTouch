# SPRINT.md — first 5 days

Goal: end the week with a working skeleton (auth + per-user data + the capture
loop), plus design and user-research foundations. Assumes a few focused hours a
day, split across the team. Divide ownership up front — suggested owners in
brackets. Check items off as you go.

## Day 1 — Accounts, repo, "hello world on a phone" [everyone]
- [ ] Each teammate claims the **GitHub Student Developer Pack** (.edu email) → free Copilot Pro
- [ ] Create a GitHub **org** + one **private repo**; turn on branch protection (PRs only, no direct push to `main`)
- [ ] Add `README`, `.gitignore`, `.env.example`; agree that secrets live in `.env` (never committed)
- [ ] Create the free **Supabase** project; copy URL + anon key into each person's local `.env`
- [ ] Install Node LTS; run `npx create-expo-app@latest --template blank-typescript`
- [ ] Everyone installs **Expo Go** and confirms the starter app loads on their phone
- [ ] Stand up a **GitHub Projects** board; paste the MVP scope in as issues
- **Done when:** the starter app runs on every teammate's phone.

## Day 2 — Schema + Row-Level Security [backend owner]
- [ ] Sketch the data model in Excalidraw / dbdiagram.io
- [ ] Run `supabase/migrations/0001_init.sql` in the Supabase SQL editor
- [ ] Confirm **RLS is enabled** and the `owner_all` policy exists on every table
- [ ] Confirm the `vector` extension is enabled (for embeddings later)
- [ ] Run `npx supabase gen types typescript` (optional but nice) for typed tables
- **Done when:** all six tables exist with RLS on.

## Day 3 — Auth + read path [app owner]
- [ ] Copy `lib/supabase.ts`, `App.tsx`, `screens/SignInScreen.tsx`, `screens/PeopleListScreen.tsx` in
- [ ] Sign in via email OTP on a real phone
- [ ] Add a few people; confirm they appear in the list
- [ ] **Verify RLS:** sign in as a second teammate; confirm you see *only* your own people
- [ ] Open the first PR through the protected branch
- **Done when:** two accounts each see only their own data.

## Day 4 — Write path + AI capture spike [app owner + AI owner]
- [ ] Copy `screens/PersonDetailScreen.tsx`, `screens/LogInteractionScreen.tsx`, `lib/extract.ts` in
- [ ] Log a raw interaction; confirm it shows on the person's detail screen
- [ ] (AI owner) Get a free **Gemini** key at ai.google.dev; set `EXPO_PUBLIC_GEMINI_API_KEY`
- [ ] Log a sentence and confirm facts get extracted into `attributes`
- **Done when:** one sentence → a structured interaction + facts on the person card.

## Day 5 — Design, real users, groom [design owner + everyone]
- [ ] Wireframe 4 screens in Figma / Excalidraw: home feed, person card, capture, pre-interaction brief
- [ ] Each teammate runs 2–3 user interviews ("how do you remember to follow up?")
- [ ] Add the CI workflow (`.github/workflows/ci.yml`); confirm it runs on a PR
- [ ] Demo the slice to each other; write down what broke
- [ ] Groom the board for weeks 2–4
- **Done when:** a clickable slice + ~8–12 interview notes + a groomed backlog.

## Standing reminders
- [ ] Keep the Supabase project awake — free projects **pause after 7 days idle** and must be restored before a demo.
- [ ] Don't hand-roll auth or storage; let Supabase do it.
- [ ] The metric is **retention**, not feature count. Protect time to test with real people.
