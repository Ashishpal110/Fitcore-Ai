# FitCore — Architecture Overview

## 1. Architectural Style: Modular Monolith
FitCore is built as a modular monolith. It avoids unnecessary microservice complexity, message queues, and multi-service overhead while retaining clean boundary isolation between modules.

```text
┌────────────────────────────────────────────────────────────┐
│                    Frontend (React + TS)                   │
│           Pages ── Components ── Hooks ── API Client       │
└─────────────────────────────┬──────────────────────────────┘
                              │ HTTP / JSON
                              ▼
┌────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI Monolith)               │
│                                                            │
│   API Route Layer (/api/v1)                                │
│       ├── Validates HTTP requests                          │
│       └── Serializes responses via Pydantic                │
│                                                            │
│   Service Layer (Business Logic)                           │
│       ├── Domain calculations & business rules             │
│       ├── Ownership & authorization checks                 │
│       └── Transaction orchestration                        │
│                                                            │
│   Repository / Data Access Layer                           │
│       ├── Encapsulates database queries                    │
│       └── Interacts with SQLAlchemy ORM                    │
│                                                            │
│   SQLAlchemy Models Layer                                  │
│       └── Declarative PostgreSQL entity mappings           │
└─────────────────────────────┬──────────────────────────────┘
                              │ Asyncpg / Psycopg2
                              ▼
┌────────────────────────────────────────────────────────────┐
│                     PostgreSQL Database                    │
└────────────────────────────────────────────────────────────┘
```

---

## 2. Layer Responsibilities & Rules

### API Routes (`app/api/v1/endpoints/`)
* **DO**: Accept requests, inject dependencies (`get_db`, current user), delegate to service layer, return Pydantic schema responses with proper HTTP status codes.
* **DON'T**: Run direct raw database queries, perform heavy business calculations, or leak internal exceptions directly.

### Pydantic Schemas (`app/schemas/`)
* **DO**: Define strict types for Request Payloads and Response DTOs. Validate field constraints (e.g. positive numbers, non-empty strings).
* **DON'T**: Embed business logic or database session interactions.

### Service Layer (`app/services/`)
* **DO**: Enforce business rules, user ownership validation, multi-entity transactions, and domain-specific calculations.
* **DON'T**: Handle HTTP-specific concerns like request headers or status codes directly.

### Repository Layer (`app/repositories/`)
* **DO**: Perform CRUD operations and optimize queries (filtering, joins, eager loading).
* **DON'T**: Handle authorization decisions or business validation rules.

### SQLAlchemy Models (`app/models/`)
* **DO**: Define database tables, columns, indexes, foreign keys, and relationships.
* **DON'T**: Contain presentation logic.
