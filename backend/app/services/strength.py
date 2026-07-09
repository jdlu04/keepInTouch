"""Relationship-strength algorithm.

Strength (0–100) grows with how many times AND how recently you've interacted
with a contact, and fades as time passes since the last interaction:

    strength = min(100, interaction_count * 12 + recency_bonus)
    recency_bonus = 40 (<=1 week) | 25 (<=1 month) | 10 (<=3 months) | else 0

This drives node size and the strength legend on the relationship map.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .. import models


def compute_strength(interaction_count: int, last_interaction_at: datetime | None) -> int:
    bonus = 0
    if last_interaction_at is not None:
        last = last_interaction_at
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        days = (datetime.now(timezone.utc) - last).days
        if days <= 7:
            bonus = 40
        elif days <= 30:
            bonus = 25
        elif days <= 90:
            bonus = 10
    return min(100, interaction_count * 12 + bonus)


def interaction_stats(
    db: Session, person_ids: list[uuid.UUID]
) -> dict[uuid.UUID, tuple[int, datetime | None]]:
    """Return {person_id: (interaction_count, last_interaction_at)} in one query."""
    if not person_ids:
        return {}
    rows = db.execute(
        select(
            models.Interaction.person_id,
            func.count().label("count"),
            func.max(models.Interaction.occurred_at).label("last"),
        )
        .where(models.Interaction.person_id.in_(person_ids))
        .group_by(models.Interaction.person_id)
    ).all()
    return {r.person_id: (r.count, r.last) for r in rows}


def annotate(db: Session, people: list[models.Person]) -> list[dict]:
    """Turn Person rows into dicts with interaction_count/last_interaction_at/strength."""
    stats = interaction_stats(db, [p.id for p in people])
    result = []
    for p in people:
        count, last = stats.get(p.id, (0, None))
        data = {c.name: getattr(p, c.name) for c in p.__table__.columns}
        data["interaction_count"] = count
        data["last_interaction_at"] = last
        data["strength"] = compute_strength(count, last)
        result.append(data)
    return result
