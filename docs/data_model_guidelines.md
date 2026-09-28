# FitCore — Data Model & Exercise Modality Guidelines

## 1. Multi-Modal Exercise Tracking Principle
A common flaw in workout trackers is assuming every exercise consists solely of `weight × reps`. FitCore supports a broad spectrum of training modalities.

### Modality Categories & Required Set Metrics:

1. **Standard Strength & Hypertrophy** (Barbells, Dumbbells, Cables, Machines)
   - Metrics: `weight_kg` (or `lbs`), `reps`, `rpe` (optional), `rest_seconds`
2. **Bodyweight / Calisthenics** (Pushups, Pullups, Dips)
   - Metrics: `reps`, `rpe` (optional)
3. **Weighted Bodyweight** (Weighted Dips, Weighted Pullups)
   - Metrics: `added_weight_kg`, `reps`, `rpe` (optional)
4. **Distance & Duration Cardio** (Running, Outdoor Cycling, Rowing)
   - Metrics: `distance_meters` (or `km`/`miles`), `duration_seconds`, `pace`, `heart_rate_avg` (optional)
5. **Isometric Holds** (Plank, Wall Sit, L-Sit)
   - Metrics: `duration_seconds`
6. **HIIT & Circuit Intervals**
   - Metrics: `rounds`, `work_duration_seconds`, `rest_duration_seconds`, `reps` (optional)
7. **Lap Swimming**
   - Metrics: `laps`, `pool_length_meters`, `duration_seconds`, `stroke_type`

## 2. Entity Relationship Overview (Target for Phase 2)

```text
users (id, email, hashed_password, full_name, created_at, ...)
  │
  ├── routines (id, user_id, name, is_archived, ...)
  │     └── routine_exercises (id, routine_id, exercise_id, order, target_sets, ...)
  │
  ├── workouts (id, user_id, routine_id, start_time, end_time, status, notes, ...)
  │     └── workout_exercises (id, workout_id, exercise_id, order, notes, ...)
  │           └── exercise_sets (id, workout_exercise_id, set_number, set_type,
  │                              weight, reps, distance, duration, rpe, is_completed, ...)
  │
  ├── body_measurements (id, user_id, logged_at, weight_kg, body_fat_pct, ...)
  └── personal_records (id, user_id, exercise_id, record_type, value, achieved_at, ...)

exercises (id, name, category, modality, primary_muscle, secondary_muscles, equipment, is_custom, created_by_user_id)
```
