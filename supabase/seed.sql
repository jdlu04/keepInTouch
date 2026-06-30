-- ============================================================================
-- Optional seed data. Run this AFTER you have signed in to the app at least
-- once (so your user exists in auth.users).
--
-- 1) Find your user id:   select id, email from auth.users;
-- 2) Paste it into `uid` below, then run this whole block.
-- ============================================================================

do $$
declare
  uid uuid := '00000000-0000-0000-0000-000000000000';  -- <-- your auth.users.id
  p1  uuid;
  p2  uuid;
begin
  insert into public.people (user_id, full_name, age, relationship, birthday)
    values (uid, 'Priya Sharma', 29, 'friend', '1996-03-12') returning id into p1;

  insert into public.people (user_id, full_name, relationship)
    values (uid, 'Marcus Lee', 'colleague') returning id into p2;

  insert into public.attributes (user_id, person_id, key, value) values
    (uid, p1, 'interest', 'pottery'),
    (uid, p1, 'topic', 'thesis defense in March');

  insert into public.interactions (user_id, person_id, channel, summary)
    values (uid, p1, 'in-person', 'Coffee; she just started a pottery class.');

  insert into public.cadences (user_id, person_id, every_days, last_contacted)
    values (uid, p1, 30, now());

  insert into public.relationships (user_id, from_person, to_person, kind)
    values (uid, p1, p2, 'introduced-by');
end $$;
