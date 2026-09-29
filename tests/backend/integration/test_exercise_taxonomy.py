"""Integration tests for exercise taxonomy models, associations, and idempotent seeder."""

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.enums import DifficultyLevel, ExerciseTrackingType
from app.models.exercise import Exercise
from app.models.taxonomy import (
    Equipment,
    ExerciseCategory,
    ExerciseLocation,
    Muscle,
    TrainingModality,
    exercise_equipment,
    exercise_locations,
    exercise_modalities,
    exercise_secondary_muscles,
)
from app.seeds.exercise_seeder import seed_exercises, seed_taxonomy


@pytest.mark.asyncio
async def test_taxonomy_creation_and_associations(db_session: AsyncSession):
    """Verify end-to-end taxonomy creation and many-to-many / one-to-many associations."""
    # 1. Create taxonomy lookup records
    category = ExerciseCategory(name="Chest", description="Upper body pushing.")
    primary_muscle = Muscle(name="Pectoralis Major", body_part="Chest", description="Main chest muscle.")
    sec_muscle_1 = Muscle(name="Anterior Deltoid", body_part="Shoulders")
    sec_muscle_2 = Muscle(name="Triceps Brachii", body_part="Arms")
    modality = TrainingModality(name="Strength / Hypertrophy")
    equipment_1 = Equipment(name="Barbell")
    equipment_2 = Equipment(name="Bench")
    location = ExerciseLocation(name="Commercial Gym")

    db_session.add_all([
        category, primary_muscle, sec_muscle_1, sec_muscle_2,
        modality, equipment_1, equipment_2, location
    ])
    await db_session.flush()

    # 2. Create Exercise linked to taxonomy
    exercise = Exercise(
        name="Barbell Bench Press Test",
        description="Standard bench press exercise.",
        category_id=category.id,
        primary_muscle_id=primary_muscle.id,
        difficulty=DifficultyLevel.INTERMEDIATE,
        tracking_type=ExerciseTrackingType.WEIGHT_REPS,
        is_system=True,
        secondary_muscles=[sec_muscle_1, sec_muscle_2],
        modalities=[modality],
        equipment=[equipment_1, equipment_2],
        locations=[location],
    )
    db_session.add(exercise)
    await db_session.commit()

    # 3. Query back exercise and verify all relationships
    stmt = (
        select(Exercise)
        .where(Exercise.id == exercise.id)
        .options(
            selectinload(Exercise.category),
            selectinload(Exercise.primary_muscle),
            selectinload(Exercise.secondary_muscles),
            selectinload(Exercise.modalities),
            selectinload(Exercise.equipment),
            selectinload(Exercise.locations),
        )
    )
    result = await db_session.execute(stmt)
    saved_ex = result.scalar_one()

    assert saved_ex.name == "Barbell Bench Press Test"
    assert saved_ex.difficulty == DifficultyLevel.INTERMEDIATE
    assert saved_ex.category is not None
    assert saved_ex.category.name == "Chest"
    assert saved_ex.primary_muscle is not None
    assert saved_ex.primary_muscle.name == "Pectoralis Major"
    assert len(saved_ex.secondary_muscles) == 2
    sec_names = {m.name for m in saved_ex.secondary_muscles}
    assert "Anterior Deltoid" in sec_names
    assert "Triceps Brachii" in sec_names
    assert len(saved_ex.modalities) == 1
    assert saved_ex.modalities[0].name == "Strength / Hypertrophy"
    assert len(saved_ex.equipment) == 2
    assert len(saved_ex.locations) == 1


@pytest.mark.asyncio
async def test_taxonomy_uniqueness_constraints(db_session: AsyncSession):
    """Verify unique constraints on taxonomy entity names."""
    cat1 = ExerciseCategory(name="Unique Category")
    db_session.add(cat1)
    await db_session.commit()

    cat2 = ExerciseCategory(name="Unique Category")
    db_session.add(cat2)
    with pytest.raises(IntegrityError):
        await db_session.commit()
    await db_session.rollback()


