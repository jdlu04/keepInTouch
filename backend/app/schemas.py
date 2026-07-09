"""Pydantic request/response models (the API's data contract)."""
import uuid
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr

InteractionType = Literal["call", "message", "meeting", "event", "note"]
ReminderType = Literal["birthday", "anniversary", "follow-up", "gift", "other"]


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── Auth / users ───────────────────────────────────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    display_name: Optional[str] = None


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    reminders_enabled: Optional[bool] = None
    notifications_enabled: Optional[bool] = None
    relationship_categories: Optional[list[str]] = None


class UserOut(ORMModel):
    id: uuid.UUID
    email: EmailStr
    display_name: Optional[str] = None
    reminders_enabled: bool
    notifications_enabled: bool
    relationship_categories: list[str]
    created_at: datetime


# ── People ───────────────────────────────────────────────────────────────
class PersonBase(BaseModel):
    full_name: str
    relationship: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    social_media: Optional[str] = None
    squad_color: Optional[str] = None
    birthday: Optional[date] = None
    anniversary: Optional[date] = None
    notes: Optional[str] = None
    is_favorite: bool = False


class PersonCreate(PersonBase):
    pass


class PersonUpdate(BaseModel):
    # All optional — only supplied fields are changed.
    full_name: Optional[str] = None
    relationship: Optional[str] = None
    location: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    social_media: Optional[str] = None
    squad_color: Optional[str] = None
    birthday: Optional[date] = None
    anniversary: Optional[date] = None
    notes: Optional[str] = None
    is_favorite: Optional[bool] = None


class PersonOut(ORMModel, PersonBase):
    id: uuid.UUID
    created_at: datetime


class PersonWithStrength(PersonOut):
    interaction_count: int
    last_interaction_at: Optional[datetime] = None
    strength: int  # 0–100


# ── Interactions ───────────────────────────────────────────────────────────
class InteractionCreate(BaseModel):
    type: InteractionType = "note"
    notes: Optional[str] = None
    occurred_at: Optional[datetime] = None


class InteractionOut(ORMModel):
    id: uuid.UUID
    person_id: uuid.UUID
    type: InteractionType
    notes: Optional[str] = None
    occurred_at: datetime
    created_at: datetime


class InteractionLogged(BaseModel):
    """Returned after logging an interaction: the row + the recomputed strength."""
    interaction: InteractionOut
    strength: int


# ── Reminders ────────────────────────────────────────────────────────────
class ReminderCreate(BaseModel):
    title: str
    type: ReminderType = "follow-up"
    due_date: date
    person_id: Optional[uuid.UUID] = None
    completed: bool = False


class ReminderUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[ReminderType] = None
    due_date: Optional[date] = None
    person_id: Optional[uuid.UUID] = None
    completed: Optional[bool] = None


class ReminderOut(ORMModel):
    id: uuid.UUID
    person_id: Optional[uuid.UUID] = None
    person_name: Optional[str] = None
    squad_color: Optional[str] = None
    title: str
    type: ReminderType
    due_date: date
    days_until: int
    completed: bool


class GenerateResult(BaseModel):
    created: int


# ── Connections ────────────────────────────────────────────────────────────
class ConnectionCreate(BaseModel):
    from_person: uuid.UUID
    to_person: uuid.UUID
    relationship_type: Optional[str] = None
    strength: int = 1


class ConnectionOut(ORMModel):
    id: uuid.UUID
    from_person: uuid.UUID
    to_person: uuid.UUID
    relationship_type: Optional[str] = None
    strength: int
    created_at: datetime
