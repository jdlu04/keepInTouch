-- ============================================================================
-- Keep in Touch — 0001_init.sql
-- Full schema + Row-Level Security, aligned with docs/mvp.md.
--
-- HOW TO RUN
--   Supabase Dashboard -> SQL Editor -> New query -> paste this whole file -> Run.
--   Run it once on a fresh project (or after dropping the old tables).
--
-- Every table has a `user_id` that defaults to auth.uid(), so the client never
-- has to send it. Combined with the RLS policies at the bottom, every row is
-- automatically scoped to the signed-in user.
-- ============================================================================

-- ─────────────────────────────── Tables ───────────────────────────────

-- PEOPLE — a contact (mvp.md "Contact")
create table public.people (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  full_name     text not null,
  relationship  text,          -- 'family' | 'friend' | 'classmate' | 'coworker' | 'mentor' | ...
  location      text,
  phone         text,
  email         text,
  social_media  text,
  squad_color   text,          -- visual grouping color, e.g. '#4F46E5'
  birthday      date,
  created_at    timestamptz not null default now()
);

-- INTERACTIONS — logged events (mvp.md "Interaction")
create table public.interactions (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null default auth.uid() references auth.users(id) on delete cascade,
  person_id    uuid not null references public.people(id) on delete cascade,
  type         text,           -- 'call' | 'message' | 'meeting' | 'event' | 'note'
  notes        text,
  occurred_at  timestamptz not null default now(),
  created_at   timestamptz not null default now()
);

-- REMINDERS — upcoming follow-ups and events (mvp.md "Reminder")
create table public.reminders (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null default auth.uid() references auth.users(id) on delete cascade,
  person_id    uuid not null references public.people(id) on delete cascade,
  title        text not null,
  due_date     date,
  completed    boolean not null default false,
  created_at   timestamptz not null default now()
);

-- CONNECTIONS — relationships between two contacts (mvp.md "Relationship Connection")
create table public.connections (
  id                 uuid primary key default gen_random_uuid(),
  user_id            uuid not null default auth.uid() references auth.users(id) on delete cascade,
  from_person        uuid not null references public.people(id) on delete cascade,
  to_person          uuid not null references public.people(id) on delete cascade,
  relationship_type  text,     -- 'spouse' | 'coworker' | 'introduced-by' | ...
  strength           int default 1,
  created_at         timestamptz not null default now()
);

-- ────────────────────────────── Indexes ───────────────────────────────
create index on public.people (user_id);
create index on public.interactions (person_id, occurred_at desc);
create index on public.reminders (person_id);
create index on public.reminders (due_date);
create index on public.connections (from_person);

-- ──────────────────────── Row-Level Security ──────────────────────────
-- Turn RLS on everywhere, then let the owner do everything and no one else
-- see anything. This is the privacy backbone — verify it by signing in as two
-- different users and confirming neither sees the other's rows.
alter table public.people       enable row level security;
alter table public.interactions enable row level security;
alter table public.reminders    enable row level security;
alter table public.connections  enable row level security;

create policy "owner_all" on public.people
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "owner_all" on public.interactions
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "owner_all" on public.reminders
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "owner_all" on public.connections
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
