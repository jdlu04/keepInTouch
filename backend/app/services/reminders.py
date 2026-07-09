"""Reminder logic: birthday/anniversary generation and the upcoming feed."""
import uuid
from datetime import date

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from .. import models


def next_anniversary(d: date, today: date | None = None) -> date:
    """Next time this month/day occurs, on or after today. Handles Feb 29."""
    today = today or date.today()

    def on_year(year: int) -> date:
        try:
            return d.replace(year=year)
        except ValueError:  # Feb 29 in a non-leap year -> clamp to Feb 28
            return date(year, 2, 28)

    occ = on_year(today.year)
    if occ < today:
        occ = on_year(today.year + 1)
    return occ


def generate_date_reminders(db: Session, user: models.User) -> int:
    """Ensure every contact with a birthday/anniversary has an upcoming reminder
    for its next occurrence. Idempotent — skips reminders that already exist for
    that person + type + date. Returns the number created.
    """
    today = date.today()
    people = db.execute(
        select(models.Person).where(models.Person.user_id == user.id)
    ).scalars().all()

    created = 0
    for person in people:
        for field, rtype, label in (
            (person.birthday, "birthday", "birthday"),
            (person.anniversary, "anniversary", "anniversary"),
        ):
            if field is None:
                continue
            due = next_anniversary(field, today)
            exists = db.execute(
                select(models.Reminder.id).where(
                    and_(
                        models.Reminder.person_id == person.id,
                        models.Reminder.type == rtype,
                        models.Reminder.due_date == due,
                    )
                )
            ).first()
            if exists:
                continue
            db.add(
                models.Reminder(
                    user_id=user.id,
                    person_id=person.id,
                    title=f"{person.full_name}'s {label}",
                    type=rtype,
                    due_date=due,
                )
            )
            created += 1

    if created:
        db.commit()
    return created
