# FitCore — Data Model & Exercise Modality Guidelines

## 1. Multi-Modal Exercise Tracking Principle
A common flaw in workout trackers is assuming every exercise consists solely of `weight × reps`. FitCore supports a broad spectrum of training modalities across gym, home, outdoor, bodyweight, cardio, functional training, and mobility.

### Modality Categories & Required Set Metrics:

1. **Standard Strength & Hypertrophy** (Barbells, Dumbbells, Cables, Machines)
   - Measurement: `ExerciseTrackingType.WEIGHT_REPS`
   - Metrics: `weight` (kg/lbs), `reps`, `rpe` (optional 1.0–10.0), `rir` (optional)
2. **Bodyweight / Calisthenics** (Pushups, Pullups, Dips, Bodyweight Squats)
   - Measurement: `ExerciseTrackingType.REPS_ONLY`
   - Metrics: `reps`, `rpe` (optional)
3. **Weighted Bodyweight** (Weighted Dips, Weighted Pullups)
   - Measurement: `ExerciseTrackingType.WEIGHTED_REPS`
   - Metrics: `weight` (added load in kg/lbs), `reps`, `rpe` (optional)
4. **Distance & Duration Cardio** (Running, Outdoor Cycling, Rowing Ergometer)
   - Measurement: `ExerciseTrackingType.DISTANCE_DURATION`
   - Metrics: `distance` (km/m/mi), `distance_unit`, `duration_seconds`
5. **Distance Only** (Pure distance target tracking)
   - Measurement: `ExerciseTrackingType.DISTANCE`
   - Metrics: `distance`, `distance_unit`
6. **Isometric Holds & Timed Static Exercises** (Plank, Wall Sit, L-Sit, Asian Squat)
   - Measurement: `ExerciseTrackingType.DURATION`
   - Metrics: `duration_seconds`
7. **Calorie & Duration Conditioning** (Air Assault Bike Sprints, SkiErg)
   - Measurement: `ExerciseTrackingType.CALORIES_DURATION`
   - Metrics: `calories`, `duration_seconds`
8. **HIIT & Circuit Intervals**
   - Measurement: `ExerciseTrackingType.INTERVAL`
   - Metrics: high-level session intervals (detailed round modeling in future phase)

---

## 2. Exercise Taxonomy & Relational Architecture (Phase 2B)

FitCore utilizes a normalized, extensible relational taxonomy structure:

```text
exercise_categories (id, name, description, created_at, updated_at)
        │ 1:N
        ▼
    exercises (id, name, description, category_id, primary_muscle_id, difficulty, tracking_type, is_system, ...)
        │
        ├── M:N ──► training_modalities (id, name, description, ...)
        │           via exercise_modalities (exercise_id, modality_id)
        │
        ├── M:N ──► equipment (id, name, description, ...)
        │           via exercise_equipment (exercise_id, equipment_id)
        │
        ├── M:N ──► locations (id, name, description, ...)
        │           via exercise_locations (exercise_id, location_id)
        │
        ├── 1:N ──► muscles (id, name, body_part, description, ...) [Primary Muscle]
        │           via exercises.primary_muscle_id (SET NULL on delete)
        │
        └── M:N ──► muscles (id, name, body_part, description, ...) [Secondary Muscles]
                    via exercise_secondary_muscles (exercise_id, muscle_id)
```

### Taxonomy Entities:
- **ExerciseCategory**: High-level grouping (e.g., Chest, Back, Shoulders, Arms, Legs, Core, Cardio & Conditioning, Olympic Weightlifting, Mobility & Flexibility, Full Body & Functional).
- **TrainingModality**: Movement training style (e.g., Strength / Hypertrophy, Calisthenics / Bodyweight, Cardio / Endurance, HIIT / Conditioning, Mobility & Stretching, Plyometrics, Functional Training, Powerlifting, Olympic Weightlifting).
- **Equipment**: Gear and apparatus requirements (e.g., Barbell, Dumbbell, Kettlebell, Bodyweight / None, Cable Machine, Weight Machine, Resistance Band, Pull-Up Bar, Dip Station, Bench, Squat Rack, Treadmill, Stationary Bike, Rowing Machine, Jump Rope, Plyo Box, Medicine Ball, EZ Curl Bar, Suspension Trainer, Foam Roller, Sled / Prowler, Battle Ropes).
- **Muscle**: Anatomical target groups with body part mapping (e.g., Pectoralis Major, Latissimus Dorsi, Trapezius, Anterior Deltoid, Lateral Deltoid, Posterior Deltoid, Biceps Brachii, Triceps Brachii, Brachialis & Forearms, Quadriceps, Hamstrings, Gluteus Maximus, Calves, Rectus Abdominis, Obliques, Transverse Abdominis, Cardiovascular System).
- **ExerciseLocation**: Environmental training contexts (e.g., Commercial Gym, Home Gym, Outdoors / Park, Hotel / Travel, CrossFit / Studio).
- **DifficultyLevel**: Controlled rating (`BEGINNER`, `INTERMEDIATE`, `ADVANCED`).

---

## 3. Core Workout Tracking Relational Schema

```text
users (id, email, hashed_password, full_name, is_active, created_at, updated_at)
  │
  └── workouts (id, user_id, name, started_at, completed_at, status, notes, created_at, updated_at)
        │
        └── workout_exercises (id, workout_id, exercise_id, order_index, notes, created_at, updated_at)
              │
              └── sets (id, workout_exercise_id, set_number, set_type,
                        reps, weight, duration_seconds, distance, distance_unit,
                        calories, rpe, rir, is_warmup, notes, created_at)
```
