-- ============================================================================
-- Keep in Touch — 0001_init.sql
-- Initial schema, pgvector, and Row-Level Security.
-- Paste this whole file into the Supabase SQL editor and run it once.
-- ============================================================================

-- pgvector powers semantic search over notes (Day 4+ / weeks 2-4).
create extension if not exists vector;

-- ─────────────────────────────── Tables ───────────────────────────────
-- Note: user_id defaults to auth.uid(), so the app never has to send it.
-- Combined with the RLS policies below, every row is automatically scoped
-- to the signed-in user.

-- PEOPLE — the hub record
create table public.people (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null default auth.uid() references auth.users(id) on delete cascade,
  full_name     text not null,
  age           int,
  relationship  text,                       -- 'family' | 'friend' | 'colleague' | ...
  birthday      date,
  created_at    timestamptz not null default now()
);

-- RELATIONSHIPS — who-knows-whom (self-referential edges between two people)
create table public.relationships (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null default auth.uid() references auth.users(id) on delete cascade,
  from_person  uuid not null references public.people(id) on delete cascade,
  to_person    uuid not null references public.people(id) on delete cascade,
  kind         text,                         -- 'spouse' | 'coworker' | 'introduced-by' | ...
  strength     int default 1,
  created_at   timestamptz not null default now()
);

-- ATTRIBUTES — flexible facts (interests, prefs, kids' names) as key/value
create table public.attributes (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null default auth.uid() references auth.users(id) on delete cascade,
  person_id   uuid not null references public.people(id) on delete cascade,
  key         text not null,
  value       text,
  created_at  timestamptz not null default now()
);

-- INTERACTIONS — logged events (calls, texts, meetups)
create table public.interactions (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null default auth.uid() references auth.users(id) on delete cascade,
  person_id    uuid not null references public.people(id) on delete cascade,
  channel      text,                         -- 'call' | 'text' | 'in-person' | 'email'
  summary      text,
  occurred_at  timestamptz not null default now(),
  created_at   timestamptz not null default now()
);

-- CADENCES — desired contact frequency per person
create table public.cadences (
  id              uuid primary key default gen_random_uuid(),
  user_id         uuid not null default auth.uid() references auth.users(id) on delete cascade,
  person_id       uuid not null references public.people(id) on delete cascade,
  every_days      int not null,              -- 30 = monthly, 7 = weekly, ...
  last_contacted  timestamptz,
  created_at      timestamptz not null default now()
);

-- NOTES — free text + embedding for semantic recall
create table public.notes (
  id          uuid primary key default gen_random_uuid(),
  user_id     uuid not null default auth.uid() references auth.users(id) on delete cascade,
  person_id   uuid references public.people(id) on delete cascade,
  body        text not null,
  embedding   vector(768),                   -- must match your embedding model's dims
  created_at  timestamptz not null default now()
);

-- ────────────────────────────── Indexes ───────────────────────────────
create index on public.people (user_id);
create index on public.interactions (person_id, occurred_at desc);
create index on public.attributes (person_id);
create index on public.cadences (person_id);
create index on public.relationships (from_person);

-- ──────────────────────── Row-Level Security ──────────────────────────
-- Turn RLS on for every table, then allow the owner to do everything and
-- no one else to see anything. This is the privacy backbone — verify it
-- works by signing in as two different users (see the white paper, Step 6).

alter table public.people        enable row level security;
alter table public.relationships enable row level security;
alter table public.attributes    enable row level security;
alter table public.interactions  enable row level security;
alter table public.cadences      enable row level security;
alter table public.notes         enable row level security;

create policy "owner_all" on public.people
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "owner_all" on public.relationships
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "owner_all" on public.attributes
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "owner_all" on public.interactions
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "owner_all" on public.cadences
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "owner_all" on public.notes
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
