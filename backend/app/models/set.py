import uuid
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.types import Enum as SQLEnum

from app.core.database import Base
from app.models.enums import DistanceUnit, SetType
from app.models.guid import GUID

if TYPE_CHECKING:
    from app.models.workout_exercise import WorkoutExercise


class Set(Base):
    """Set performed within a workout exercise."""
    __tablename__ = "sets"
    __table_args__ = (
        UniqueConstraint(
            "workout_exercise_id",
            "set_number",
            name="uq_sets_workout_exercise_set_number",
        ),
        CheckConstraint(
            "set_number > 0",
            name="ck_sets_set_number_positive",
        ),
        CheckConstraint(
            "reps IS NULL OR reps >= 0",
            name="ck_sets_reps_non_negative",
        ),
        CheckConstraint(
            "weight IS NULL OR weight >= 0",
            name="ck_sets_weight_non_negative",
        ),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds >= 0",
            name="ck_sets_duration_non_negative",
        ),
        CheckConstraint(
            "distance IS NULL OR distance >= 0",
            name="ck_sets_distance_non_negative",
        ),
        CheckConstraint(
            "calories IS NULL OR calories >= 0",
            name="ck_sets_calories_non_negative",
        ),
        CheckConstraint(
            "rpe IS NULL OR (rpe >= 1.0 AND rpe <= 10.0)",
            name="ck_sets_rpe_range",
        ),
        CheckConstraint(
            "rir IS NULL OR rir >= 0",
            name="ck_sets_rir_non_negative",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    workout_exercise_id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        ForeignKey("workout_exercises.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    set_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    set_type: Mapped[SetType] = mapped_column(
        SQLEnum(
            SetType,
            name="set_type",
            native_enum=False,
            values_callable=lambda obj: [e.value for e in obj],
        ),
        nullable=False,
        default=SetType.WORKING,
    )
    reps: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    weight: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(precision=7, scale=2),
        nullable=True,
        comment="Weight in kilograms (kg)",
    )
    duration_seconds: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Duration in seconds",
    )
    distance: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(precision=8, scale=2),
        nullable=True,
    )
    distance_unit: Mapped[Optional[DistanceUnit]] = mapped_column(
        SQLEnum(
            DistanceUnit,
            name="distance_unit",
            native_enum=False,
            values_callable=lambda obj: [e.value for e in obj],
        ),
        nullable=True,
    )
    calories: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(precision=7, scale=2),
        nullable=True,
        comment="Calories burned (kcal)",
    )
    rpe: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(precision=3, scale=1),
        nullable=True,
        comment="Rate of Perceived Exertion (1.0 - 10.0)",
    )
    rir: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Reps in Reserve (>= 0)",
    )
    is_warmup: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
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

    # Relationships
    workout_exercise: Mapped["WorkoutExercise"] = relationship(
        "WorkoutExercise",
        back_populates="sets",
    )

    @validates("set_type")
    def sync_set_type_warmup(self, key: str, value: SetType) -> SetType:
        """Ensure setting set_type to WARMUP automatically flags is_warmup as True."""
        if value == SetType.WARMUP or (isinstance(value, str) and value == SetType.WARMUP.value):
            self.is_warmup = True
        return value

    def __repr__(self) -> str:
        return (
            f"<Set id={self.id} workout_exercise_id={self.workout_exercise_id} "
            f"set_number={self.set_number} set_type={self.set_type}>"
        )
