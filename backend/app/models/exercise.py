import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Enum as SQLEnum

from app.core.database import Base
from app.models.enums import DifficultyLevel, ExerciseTrackingType
from app.models.guid import GUID

if TYPE_CHECKING:
    from app.models.taxonomy import (
        Equipment,
        ExerciseCategory,
        ExerciseLocation,
        Muscle,
        TrainingModality,
    )
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
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID,
        ForeignKey("exercise_categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    primary_muscle_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID,
        ForeignKey("muscles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    difficulty: Mapped[DifficultyLevel] = mapped_column(
        SQLEnum(
            DifficultyLevel,
            name="difficulty_level",
            native_enum=False,
            values_callable=lambda obj: [e.value for e in obj],
        ),
        nullable=False,
        default=DifficultyLevel.BEGINNER,
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
    category: Mapped[Optional["ExerciseCategory"]] = relationship(
        "ExerciseCategory",
        back_populates="exercises",
        lazy="selectin",
    )
    primary_muscle: Mapped[Optional["Muscle"]] = relationship(
        "Muscle",
        foreign_keys=[primary_muscle_id],
        back_populates="primary_exercises",
        lazy="selectin",
    )
    secondary_muscles: Mapped[List["Muscle"]] = relationship(
        "Muscle",
        secondary="exercise_secondary_muscles",
        back_populates="secondary_exercises",
        lazy="selectin",
    )
    modalities: Mapped[List["TrainingModality"]] = relationship(
        "TrainingModality",
        secondary="exercise_modalities",
        back_populates="exercises",
        lazy="selectin",
    )
    equipment: Mapped[List["Equipment"]] = relationship(
        "Equipment",
        secondary="exercise_equipment",
        back_populates="exercises",
        lazy="selectin",
    )
    locations: Mapped[List["ExerciseLocation"]] = relationship(
        "ExerciseLocation",
        secondary="exercise_locations",
        back_populates="exercises",
        lazy="selectin",
    )
    workout_exercises: Mapped[List["WorkoutExercise"]] = relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<Exercise id={self.id} name={self.name} tracking_type={self.tracking_type}>"
