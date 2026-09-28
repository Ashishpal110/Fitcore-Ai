-- FitCore Initial PostgreSQL Database Setup
-- This script prepares required extensions for UUID generation and performance.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Note: Tables will be created and managed via Alembic migrations in Phase 2.
