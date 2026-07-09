"""Edges between two contacts — the data behind the relationship map."""
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..deps import get_current_user, get_db

router = APIRouter(prefix="/connections", tags=["connections"])


@router.get("", response_model=list[schemas.ConnectionOut])
def list_connections(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.execute(
        select(models.Connection).where(models.Connection.user_id == user.id)
    ).scalars().all()


@router.post("", response_model=schemas.ConnectionOut, status_code=status.HTTP_201_CREATED)
def create_connection(
    payload: schemas.ConnectionCreate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.from_person == payload.to_person:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "A contact cannot connect to itself")
    if not (1 <= payload.strength <= 5):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "strength must be between 1 and 5")

    # Both endpoints must be contacts owned by this user.
    owned = db.execute(
        select(models.Person.id).where(
            models.Person.user_id == user.id,
            models.Person.id.in_([payload.from_person, payload.to_person]),
        )
    ).scalars().all()
    if set(owned) != {payload.from_person, payload.to_person}:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Both contacts must exist and be yours")

    connection = models.Connection(user_id=user.id, **payload.model_dump())
    db.add(connection)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "That connection already exists")
    db.refresh(connection)
    return connection


@router.delete("/{connection_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_connection(
    connection_id: uuid.UUID,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    connection = db.get(models.Connection, connection_id)
    if connection is None or connection.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Connection not found")
    db.delete(connection)
    db.commit()
