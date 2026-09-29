"""Create exercise taxonomy tables and associations

Revision ID: 20260929_0003
Revises: 20260929_0002
Create Date: 2026-09-29 11:30:00

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '20260929_0003'
down_revision: Union[str, None] = '20260929_0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    is_postgres = bind.dialect.name == "postgresql"
    uuid_col = postgresql.UUID(as_uuid=True) if is_postgres else sa.CHAR(36)

    # 1. Exercise Categories Table
    op.create_table(
        'exercise_categories',
        sa.Column('id', uuid_col, primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f('ix_exercise_categories_name'), 'exercise_categories', ['name'], unique=True)

    # 2. Training Modalities Table
    op.create_table(
        'training_modalities',
        sa.Column('id', uuid_col, primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f('ix_training_modalities_name'), 'training_modalities', ['name'], unique=True)

    # 3. Equipment Table
    op.create_table(
        'equipment',
        sa.Column('id', uuid_col, primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f('ix_equipment_name'), 'equipment', ['name'], unique=True)

    # 4. Muscles Table
    op.create_table(
        'muscles',
        sa.Column('id', uuid_col, primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('body_part', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f('ix_muscles_name'), 'muscles', ['name'], unique=True)
    op.create_index(op.f('ix_muscles_body_part'), 'muscles', ['body_part'], unique=False)

    # 5. Locations Table
    op.create_table(
        'locations',
        sa.Column('id', uuid_col, primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index(op.f('ix_locations_name'), 'locations', ['name'], unique=True)

    # 6. Add taxonomy columns to Exercises table
    op.add_column('exercises', sa.Column('category_id', uuid_col, sa.ForeignKey('exercise_categories.id', ondelete='SET NULL'), nullable=True))
    op.add_column('exercises', sa.Column('primary_muscle_id', uuid_col, sa.ForeignKey('muscles.id', ondelete='SET NULL'), nullable=True))
    op.add_column('exercises', sa.Column('difficulty', sa.String(length=50), server_default='BEGINNER', nullable=False))

    op.create_index(op.f('ix_exercises_category_id'), 'exercises', ['category_id'], unique=False)
    op.create_index(op.f('ix_exercises_primary_muscle_id'), 'exercises', ['primary_muscle_id'], unique=False)

    # 7. Association Tables (Many-to-Many)
    op.create_table(
        'exercise_modalities',
        sa.Column('exercise_id', uuid_col, sa.ForeignKey('exercises.id', ondelete='CASCADE'), primary_key=True, nullable=False),
        sa.Column('modality_id', uuid_col, sa.ForeignKey('training_modalities.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    )
    op.create_index(op.f('ix_exercise_modalities_exercise_id'), 'exercise_modalities', ['exercise_id'], unique=False)
    op.create_index(op.f('ix_exercise_modalities_modality_id'), 'exercise_modalities', ['modality_id'], unique=False)

    op.create_table(
        'exercise_equipment',
        sa.Column('exercise_id', uuid_col, sa.ForeignKey('exercises.id', ondelete='CASCADE'), primary_key=True, nullable=False),
        sa.Column('equipment_id', uuid_col, sa.ForeignKey('equipment.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    )
    op.create_index(op.f('ix_exercise_equipment_exercise_id'), 'exercise_equipment', ['exercise_id'], unique=False)
    op.create_index(op.f('ix_exercise_equipment_equipment_id'), 'exercise_equipment', ['equipment_id'], unique=False)

    op.create_table(
        'exercise_locations',
        sa.Column('exercise_id', uuid_col, sa.ForeignKey('exercises.id', ondelete='CASCADE'), primary_key=True, nullable=False),
        sa.Column('location_id', uuid_col, sa.ForeignKey('locations.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    )
    op.create_index(op.f('ix_exercise_locations_exercise_id'), 'exercise_locations', ['exercise_id'], unique=False)
    op.create_index(op.f('ix_exercise_locations_location_id'), 'exercise_locations', ['location_id'], unique=False)

    op.create_table(
        'exercise_secondary_muscles',
        sa.Column('exercise_id', uuid_col, sa.ForeignKey('exercises.id', ondelete='CASCADE'), primary_key=True, nullable=False),
        sa.Column('muscle_id', uuid_col, sa.ForeignKey('muscles.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    )
    op.create_index(op.f('ix_exercise_secondary_muscles_exercise_id'), 'exercise_secondary_muscles', ['exercise_id'], unique=False)
    op.create_index(op.f('ix_exercise_secondary_muscles_muscle_id'), 'exercise_secondary_muscles', ['muscle_id'], unique=False)


def downgrade() -> None:
    # 1. Drop Association Tables
    op.drop_index(op.f('ix_exercise_secondary_muscles_muscle_id'), table_name='exercise_secondary_muscles')
    op.drop_index(op.f('ix_exercise_secondary_muscles_exercise_id'), table_name='exercise_secondary_muscles')
    op.drop_table('exercise_secondary_muscles')

    op.drop_index(op.f('ix_exercise_locations_location_id'), table_name='exercise_locations')
    op.drop_index(op.f('ix_exercise_locations_exercise_id'), table_name='exercise_locations')
    op.drop_table('exercise_locations')

    op.drop_index(op.f('ix_exercise_equipment_equipment_id'), table_name='exercise_equipment')
    op.drop_index(op.f('ix_exercise_equipment_exercise_id'), table_name='exercise_equipment')
    op.drop_table('exercise_equipment')

    op.drop_index(op.f('ix_exercise_modalities_modality_id'), table_name='exercise_modalities')
    op.drop_index(op.f('ix_exercise_modalities_exercise_id'), table_name='exercise_modalities')
    op.drop_table('exercise_modalities')

    # 2. Remove columns from Exercises
    op.drop_index(op.f('ix_exercises_primary_muscle_id'), table_name='exercises')
    op.drop_index(op.f('ix_exercises_category_id'), table_name='exercises')
    op.drop_column('exercises', 'difficulty')
    op.drop_column('exercises', 'primary_muscle_id')
    op.drop_column('exercises', 'category_id')

    # 3. Drop Taxonomy Lookup Tables
    op.drop_index(op.f('ix_locations_name'), table_name='locations')
    op.drop_table('locations')

    op.drop_index(op.f('ix_muscles_body_part'), table_name='muscles')
    op.drop_index(op.f('ix_muscles_name'), table_name='muscles')
    op.drop_table('muscles')

    op.drop_index(op.f('ix_equipment_name'), table_name='equipment')
    op.drop_table('equipment')

    op.drop_index(op.f('ix_training_modalities_name'), table_name='training_modalities')
    op.drop_table('training_modalities')

    op.drop_index(op.f('ix_exercise_categories_name'), table_name='exercise_categories')
    op.drop_table('exercise_categories')
