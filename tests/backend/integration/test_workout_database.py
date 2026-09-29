import uuid
from datetime import datetime, timezone
from decimal import Decimal
import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import DistanceUnit, ExerciseTrackingType, SetType, WorkoutStatus
from app.models.exercise import Exercise
from app.models.set import Set
from app.models.user import User
from app.models.workout import Workout
from app.models.workout_exercise import WorkoutExercise


@pytest_asyncio.fixture
async def sample_user(db_session: AsyncSession) -> User:
    """Create a persistent sample user for database integration tests."""
    user = User(
        name="Athlete Alex",
        email=f"alex_{uuid.uuid4().hex[:6]}@example.com",
        password_hash="hashed_pw_test",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_exercise_creation_all_tracking_types(db_session: AsyncSession):
    """Verify that exercises can be created with each supported tracking type."""
    tracking_types = [
        ExerciseTrackingType.WEIGHT_REPS,
        ExerciseTrackingType.REPS_ONLY,
        ExerciseTrackingType.WEIGHTED_REPS,
        ExerciseTrackingType.DURATION,
        ExerciseTrackingType.DISTANCE_DURATION,
        ExerciseTrackingType.DISTANCE,
        ExerciseTrackingType.CALORIES_DURATION,
        ExerciseTrackingType.INTERVAL,
    ]

    for t_type in tracking_types:
        ex = Exercise(
            name=f"Exercise {t_type.value}",
            description=f"Testing {t_type.value}",
            tracking_type=t_type,
            is_system=True,
        )
        db_session.add(ex)

    await db_session.commit()

    stmt = select(Exercise)
    result = await db_session.execute(stmt)
    saved_exercises = result.scalars().all()
    assert len(saved_exercises) == len(tracking_types)


@pytest.mark.asyncio
async def test_workout_creation_and_user_relationship(
    db_session: AsyncSession,
    sample_user: User,
):
    """Verify workout creation, status, and bidirectional user relationship."""
    workout = Workout(
        user_id=sample_user.id,
        name="Leg Hypertrophy",
        started_at=datetime.now(timezone.utc),
        status=WorkoutStatus.IN_PROGRESS,
        notes="High volume leg session",
    )
    db_session.add(workout)
    await db_session.commit()
    await db_session.refresh(workout)

    assert workout.id is not None
    assert workout.user_id == sample_user.id
    assert workout.status == WorkoutStatus.IN_PROGRESS

    # Verify traversal through relationship
    stmt = select(Workout).where(Workout.id == workout.id)
    res = await db_session.execute(stmt)
    loaded_workout = res.scalars().first()
    assert loaded_workout is not None
    assert loaded_workout.user.email == sample_user.email

    # Complete the workout
    loaded_workout.status = WorkoutStatus.COMPLETED
    loaded_workout.completed_at = datetime.now(timezone.utc)
    await db_session.commit()
    await db_session.refresh(loaded_workout)

    assert loaded_workout.status == WorkoutStatus.COMPLETED
    assert loaded_workout.completed_at is not None


@pytest.mark.asyncio
async def test_workout_exercise_ordering(
    db_session: AsyncSession,
    sample_user: User,
):
    """Verify WorkoutExercise order preservation within a workout."""
    workout = Workout(
        user_id=sample_user.id,
        name="Upper Body Routine",
        started_at=datetime.now(timezone.utc),
    )
    ex1 = Exercise(name="Bench Press", tracking_type=ExerciseTrackingType.WEIGHT_REPS)
    ex2 = Exercise(name="Incline DB Press", tracking_type=ExerciseTrackingType.WEIGHT_REPS)
    ex3 = Exercise(name="Tricep Pushdown", tracking_type=ExerciseTrackingType.WEIGHT_REPS)

    db_session.add_all([workout, ex1, ex2, ex3])
    await db_session.commit()

    # Add workout exercises with explicit order_index
    we1 = WorkoutExercise(workout_id=workout.id, exercise_id=ex1.id, order_index=0)
    we2 = WorkoutExercise(workout_id=workout.id, exercise_id=ex2.id, order_index=1)
    we3 = WorkoutExercise(workout_id=workout.id, exercise_id=ex3.id, order_index=2)

    db_session.add_all([we1, we2, we3])
    await db_session.commit()

    # Query workout and check ordered workout_exercises
    stmt = select(Workout).where(Workout.id == workout.id)
    res = await db_session.execute(stmt)
    w = res.scalars().first()

    assert len(w.workout_exercises) == 3
    assert [we.order_index for we in w.workout_exercises] == [0, 1, 2]
    assert [we.exercise.name for we in w.workout_exercises] == [
        "Bench Press",
        "Incline DB Press",
        "Tricep Pushdown",
    ]


@pytest.mark.asyncio
async def test_set_unique_constraint(
    db_session: AsyncSession,
    sample_user: User,
):
    """Verify that duplicate set_number within same workout_exercise raises IntegrityError."""
    workout = Workout(user_id=sample_user.id, started_at=datetime.now(timezone.utc))
    ex = Exercise(name="Squat", tracking_type=ExerciseTrackingType.WEIGHT_REPS)
    db_session.add_all([workout, ex])
    await db_session.commit()

    we = WorkoutExercise(workout_id=workout.id, exercise_id=ex.id, order_index=0)
    db_session.add(we)
    await db_session.commit()

    set1 = Set(
        workout_exercise_id=we.id,
        set_number=1,
        set_type=SetType.WORKING,
        reps=5,
        weight=Decimal("100.00"),
    )
    db_session.add(set1)
    await db_session.commit()

    # Attempt to insert another Set with set_number=1 for the same workout_exercise
    set1_duplicate = Set(
        workout_exercise_id=we.id,
        set_number=1,
        set_type=SetType.WORKING,
        reps=5,
        weight=Decimal("100.00"),
    )
    db_session.add(set1_duplicate)

    with pytest.raises(IntegrityError):
        await db_session.commit()

    await db_session.rollback()


@pytest.mark.asyncio
async def test_set_calories_and_warmup_behavior(
    db_session: AsyncSession,
    sample_user: User,
):
    """Verify calories recording and warmup synchronization."""
    workout = Workout(user_id=sample_user.id, started_at=datetime.now(timezone.utc))
    ex = Exercise(name="Rowing Ergometer", tracking_type=ExerciseTrackingType.CALORIES_DURATION)
    db_session.add_all([workout, ex])
    await db_session.commit()

    we = WorkoutExercise(workout_id=workout.id, exercise_id=ex.id, order_index=0)
    db_session.add(we)
    await db_session.commit()

    # Warmup set with calories
    warmup_set = Set(
        workout_exercise_id=we.id,
        set_number=1,
        set_type=SetType.WARMUP,
        duration_seconds=300,
        calories=Decimal("50.00"),
    )
    db_session.add(warmup_set)
    await db_session.commit()
    await db_session.refresh(warmup_set)

    assert warmup_set.set_type == SetType.WARMUP
    assert warmup_set.is_warmup is True
    assert warmup_set.calories == Decimal("50.00")

    # Working set with calories
    work_set = Set(
        workout_exercise_id=we.id,
        set_number=2,
        set_type=SetType.WORKING,
        duration_seconds=900,
        calories=Decimal("200.00"),
        is_warmup=False,
    )
    db_session.add(work_set)
    await db_session.commit()
    await db_session.refresh(work_set)

    assert work_set.calories == Decimal("200.00")
    assert work_set.is_warmup is False


@pytest.mark.asyncio
async def test_cascade_deletion_of_workout_tree(
    db_session: AsyncSession,
    sample_user: User,
):
    """Verify that deleting a workout cascades and cleans up workout_exercises and sets."""
    workout = Workout(user_id=sample_user.id, started_at=datetime.now(timezone.utc))
    ex = Exercise(name="Deadlift", tracking_type=ExerciseTrackingType.WEIGHT_REPS)
    db_session.add_all([workout, ex])
    await db_session.commit()

    we = WorkoutExercise(workout_id=workout.id, exercise_id=ex.id, order_index=0)
    db_session.add(we)
    await db_session.commit()

    s1 = Set(workout_exercise_id=we.id, set_number=1, reps=5, weight=Decimal("140.00"))
    s2 = Set(workout_exercise_id=we.id, set_number=2, reps=5, weight=Decimal("140.00"))
    db_session.add_all([s1, s2])
    await db_session.commit()

    we_id = we.id
    s1_id = s1.id
    s2_id = s2.id

    # Delete the parent workout
    await db_session.delete(workout)
    await db_session.commit()

    # Verify workout_exercise and sets are also deleted
    we_check = await db_session.execute(select(WorkoutExercise).where(WorkoutExercise.id == we_id))
    assert we_check.scalars().first() is None

    s1_check = await db_session.execute(select(Set).where(Set.id == s1_id))
    assert s1_check.scalars().first() is None

    s2_check = await db_session.execute(select(Set).where(Set.id == s2_id))
    assert s2_check.scalars().first() is None

    # Exercise itself must still exist (historical master definition preserved)
    ex_check = await db_session.execute(select(Exercise).where(Exercise.id == ex.id))
    assert ex_check.scalars().first() is not None


@pytest.mark.asyncio
async def test_user_deletion_cascades_to_workouts(
    db_session: AsyncSession,
    sample_user: User,
):
    """Verify that deleting a user cascades to all their workouts."""
    workout = Workout(
        user_id=sample_user.id,
        name="User Workout",
        started_at=datetime.now(timezone.utc),
    )
    db_session.add(workout)
    await db_session.commit()

    workout_id = workout.id

    await db_session.delete(sample_user)
    await db_session.commit()

    w_check = await db_session.execute(select(Workout).where(Workout.id == workout_id))
    assert w_check.scalars().first() is None


@pytest.mark.asyncio
async def test_multi_modal_exercise_tracking(
    db_session: AsyncSession,
    sample_user: User,
):
    """Verify representative multi-modal exercise recording without fake placeholder values."""
    workout = Workout(
        user_id=sample_user.id,
        name="Hybrid Training Session",
        started_at=datetime.now(timezone.utc),
    )
    db_session.add(workout)
    await db_session.commit()

    # 1. Strength: Bench Press (60 kg, 8 reps, RPE 8.5)
    ex_bench = Exercise(name="Bench Press", tracking_type=ExerciseTrackingType.WEIGHT_REPS)
    db_session.add(ex_bench)
    await db_session.commit()

    we_bench = WorkoutExercise(workout_id=workout.id, exercise_id=ex_bench.id, order_index=0)
    db_session.add(we_bench)
    await db_session.commit()

    set_bench = Set(
        workout_exercise_id=we_bench.id,
        set_number=1,
        set_type=SetType.WORKING,
        reps=8,
        weight=Decimal("60.00"),
        rpe=Decimal("8.5"),
        rir=1,
        is_warmup=False,
    )
    db_session.add(set_bench)

    # 2. Bodyweight: Push Up (15 reps, weight NULL, duration NULL)
    ex_pushup = Exercise(name="Push Up", tracking_type=ExerciseTrackingType.REPS_ONLY)
    db_session.add(ex_pushup)
    await db_session.commit()

    we_pushup = WorkoutExercise(workout_id=workout.id, exercise_id=ex_pushup.id, order_index=1)
    db_session.add(we_pushup)
    await db_session.commit()

    set_pushup = Set(
        workout_exercise_id=we_pushup.id,
        set_number=1,
        set_type=SetType.WORKING,
        reps=15,
        weight=None,
        duration_seconds=None,
        is_warmup=False,
    )
    db_session.add(set_pushup)

    # 3. Weighted Bodyweight: Pull Up (10 kg added, 6 reps)
    ex_pullup = Exercise(name="Pull Up", tracking_type=ExerciseTrackingType.WEIGHTED_REPS)
    db_session.add(ex_pullup)
    await db_session.commit()

    we_pullup = WorkoutExercise(workout_id=workout.id, exercise_id=ex_pullup.id, order_index=2)
    db_session.add(we_pullup)
    await db_session.commit()

    set_pullup = Set(
        workout_exercise_id=we_pullup.id,
        set_number=1,
        set_type=SetType.WORKING,
        reps=6,
        weight=Decimal("10.00"),
        is_warmup=False,
    )
    db_session.add(set_pullup)

    # 4. Isometric Duration: Plank (60 seconds, reps NULL, weight NULL)
    ex_plank = Exercise(name="Plank", tracking_type=ExerciseTrackingType.DURATION)
    db_session.add(ex_plank)
    await db_session.commit()

    we_plank = WorkoutExercise(workout_id=workout.id, exercise_id=ex_plank.id, order_index=3)
    db_session.add(we_plank)
    await db_session.commit()

    set_plank = Set(
        workout_exercise_id=we_plank.id,
        set_number=1,
        set_type=SetType.WORKING,
        reps=None,
        weight=None,
        duration_seconds=60,
        is_warmup=False,
    )
    db_session.add(set_plank)

    # 5. Distance + Duration: Outdoor Running (5.00 km, 1800 seconds)
    ex_run = Exercise(name="Outdoor Running", tracking_type=ExerciseTrackingType.DISTANCE_DURATION)
    db_session.add(ex_run)
    await db_session.commit()

    we_run = WorkoutExercise(workout_id=workout.id, exercise_id=ex_run.id, order_index=4)
    db_session.add(we_run)
    await db_session.commit()

    set_run = Set(
        workout_exercise_id=we_run.id,
        set_number=1,
        set_type=SetType.WORKING,
        reps=None,
        weight=None,
        distance=Decimal("5.00"),
        distance_unit=DistanceUnit.KM,
        duration_seconds=1800,
        is_warmup=False,
    )
    db_session.add(set_run)

    # 6. Calories + Duration: Assault AirBike (250.00 kcal, 900 seconds)
    ex_bike = Exercise(name="Assault AirBike", tracking_type=ExerciseTrackingType.CALORIES_DURATION)
    db_session.add(ex_bike)
    await db_session.commit()

    we_bike = WorkoutExercise(workout_id=workout.id, exercise_id=ex_bike.id, order_index=5)
    db_session.add(we_bike)
    await db_session.commit()

    set_bike = Set(
        workout_exercise_id=we_bike.id,
        set_number=1,
        set_type=SetType.WORKING,
        reps=None,
        weight=None,
        calories=Decimal("250.00"),
        duration_seconds=900,
        is_warmup=False,
    )
    db_session.add(set_bike)

    await db_session.commit()

    # Verify query and all metrics
    stmt = select(Workout).where(Workout.id == workout.id)
    res = await db_session.execute(stmt)
    loaded_w = res.scalars().first()

    assert len(loaded_w.workout_exercises) == 6

    # Check Bench Press
    bench_set = loaded_w.workout_exercises[0].sets[0]
    assert bench_set.weight == Decimal("60.00")
    assert bench_set.reps == 8
    assert bench_set.rpe == Decimal("8.5")

    # Check Push Up
    pushup_set = loaded_w.workout_exercises[1].sets[0]
    assert pushup_set.reps == 15
    assert pushup_set.weight is None
    assert pushup_set.duration_seconds is None

    # Check Pull Up
    pullup_set = loaded_w.workout_exercises[2].sets[0]
    assert pullup_set.weight == Decimal("10.00")
    assert pullup_set.reps == 6

    # Check Plank
    plank_set = loaded_w.workout_exercises[3].sets[0]
    assert plank_set.duration_seconds == 60
    assert plank_set.reps is None
    assert plank_set.weight is None

    # Check Running
    run_set = loaded_w.workout_exercises[4].sets[0]
    assert run_set.distance == Decimal("5.00")
    assert run_set.distance_unit == DistanceUnit.KM
    assert run_set.duration_seconds == 1800

    # Check AirBike Calories
    bike_set = loaded_w.workout_exercises[5].sets[0]
    assert bike_set.calories == Decimal("250.00")
    assert bike_set.duration_seconds == 900
    assert bike_set.reps is None
    assert bike_set.weight is None
