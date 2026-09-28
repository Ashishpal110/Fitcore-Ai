# FitCore — Database Architecture & Setup

## Overview
FitCore uses PostgreSQL as its primary relational data store, managed via SQLAlchemy 2.0 and Alembic migrations.

## Database Design Guidelines
1. **Multi-Modal Workout Logging**:
   The schema must handle varying performance metrics without forcing a rigid `weight × reps` pattern. The workout exercises and sets schema will support:
   - Strength: `weight`, `reps`, `rpe`
   - Bodyweight / Calisthenics: `reps`
   - Weighted Bodyweight: `added_weight`, `reps`
   - Cardio (Running / Cycling): `distance`, `duration`, `pace`
   - Isometric (Plank): `duration`
   - HIIT / Functional: `rounds`, `duration`, `work_rest_intervals`

2. **Strict User Ownership**:
   All user-scoped entities (`workouts`, `routines`, `measurements`, `personal_records`) must maintain foreign keys to `users.id` with appropriate indexes and composite unique constraints where applicable.

3. **Migrations**:
   All schema modifications must be applied via Alembic migrations (`backend/alembic/versions/`). Never modify production schemas manually.

## Local PostgreSQL Initialization
To run a local PostgreSQL database with Docker:
```bash
docker run --name fitcore-postgres -e POSTGRES_DB=fitcore_dev -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:16-alpine
```
