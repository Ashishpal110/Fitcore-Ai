# FitCore — Test Suite Structure

FitCore enforces rigorous automated testing across both backend and frontend layers.

## Testing Hierarchy

```text
tests/
├── backend/
│   ├── conftest.py          # Pytest shared fixtures, test DB session, async HTTP client
│   ├── unit/                # Unit tests for isolated domain models, utility functions, calculators
│   ├── integration/         # Repository & service layer database integration tests
│   └── api/                 # End-to-end HTTP API tests against FastAPI endpoints
└── frontend/
    └── .gitkeep             # Component, hook, and integration tests (Vitest / Testing Library)
```

## Running Backend Tests
```bash
cd backend
pytest ../tests/backend -v
```
