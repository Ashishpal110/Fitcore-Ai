import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SQLEnum

from app.core.database import Base
from app.models.enums import ExerciseTrackingType
from app.models.guid import GUID

if TYPE_CHECKING:
    from app.models.workout_exercise import WorkoutExercise


class Exercise(Base):
    """Reusable exercise definition entity."""
    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    tracking_type: Mapped[ExerciseTrackingType] = mapped_column(
        SQLEnum(
            ExerciseTrackingType,
            name="exercise_tracking_type",
            native_enum=False,
            values_callable=lambda obj: [e.value for e in obj],
        ),
        nullable=False,
        default=ExerciseTrackingType.WEIGHT_REPS,
    )
    is_system: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
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
    workout_exercises: Mapped[List["WorkoutExercise"]] = relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Exercise id={self.id} name={self.name} tracking_type={self.tracking_type}>"
