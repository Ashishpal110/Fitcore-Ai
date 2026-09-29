import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, DateTime, ForeignKey, String, Table, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.guid import GUID

if TYPE_CHECKING:
    from app.models.exercise import Exercise


# Association Tables (Many-to-Many)
exercise_modalities = Table(
    "exercise_modalities",
    Base.metadata,
    Column(
        "exercise_id",
        GUID,
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "modality_id",
        GUID,
        ForeignKey("training_modalities.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)

exercise_equipment = Table(
    "exercise_equipment",
    Base.metadata,
    Column(
        "exercise_id",
        GUID,
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "equipment_id",
        GUID,
        ForeignKey("equipment.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)

exercise_locations = Table(
    "exercise_locations",
    Base.metadata,
    Column(
        "exercise_id",
        GUID,
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "location_id",
        GUID,
        ForeignKey("locations.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)

exercise_secondary_muscles = Table(
    "exercise_secondary_muscles",
    Base.metadata,
    Column(
        "exercise_id",
        GUID,
        ForeignKey("exercises.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "muscle_id",
        GUID,
        ForeignKey("muscles.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)


class ExerciseCategory(Base):
    """Categorical grouping for exercises (e.g. Chest, Back, Legs, Cardio)."""
    __tablename__ = "exercise_categories"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
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
    exercises: Mapped[List["Exercise"]] = relationship(
        "Exercise",
        back_populates="category",
    )

    def __repr__(self) -> str:
        return f"<ExerciseCategory id={self.id} name={self.name}>"


class TrainingModality(Base):
    """Training style or methodology (e.g. Strength, Cardio, HIIT, Calisthenics)."""
    __tablename__ = "training_modalities"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
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
    exercises: Mapped[List["Exercise"]] = relationship(
        "Exercise",
        secondary=exercise_modalities,
        back_populates="modalities",
    )

    def __repr__(self) -> str:
        return f"<TrainingModality id={self.id} name={self.name}>"


class Equipment(Base):
    """Gear or machinery used for exercises (e.g. Barbell, Dumbbell, Bodyweight)."""
    __tablename__ = "equipment"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
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
    exercises: Mapped[List["Exercise"]] = relationship(
        "Exercise",
        secondary=exercise_equipment,
        back_populates="equipment",
    )

    def __repr__(self) -> str:
        return f"<Equipment id={self.id} name={self.name}>"


class Muscle(Base):
    """Anatomical muscle group target (e.g. Pectoralis Major, Latissimus Dorsi)."""
    __tablename__ = "muscles"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    body_part: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
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
    primary_exercises: Mapped[List["Exercise"]] = relationship(
        "Exercise",
        foreign_keys="Exercise.primary_muscle_id",
        back_populates="primary_muscle",
    )
    secondary_exercises: Mapped[List["Exercise"]] = relationship(
        "Exercise",
        secondary=exercise_secondary_muscles,
        back_populates="secondary_muscles",
    )

    def __repr__(self) -> str:
        return f"<Muscle id={self.id} name={self.name} body_part={self.body_part}>"


class ExerciseLocation(Base):
    """Training setting context (e.g. Gym, Home, Outdoors, Hotel/Travel)."""
    __tablename__ = "locations"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )
    description: Mapped[Optional[str]] = mapped_column(
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
    exercises: Mapped[List["Exercise"]] = relationship(
        "Exercise",
        secondary=exercise_locations,
        back_populates="locations",
    )

    def __repr__(self) -> str:
        return f"<ExerciseLocation id={self.id} name={self.name}>"
