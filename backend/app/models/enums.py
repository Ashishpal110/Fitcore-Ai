import enum


class ExerciseTrackingType(str, enum.Enum):
    """Supported exercise measurement modalities.
    
    Modalities:
    - WEIGHT_REPS: Standard resistance exercises (weight + reps)
    - REPS_ONLY: Calisthenics and bodyweight exercises (reps)
    - WEIGHTED_REPS: Weighted bodyweight movements (added weight + reps)
    - DURATION: Isometric holds and static exercises (duration in seconds)
    - DISTANCE_DURATION: Cardio activities recording distance and elapsed time
    - DISTANCE: Pure distance target activities
    - CALORIES_DURATION: Machine cardio/conditioning tracking energy burned and time
    - INTERVAL: High-level interval training. Note: Detailed round/work/rest 
      interval breakdown modeling will be implemented in a dedicated future phase.
    """
    WEIGHT_REPS = "WEIGHT_REPS"
    REPS_ONLY = "REPS_ONLY"
    WEIGHTED_REPS = "WEIGHTED_REPS"
    DURATION = "DURATION"
    DISTANCE_DURATION = "DISTANCE_DURATION"
    DISTANCE = "DISTANCE"
    CALORIES_DURATION = "CALORIES_DURATION"
    INTERVAL = "INTERVAL"


class WorkoutStatus(str, enum.Enum):
    """Lifecycle status of a workout session."""
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class SetType(str, enum.Enum):
    """Categorization of individual sets.
    
    Standard set types:
    - WORKING: Standard prescribed working set
    - WARMUP: Acclimation/warmup set (corresponds to is_warmup=True)
    - DROP: Dropset with immediate weight reduction
    - FAILURE: Set taken to absolute mechanical failure
    - AMRAP: As Many Reps/Rounds As Possible
    - OTHER: Miscellaneous or custom set type
    """
    WORKING = "WORKING"
    WARMUP = "WARMUP"
    DROP = "DROP"
    FAILURE = "FAILURE"
    AMRAP = "AMRAP"
    OTHER = "OTHER"


class DistanceUnit(str, enum.Enum):
    """Supported distance units for cardio and endurance exercises."""
    KM = "KM"
    M = "M"
    MI = "MI"


class DifficultyLevel(str, enum.Enum):
    """Subjective exercise execution difficulty rating."""
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

