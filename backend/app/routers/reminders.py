"""Reminders: the upcoming feed, CRUD, and birthday/anniversary generation."""
import uuid
from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_current_user, get_db
from ..services import reminders as reminder_service

router = APIRouter(prefix="/reminders", tags=["reminders"])


def _to_out(reminder: models.Reminder, person: Optional[models.Person], today: date) -> schemas.ReminderOut:
    return schemas.ReminderOut(
        id=reminder.id,
        person_id=reminder.person_id,
        person_name=person.full_name if person else None,
        squad_color=person.squad_color if person else None,
        title=reminder.title,
        type=reminder.type,
        due_date=reminder.due_date,
        days_until=(reminder.due_date - today).days,
        completed=reminder.completed,
    )


def _get_owned(db: Session, user: models.User, reminder_id: uuid.UUID) -> models.Reminder:
    reminder = db.get(models.Reminder, reminder_id)
    if reminder is None or reminder.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Reminder not found")
    return reminder


@router.get("", response_model=list[schemas.ReminderOut])
def list_reminders(
    days: Optional[int] = Query(None, ge=0, description="Only reminders due within N days"),
    include_completed: bool = Query(False),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    today = date.today()
    stmt = (
        select(models.Reminder, models.Person)
        .join(models.Person, models.Person.id == models.Reminder.person_id, isouter=True)
        .where(models.Reminder.user_id == user.id)
    )
    if not include_completed:
        stmt = stmt.where(models.Reminder.completed.is_(False))
    if days is not None:
        stmt = stmt.where(
            models.Reminder.due_date >= today,
            models.Reminder.due_date <= today + timedelta(days=days),
        )
    stmt = stmt.order_by(models.Reminder.due_date)

    return [_to_out(r, p, today) for r, p in db.execute(stmt).all()]


@router.post("", response_model=schemas.ReminderOut, status_code=status.HTTP_201_CREATED)
def create_reminder(
    payload: schemas.ReminderCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.person_id is not None:
        person = db.get(models.Person, payload.person_id)
        if person is None or person.user_id != user.id:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Contact not found")

    reminder = models.Reminder(user_id=user.id, **payload.model_dump())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    person = db.get(models.Person, reminder.person_id) if reminder.person_id else None
    return _to_out(reminder, person, date.today())


@router.post("/generate", response_model=schemas.GenerateResult)
def generate(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    created = reminder_service.generate_date_reminders(db, user)
    return schemas.GenerateResult(created=created)


@router.patch("/{reminder_id}", response_model=schemas.ReminderOut)
def update_reminder(
    reminder_id: uuid.UUID,
    payload: schemas.ReminderUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reminder = _get_owned(db, user, reminder_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(reminder, field, value)
    db.commit()
    db.refresh(reminder)
    person = db.get(models.Person, reminder.person_id) if reminder.person_id else None
    return _to_out(reminder, person, date.today())


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(
    reminder_id: uuid.UUID,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reminder = _get_owned(db, user, reminder_id)
    db.delete(reminder)
    db.commit()
