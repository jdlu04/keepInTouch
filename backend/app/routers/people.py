"""Contacts CRUD, each annotated with computed relationship strength."""
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_current_user, get_db
from ..services import strength

router = APIRouter(prefix="/people", tags=["people"])


def _get_owned(db: Session, user: models.User, person_id: uuid.UUID) -> models.Person:
    person = db.get(models.Person, person_id)
    if person is None or person.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Contact not found")
    return person


@router.get("", response_model=list[schemas.PersonWithStrength])
def list_people(
    q: Optional[str] = Query(None, description="Search by name"),
    relationship: Optional[str] = Query(None, description="Filter by category"),
    favorite: Optional[bool] = Query(None, description="Only favorites when true"),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    stmt = select(models.Person).where(models.Person.user_id == user.id)
    if q:
        stmt = stmt.where(models.Person.full_name.ilike(f"%{q}%"))
    if relationship:
        stmt = stmt.where(models.Person.relationship == relationship)
    if favorite is not None:
        stmt = stmt.where(models.Person.is_favorite.is_(favorite))
    stmt = stmt.order_by(models.Person.full_name)

    people = db.execute(stmt).scalars().all()
    return strength.annotate(db, list(people))


@router.post("", response_model=schemas.PersonWithStrength, status_code=status.HTTP_201_CREATED)
def create_person(
    payload: schemas.PersonCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    person = models.Person(user_id=user.id, **payload.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return strength.annotate(db, [person])[0]


@router.get("/{person_id}", response_model=schemas.PersonWithStrength)
def get_person(
    person_id: uuid.UUID,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    person = _get_owned(db, user, person_id)
    return strength.annotate(db, [person])[0]


@router.patch("/{person_id}", response_model=schemas.PersonWithStrength)
def update_person(
    person_id: uuid.UUID,
    payload: schemas.PersonUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    person = _get_owned(db, user, person_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(person, field, value)
    db.commit()
    db.refresh(person)
    return strength.annotate(db, [person])[0]


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(
    person_id: uuid.UUID,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    person = _get_owned(db, user, person_id)
    db.delete(person)
    db.commit()
