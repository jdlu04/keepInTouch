"""Interaction timeline for a contact. Logging an interaction returns the
contact's freshly recomputed relationship strength."""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_current_user, get_db
from ..services import strength

router = APIRouter(tags=["interactions"])


def _get_owned_person(db: Session, user: models.User, person_id: uuid.UUID) -> models.Person:
    person = db.get(models.Person, person_id)
    if person is None or person.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Contact not found")
    return person


@router.get("/people/{person_id}/interactions", response_model=list[schemas.InteractionOut])
def list_interactions(
    person_id: uuid.UUID,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _get_owned_person(db, user, person_id)
    rows = db.execute(
        select(models.Interaction)
        .where(models.Interaction.person_id == person_id)
        .order_by(models.Interaction.occurred_at.desc())
    ).scalars().all()
    return rows


@router.post(
    "/people/{person_id}/interactions",
    response_model=schemas.InteractionLogged,
    status_code=status.HTTP_201_CREATED,
)
def log_interaction(
    person_id: uuid.UUID,
    payload: schemas.InteractionCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    person = _get_owned_person(db, user, person_id)
    data = payload.model_dump(exclude_unset=True)
    interaction = models.Interaction(user_id=user.id, person_id=person.id, **data)
    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    annotated = strength.annotate(db, [person])[0]
    return schemas.InteractionLogged(interaction=interaction, strength=annotated["strength"])


@router.delete("/interactions/{interaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_interaction(
    interaction_id: uuid.UUID,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interaction = db.get(models.Interaction, interaction_id)
    if interaction is None or interaction.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Interaction not found")
    db.delete(interaction)
    db.commit()
