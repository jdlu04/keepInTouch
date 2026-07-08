-- ============================================================================
-- Optional seed data for Keep in Touch.
-- Run this AFTER 0001_init.sql, and after at least one user exists in
-- auth.users (create one in Dashboard -> Authentication -> Users -> Add user,
-- or sign up from the app once auth is built).
--
-- HOW TO RUN
--   Supabase Dashboard -> SQL Editor -> New query -> paste this file -> Run.
--   By default it seeds the FIRST user in auth.users. If your project has
--   several users, hardcode your own id instead (see the `uid` line below):
--     select id, email from auth.users;   -- find yours
--
-- RE-RUNNING / STARTING OVER
--   This inserts fresh rows every time. To wipe previous seed rows first
--   (deletes ALL of that user's data), uncomment the cleanup block below.
-- ============================================================================

do $$
declare
  uid uuid := (select id from auth.users order by created_at asc limit 1);
  -- uid uuid := '00000000-0000-0000-0000-000000000000';  -- or hardcode your id
  priya  uuid;
  marcus uuid;
  amara  uuid;
begin
  if uid is null then
    raise exception 'No user found in auth.users — create a user first.';
  end if;

  -- Optional cleanup (uncomment to reset this user's data before seeding):
  -- delete from public.reminders    where user_id = uid;
  -- delete from public.interactions where user_id = uid;
  -- delete from public.connections  where user_id = uid;
  -- delete from public.people       where user_id = uid;

  -- ── Contacts ─────────────────────────────────────────────────────────────
  insert into public.people
    (user_id, full_name, relationship, location, phone, email, social_media, squad_color, birthday)
  values
    (uid, 'Priya Sharma', 'friend', 'Brooklyn, NY',
     '+1 212 555 0142', 'priya.sharma@example.com', '@priyamakes', '#4F46E5', '1996-03-12')
    returning id into priya;

  insert into public.people
    (user_id, full_name, relationship, location, email, squad_color)
  values
    (uid, 'Marcus Lee', 'colleague', 'Manhattan, NY', 'marcus.lee@example.com', '#059669')
    returning id into marcus;

  insert into public.people
    (user_id, full_name, relationship, location, squad_color, birthday)
  values
    (uid, 'Amara Okafor', 'mentor', 'Jersey City, NJ', '#DC2626', '1991-09-02')
    returning id into amara;

  -- ── Interactions (relationship history) ──────────────────────────────────
  insert into public.interactions (user_id, person_id, type, notes, occurred_at) values
    (uid, priya,  'meeting', 'Coffee; she just started a pottery class.', now() - interval '3 days'),
    (uid, marcus, 'call',    'Synced on the demo prep for next week.',    now() - interval '10 days'),
    (uid, amara,  'message', 'Checked in about the mentorship call.',     now() - interval '1 day');

  -- ── Reminders (upcoming follow-ups / events) ─────────────────────────────
  insert into public.reminders (user_id, person_id, title, due_date, completed) values
    (uid, priya,  'Wish Priya luck on her thesis defense', '2026-07-14', false),
    (uid, marcus, 'Follow up after the demo',              '2026-07-10', false),
    (uid, amara,  'Schedule next mentorship call',         '2026-07-21', false);

  -- ── Connections (who knows whom) ─────────────────────────────────────────
  insert into public.connections (user_id, from_person, to_person, relationship_type, strength) values
    (uid, priya, marcus, 'introduced-by', 2),
    (uid, amara, marcus, 'coworker',      1);
end $$;
