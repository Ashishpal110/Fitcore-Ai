"""Create core workout tables (exercises, workouts, workout_exercises, sets)

Revision ID: 20260929_0002
Revises: 20260928_0001
Create Date: 2026-09-29 11:06:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20260929_0002'
down_revision: Union[str, None] = '20260928_0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"
    uuid_col = postgresql.UUID(as_uuid=True) if is_postgres else sa.CHAR(36)

    # 1. Exercises Table
    op.create_table(
        'exercises',
        sa.Column('id', uuid_col, primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tracking_type', sa.String(length=50), nullable=False),
        sa.Column('is_system', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f('ix_exercises_name'), 'exercises', ['name'], unique=False)

    # 2. Workouts Table
    op.create_table(
        'workouts',
        sa.Column('id', uuid_col, primary_key=True, nullable=False),
        sa.Column('user_id', uuid_col, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=50), server_default='IN_PROGRESS', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f('ix_workouts_user_id'), 'workouts', ['user_id'], unique=False)
    op.create_index(op.f('ix_workouts_started_at'), 'workouts', ['started_at'], unique=False)
    op.create_index(op.f('ix_workouts_status'), 'workouts', ['status'], unique=False)

    # 3. Workout Exercises Table
    op.create_table(
        'workout_exercises',
        sa.Column('id', uuid_col, primary_key=True, nullable=False),
        sa.Column('workout_id', uuid_col, sa.ForeignKey('workouts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('exercise_id', uuid_col, sa.ForeignKey('exercises.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('order_index', sa.Integer(), server_default='0', nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint('order_index >= 0', name='ck_workout_exercises_order_index_non_negative'),
    )
    op.create_index(op.f('ix_workout_exercises_workout_id'), 'workout_exercises', ['workout_id'], unique=False)
    op.create_index(op.f('ix_workout_exercises_exercise_id'), 'workout_exercises', ['exercise_id'], unique=False)

    # 4. Sets Table
    op.create_table(
        'sets',
        sa.Column('id', uuid_col, primary_key=True, nullable=False),
        sa.Column('workout_exercise_id', uuid_col, sa.ForeignKey('workout_exercises.id', ondelete='CASCADE'), nullable=False),
        sa.Column('set_number', sa.Integer(), nullable=False),
        sa.Column('set_type', sa.String(length=50), server_default='WORKING', nullable=False),
        sa.Column('reps', sa.Integer(), nullable=True),
        sa.Column('weight', sa.Numeric(precision=7, scale=2), nullable=True),
        sa.Column('duration_seconds', sa.Integer(), nullable=True),
        sa.Column('distance', sa.Numeric(precision=8, scale=2), nullable=True),
        sa.Column('distance_unit', sa.String(length=20), nullable=True),
        sa.Column('calories', sa.Numeric(precision=7, scale=2), nullable=True),
        sa.Column('rpe', sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column('rir', sa.Integer(), nullable=True),
        sa.Column('is_warmup', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint('workout_exercise_id', 'set_number', name='uq_sets_workout_exercise_set_number'),
        sa.CheckConstraint('set_number > 0', name='ck_sets_set_number_positive'),
        sa.CheckConstraint('reps IS NULL OR reps >= 0', name='ck_sets_reps_non_negative'),
        sa.CheckConstraint('weight IS NULL OR weight >= 0', name='ck_sets_weight_non_negative'),
        sa.CheckConstraint('duration_seconds IS NULL OR duration_seconds >= 0', name='ck_sets_duration_non_negative'),
        sa.CheckConstraint('distance IS NULL OR distance >= 0', name='ck_sets_distance_non_negative'),
        sa.CheckConstraint('calories IS NULL OR calories >= 0', name='ck_sets_calories_non_negative'),
        sa.CheckConstraint('rpe IS NULL OR (rpe >= 1.0 AND rpe <= 10.0)', name='ck_sets_rpe_range'),
        sa.CheckConstraint('rir IS NULL OR rir >= 0', name='ck_sets_rir_non_negative'),
    )
    op.create_index(op.f('ix_sets_workout_exercise_id'), 'sets', ['workout_exercise_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_sets_workout_exercise_id'), table_name='sets')
    op.drop_table('sets')

    op.drop_index(op.f('ix_workout_exercises_exercise_id'), table_name='workout_exercises')
    op.drop_index(op.f('ix_workout_exercises_workout_id'), table_name='workout_exercises')
    op.drop_table('workout_exercises')

    op.drop_index(op.f('ix_workouts_status'), table_name='workouts')
    op.drop_index(op.f('ix_workouts_started_at'), table_name='workouts')
    op.drop_index(op.f('ix_workouts_user_id'), table_name='workouts')
    op.drop_table('workouts')

    op.drop_index(op.f('ix_exercises_name'), table_name='exercises')
    op.drop_table('exercises')
