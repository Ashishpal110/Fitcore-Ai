import uuid
import pytest
from app.models.enums import DifficultyLevel, ExerciseTrackingType
from app.models.exercise import Exercise
from app.models.taxonomy import (
    Equipment,
    ExerciseCategory,
    ExerciseLocation,
    Muscle,
    TrainingModality,
)


def test_exercise_category_instantiation():
    """Verify ExerciseCategory model fields and repr."""
    category = ExerciseCategory(
        name="Chest",
        description="Upper body pushing movements targeting pectorals.",
    )
    assert category.name == "Chest"
    assert category.description == "Upper body pushing movements targeting pectorals."
    assert "Chest" in repr(category)


def test_training_modality_instantiation():
    """Verify TrainingModality model fields and repr."""
    modality = TrainingModality(
        name="Strength / Hypertrophy",
        description="Progressive resistance training focused on muscle hypertrophy.",
    )
    assert modality.name == "Strength / Hypertrophy"
    assert "Strength / Hypertrophy" in repr(modality)


def test_equipment_instantiation():
    """Verify Equipment model fields and repr."""
    equipment = Equipment(
        name="Barbell",
        description="Standard Olympic barbell and weight plates.",
    )
    assert equipment.name == "Barbell"
    assert "Barbell" in repr(equipment)


def test_muscle_instantiation():
    """Verify Muscle model fields and repr."""
    muscle = Muscle(
        name="Pectoralis Major",
        body_part="Chest",
        description="Primary chest muscle.",
    )
    assert muscle.name == "Pectoralis Major"
    assert muscle.body_part == "Chest"
    assert "Pectoralis Major" in repr(muscle)


def test_location_instantiation():
    """Verify ExerciseLocation model fields and repr."""
    location = ExerciseLocation(
        name="Commercial Gym",
        description="Full facility fitness center.",
    )
    assert location.name == "Commercial Gym"
    assert "Commercial Gym" in repr(location)


def test_exercise_with_taxonomy_attributes():
    """Verify Exercise model instantiation with taxonomy keys and DifficultyLevel enum."""
    cat_id = uuid.uuid4()
    muscle_id = uuid.uuid4()
    exercise = Exercise(
        name="Barbell Bench Press",
        description="Horizontal pressing movement.",
        category_id=cat_id,
        primary_muscle_id=muscle_id,
        difficulty=DifficultyLevel.INTERMEDIATE,
        tracking_type=ExerciseTrackingType.WEIGHT_REPS,
        is_system=True,
    )
    assert exercise.name == "Barbell Bench Press"
    assert exercise.category_id == cat_id
    assert exercise.primary_muscle_id == muscle_id
    assert exercise.difficulty == DifficultyLevel.INTERMEDIATE
    assert exercise.tracking_type == ExerciseTrackingType.WEIGHT_REPS
    assert exercise.is_system is True