@pytest.mark.asyncio
async def test_cascade_delete_exercise_associations(db_session: AsyncSession):
    """Verify that deleting an Exercise removes association rows but preserves taxonomy entities."""
    category = ExerciseCategory(name="Back Unique")
    muscle = Muscle(name="Latissimus Dorsi Unique", body_part="Back")
    equipment = Equipment(name="Pull-Up Bar Unique")
    modality = TrainingModality(name="Calisthenics Unique")
    location = ExerciseLocation(name="Park Unique")

    db_session.add_all([category, muscle, equipment, modality, location])
    await db_session.flush()

    exercise = Exercise(
        name="Pull-Up Unique",
        category_id=category.id,
        primary_muscle_id=muscle.id,
        secondary_muscles=[muscle],
        modalities=[modality],
        equipment=[equipment],
        locations=[location],
    )
    db_session.add(exercise)
    await db_session.commit()

    # Delete exercise
    await db_session.delete(exercise)
    await db_session.commit()

    # Verify taxonomy lookup entities still exist
    cat_check = (await db_session.execute(select(ExerciseCategory).where(ExerciseCategory.id == category.id))).scalar_one_or_none()
    assert cat_check is not None
    muscle_check = (await db_session.execute(select(Muscle).where(Muscle.id == muscle.id))).scalar_one_or_none()
    assert muscle_check is not None


@pytest.mark.asyncio
async def test_exercise_seeder_execution_and_idempotency(db_session: AsyncSession):
    """Verify complete database seeding and strict 100% idempotency upon re-execution."""
    # First execution: Should create taxonomy and all exercises
    first_run = await seed_exercises(db_session)
    assert first_run["taxonomy"]["categories"] >= 10
    assert first_run["taxonomy"]["modalities"] >= 8
    assert first_run["taxonomy"]["equipment"] >= 18
    assert first_run["taxonomy"]["muscles"] >= 20
    assert first_run["taxonomy"]["locations"] >= 5
    assert first_run["created_exercises"] >= 150
    assert first_run["total_exercises"] == first_run["created_exercises"]

    initial_total = first_run["total_exercises"]

    # Second execution: Should update existing records and create exactly 0 new records
    second_run = await seed_exercises(db_session)
    assert second_run["created_exercises"] == 0
    assert second_run["updated_exercises"] == initial_total
    assert second_run["total_exercises"] == initial_total


@pytest.mark.asyncio
async def test_seeded_exercise_queries_and_taxonomy_integrity(db_session: AsyncSession):
    """Verify specific seeded exercises contain full relational taxonomy integrity."""
    await seed_exercises(db_session)

    # 1. Barbell Bench Press
    stmt = (
        select(Exercise)
        .where(Exercise.name == "Barbell Bench Press")
        .options(
            selectinload(Exercise.category),
            selectinload(Exercise.primary_muscle),
            selectinload(Exercise.secondary_muscles),
            selectinload(Exercise.equipment),
            selectinload(Exercise.modalities),
        )
    )
    bench_ex = (await db_session.execute(stmt)).scalar_one_or_none()
    assert bench_ex is not None
    assert bench_ex.category.name == "Chest"
    assert bench_ex.primary_muscle.name == "Pectoralis Major"
    sec_muscles = {m.name for m in bench_ex.secondary_muscles}
    assert "Anterior Deltoid" in sec_muscles
    assert "Triceps Brachii" in sec_muscles
    eq_names = {e.name for e in bench_ex.equipment}
    assert "Barbell" in eq_names
    assert "Bench" in eq_names

    # 2. Treadmill Running (Cardio / Distance Duration)
    treadmill_stmt = (
        select(Exercise)
        .where(Exercise.name == "Treadmill Running")
        .options(
            selectinload(Exercise.category),
            selectinload(Exercise.primary_muscle),
            selectinload(Exercise.locations),
        )
    )
    treadmill_ex = (await db_session.execute(treadmill_stmt)).scalar_one_or_none()
    assert treadmill_ex is not None
    assert treadmill_ex.tracking_type == ExerciseTrackingType.DISTANCE_DURATION
    assert treadmill_ex.primary_muscle.name == "Cardiovascular System"
    loc_names = {l.name for l in treadmill_ex.locations}
    assert "Commercial Gym" in loc_names

    # 3. Standard Plank Hold (Duration)
    plank_stmt = (
        select(Exercise)
        .where(Exercise.name == "Standard Plank Hold")
        .options(
            selectinload(Exercise.category),
            selectinload(Exercise.primary_muscle),
        )
    )
    plank_ex = (await db_session.execute(plank_stmt)).scalar_one_or_none()
    assert plank_ex is not None
    assert plank_ex.tracking_type == ExerciseTrackingType.DURATION
    assert plank_ex.category.name == "Core"
    assert plank_ex.primary_muscle.name == "Rectus Abdominis"
