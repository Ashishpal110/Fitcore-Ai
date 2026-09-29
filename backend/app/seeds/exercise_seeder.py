"""Idempotent database seeder for FitCore exercise taxonomy and library."""

from typing import Any, Dict
from sqlalchemy import select
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
)
from app.seeds.exercise_data import EXERCISES
from app.seeds.taxonomy_data import (
    CATEGORIES,
    EQUIPMENT,
    LOCATIONS,
    MODALITIES,
    MUSCLES,
)


async def seed_taxonomy(session: AsyncSession) -> Dict[str, int]:
    """Seed all baseline taxonomy entities idempotently."""
    counts = {}

    # 1. Categories
    cat_result = await session.execute(select(ExerciseCategory))
    existing_cats = {c.name: c for c in cat_result.scalars().all()}
    for cat_data in CATEGORIES:
        if cat_data["name"] not in existing_cats:
            cat = ExerciseCategory(
                name=cat_data["name"],
                description=cat_data.get("description"),
            )
            session.add(cat)
    await session.flush()
    cat_count_res = await session.execute(select(ExerciseCategory))
    counts["categories"] = len(cat_count_res.scalars().all())

    # 2. Modalities
    mod_result = await session.execute(select(TrainingModality))
    existing_mods = {m.name: m for m in mod_result.scalars().all()}
    for mod_data in MODALITIES:
        if mod_data["name"] not in existing_mods:
            mod = TrainingModality(
                name=mod_data["name"],
                description=mod_data.get("description"),
            )
            session.add(mod)
    await session.flush()
    mod_count_res = await session.execute(select(TrainingModality))
    counts["modalities"] = len(mod_count_res.scalars().all())

    # 3. Equipment
    eq_result = await session.execute(select(Equipment))
    existing_eq = {e.name: e for e in eq_result.scalars().all()}
    for eq_data in EQUIPMENT:
        if eq_data["name"] not in existing_eq:
            eq = Equipment(
                name=eq_data["name"],
                description=eq_data.get("description"),
            )
            session.add(eq)
    await session.flush()
    eq_count_res = await session.execute(select(Equipment))
    counts["equipment"] = len(eq_count_res.scalars().all())

    # 4. Muscles
    mus_result = await session.execute(select(Muscle))
    existing_mus = {m.name: m for m in mus_result.scalars().all()}
    for mus_data in MUSCLES:
        if mus_data["name"] not in existing_mus:
            mus = Muscle(
                name=mus_data["name"],
                body_part=mus_data["body_part"],
                description=mus_data.get("description"),
            )
            session.add(mus)
    await session.flush()
    mus_count_res = await session.execute(select(Muscle))
    counts["muscles"] = len(mus_count_res.scalars().all())

    # 5. Locations
    loc_result = await session.execute(select(ExerciseLocation))
    existing_loc = {l.name: l for l in loc_result.scalars().all()}
    for loc_data in LOCATIONS:
        if loc_data["name"] not in existing_loc:
            loc = ExerciseLocation(
                name=loc_data["name"],
                description=loc_data.get("description"),
            )
            session.add(loc)
    await session.flush()
    loc_count_res = await session.execute(select(ExerciseLocation))
    counts["locations"] = len(loc_count_res.scalars().all())

    return counts


async def seed_exercises(session: AsyncSession) -> Dict[str, Any]:
    """Seed comprehensive exercise catalog with taxonomy associations idempotently."""
    taxonomy_counts = await seed_taxonomy(session)

    # Fetch lookup maps
    cat_map = {c.name: c for c in (await session.execute(select(ExerciseCategory))).scalars().all()}
    mod_map = {m.name: m for m in (await session.execute(select(TrainingModality))).scalars().all()}
    eq_map = {e.name: e for e in (await session.execute(select(Equipment))).scalars().all()}
    mus_map = {m.name: m for m in (await session.execute(select(Muscle))).scalars().all()}
    loc_map = {l.name: l for l in (await session.execute(select(ExerciseLocation))).scalars().all()}

    created_count = 0
    updated_count = 0

    for ex_data in EXERCISES:
        stmt = (
            select(Exercise)
            .where(Exercise.name == ex_data["name"])
            .options(
                selectinload(Exercise.secondary_muscles),
                selectinload(Exercise.modalities),
                selectinload(Exercise.equipment),
                selectinload(Exercise.locations),
            )
        )
        result = await session.execute(stmt)
        existing_exercise = result.scalar_one_or_none()

        category = cat_map.get(ex_data["category"])
        primary_muscle = mus_map.get(ex_data["primary_muscle"])
        difficulty = DifficultyLevel(ex_data.get("difficulty", "BEGINNER"))
        tracking_type = ExerciseTrackingType(ex_data.get("tracking_type", "WEIGHT_REPS"))

        secondary_muscles = [mus_map[m] for m in ex_data.get("secondary_muscles", []) if m in mus_map]
        modalities = [mod_map[m] for m in ex_data.get("modalities", []) if m in mod_map]
        equipment = [eq_map[e] for e in ex_data.get("equipment", []) if e in eq_map]
        locations = [loc_map[l] for l in ex_data.get("locations", []) if l in loc_map]

        if existing_exercise is None:
            new_exercise = Exercise(
                name=ex_data["name"],
                description=ex_data.get("description"),
                category_id=category.id if category else None,
                primary_muscle_id=primary_muscle.id if primary_muscle else None,
                difficulty=difficulty,
                tracking_type=tracking_type,
                is_system=True,
                secondary_muscles=secondary_muscles,
                modalities=modalities,
                equipment=equipment,
                locations=locations,
            )
            session.add(new_exercise)
            created_count += 1
        else:
            existing_exercise.description = ex_data.get("description")
            existing_exercise.category_id = category.id if category else None
            existing_exercise.primary_muscle_id = primary_muscle.id if primary_muscle else None
            existing_exercise.difficulty = difficulty
            existing_exercise.tracking_type = tracking_type
            existing_exercise.is_system = True
            existing_exercise.secondary_muscles = secondary_muscles
            existing_exercise.modalities = modalities
            existing_exercise.equipment = equipment
            existing_exercise.locations = locations
            updated_count += 1

    await session.commit()

    total_exercises = len((await session.execute(select(Exercise))).scalars().all())

    return {
        "taxonomy": taxonomy_counts,
        "created_exercises": created_count,
        "updated_exercises": updated_count,
        "total_exercises": total_exercises,
    }
