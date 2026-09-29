import uuid
from decimal import Decimal
import pytest
from app.models.enums import DistanceUnit, ExerciseTrackingType, SetType, WorkoutStatus
from app.models.exercise import Exercise
from app.models.set import Set
from app.models.user import User
from app.models.workout import Workout
from app.models.workout_exercise import WorkoutExercise


def test_exercise_model_instantiation():
    """Verify Exercise model fields and enum defaults."""
    exercise = Exercise(
        name="Barbell Bench Press",
        description="Horizontal pressing movement targeting pectorals, triceps, and anterior deltoids.",
        tracking_type=ExerciseTrackingType.WEIGHT_REPS,
        is_system=True,
    )
    assert exercise.name == "Barbell Bench Press"
    assert exercise.tracking_type == ExerciseTrackingType.WEIGHT_REPS
    assert exercise.is_system is True
    assert "Barbell Bench Press" in repr(exercise)


def test_workout_model_instantiation():
    """Verify Workout model fields and status enum."""
    user_id = uuid.uuid4()
    workout = Workout(
        user_id=user_id,
        name="Upper Body Power",
        status=WorkoutStatus.IN_PROGRESS,
    )
    assert workout.user_id == user_id
    assert workout.name == "Upper Body Power"
    assert workout.status == WorkoutStatus.IN_PROGRESS
    assert workout.completed_at is None
    assert str(user_id) in repr(workout)


def test_workout_exercise_instantiation():
    """Verify WorkoutExercise ordering and foreign keys."""
    workout_id = uuid.uuid4()
    exercise_id = uuid.uuid4()
    we = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        order_index=1,
        notes="Focus on full range of motion",
    )
    assert we.workout_id == workout_id
    assert we.exercise_id == exercise_id
    assert we.order_index == 1
    assert we.notes == "Focus on full range of motion"


def test_set_model_instantiation_and_warmup_sync():
    """Verify Set metrics, calories, decimal precision, and warmup synchronization."""
    we_id = uuid.uuid4()
    
    # 1. Standard working set with calories
    s1 = Set(
        workout_exercise_id=we_id,
        set_number=1,
        set_type=SetType.WORKING,
        reps=10,
        weight=Decimal("82.50"),
        calories=Decimal("45.00"),
        rpe=Decimal("8.0"),
        rir=2,
        is_warmup=False,
    )
    assert s1.workout_exercise_id == we_id
    assert s1.set_number == 1
    assert s1.reps == 10
    assert s1.weight == Decimal("82.50")
    assert s1.calories == Decimal("45.00")
    assert s1.rpe == Decimal("8.0")
    assert s1.rir == 2
    assert s1.is_warmup is False
    assert s1.duration_seconds is None
    assert s1.distance is None

    # 2. Set with set_type=WARMUP automatically flags is_warmup=True
    s2 = Set(
        workout_exercise_id=we_id,
        set_number=2,
        set_type=SetType.WARMUP,
        weight=Decimal("40.00"),
        reps=12,
    )
    assert s2.set_type == SetType.WARMUP
    assert s2.is_warmup is True
