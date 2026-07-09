"""SQLAlchemy ORM models — the database schema, defined in Python.

Access control is enforced in the API layer (every query filters by the
authenticated user's id), not by database RLS.
"""
import uuid
from datetime import date, datetime

from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base

DEFAULT_CATEGORIES = ["family", "friends", "classmates", "coworkers", "mentors"]

INTERACTION_TYPES = ("call", "message", "meeting", "event", "note")
REMINDER_TYPES = ("birthday", "anniversary", "follow-up", "gift", "other")


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String)

    # Settings-page preferences
    reminders_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    relationship_categories: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=lambda: list(DEFAULT_CATEGORIES),
        server_default="{family,friends,classmates,coworkers,mentors}",
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class Person(Base):
    __tablename__ = "people"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    relationship: Mapped[str | None] = mapped_column(String)  # category: friend / family / mentor…
    location: Mapped[str | None] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String)
    social_media: Mapped[str | None] = mapped_column(String)
    squad_color: Mapped[str | None] = mapped_column(String)  # hex for the map, e.g. '#4F46E5'
    birthday: Mapped[date | None] = mapped_column(Date)
    anniversary: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(Text)  # interests, memories, preferences
    is_favorite: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class Interaction(Base):
    __tablename__ = "interactions"
    __table_args__ = (
        CheckConstraint(
            "type in ('call','message','meeting','event','note')", name="interactions_type_check"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    person_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("people.id", ondelete="CASCADE"), index=True, nullable=False
    )
    type: Mapped[str] = mapped_column(String, nullable=False, default="note", server_default="note")
    notes: Mapped[str | None] = mapped_column(Text)
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())


class Reminder(Base):
    __tablename__ = "reminders"
    __table_args__ = (
        CheckConstraint(
            "type in ('birthday','anniversary','follow-up','gift','other')", name="reminders_type_check"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    # Nullable: a reminder can be general (not tied to one contact).
    person_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("people.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str] = mapped_column(String, nullable=False, default="follow-up", server_default="follow-up")
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class Connection(Base):
    __tablename__ = "connections"
    __table_args__ = (
        UniqueConstraint("user_id", "from_person", "to_person", name="connections_unique_edge"),
        CheckConstraint("from_person <> to_person", name="connections_distinct"),
        CheckConstraint("strength between 1 and 5", name="connections_strength_check"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    from_person: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("people.id", ondelete="CASCADE"), index=True, nullable=False
    )
    to_person: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("people.id", ondelete="CASCADE"), index=True, nullable=False
    )
    relationship_type: Mapped[str | None] = mapped_column(String)
    strength: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
