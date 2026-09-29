import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.guid import GUID

if TYPE_CHECKING:
    from app.models.exercise import Exercise
    from app.models.set import Set
    from app.models.workout import Workout


class WorkoutExercise(Base):
    """Exercise performed within a specific workout session."""
    __tablename__ = "workout_exercises"
    __table_args__ = (
        CheckConstraint("order_index >= 0", name="ck_workout_exercises_order_index_non_negative"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    workout_id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        ForeignKey("workouts.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exercise_id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        ForeignKey("exercises.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    workout: Mapped["Workout"] = relationship(
        "Workout",
        back_populates="workout_exercises",
        lazy="selectin",
    )
    exercise: Mapped["Exercise"] = relationship(
        "Exercise",
        back_populates="workout_exercises",
        lazy="selectin",
    )
    sets: Mapped[List["Set"]] = relationship(
        "Set",
        back_populates="workout_exercise",
        cascade="all, delete-orphan",
        order_by="Set.set_number",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<WorkoutExercise id={self.id} workout_id={self.workout_id} exercise_id={self.exercise_id} order={self.order_index}>"
