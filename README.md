# FitCore

FitCore is a modern, responsive, and robust workout logging and progress-tracking application designed for athletes, fitness enthusiasts, and everyday lifters.

## Project Purpose
FitCore enables users to quickly record workouts across diverse modalities—including gym/strength training, bodyweight/calisthenics, cardio, running, cycling, HIIT, and functional training—and retrieve actionable analytics on their training history without clutter, unnecessary social noise, or nutrition bloat.

---

## High-Level Architecture
FitCore is designed as a clean, modular monolith with clear layer boundaries:

```text
Frontend (React + TypeScript + Vite + Tailwind CSS)
   │
   ▼ HTTP / JSON
FastAPI REST API (/api/v1)
   │
   ▼
Pydantic Schemas & DTOs
   │
   ▼
Service Layer (Business Logic & Authorization)
   │
   ▼
Repository Layer (Data Access)
   │
   ▼
SQLAlchemy ORM
   │
   ▼
PostgreSQL Database
```

---

## Planned Technology Stack

### Backend
* **Language & Framework**: Python 3.11+, FastAPI
* **Data Validation**: Pydantic v2
* **ORM & Database Tooling**: SQLAlchemy 2.0+, Alembic
* **Database**: PostgreSQL
* **Authentication** *(Future Phase)*: JWT (JSON Web Tokens), Argon2 / Passlib password hashing
* **Testing**: pytest, httpx, pytest-asyncio

### Frontend
* **Core**: React 18 / 19, TypeScript, Vite
* **Styling**: Tailwind CSS
* **Routing**: React Router v6 / v7
* **Server State**: TanStack Query (React Query)
* **Form & Validation**: React Hook Form, Zod
* **Visualization**: Recharts
* **Icons**: Lucide React

---

## Project Structure
```text
FitCore/
├── frontend/             # React + TypeScript Vite frontend application
│   ├── public/           # Static web assets
│   └── src/
│       ├── api/          # API client & endpoint definitions
│       ├── components/   # Reusable UI components & layouts
│       ├── hooks/        # Custom React hooks
│       ├── pages/        # Route pages
│       ├── routes/       # Router configuration
│       ├── types/        # TypeScript interfaces & types
│       └── utils/        # Utility helpers
├── backend/              # FastAPI Python backend application
│   ├── alembic/          # Database migrations
│   └── app/
│       ├── api/v1/       # REST API endpoints & route aggregators
│       ├── core/         # Settings, database connection, security base
│       ├── models/       # SQLAlchemy database models
│       ├── repositories/ # Database query / data access layer
│       ├── schemas/      # Pydantic request/response schemas
│       └── services/     # Core business logic layer
├── database/             # Database initialization scripts and documentation
├── scripts/              # Developer utility and startup scripts
├── tests/                # Automated tests (unit, integration, API, frontend)
├── docs/                 # Architectural and API documentation
├── .env.example          # Environment variables template
├── .gitignore            # Git exclusion rules
├── README.md             # Project documentation
└── PROJECT_STATUS.md     # Development roadmap & status tracker
```

---

## Development Prerequisites
* **Node.js**: v18.0.0 or higher
* **Python**: v3.11 or higher
* **PostgreSQL**: v14.0 or higher (for database-connected phases)

---

## Getting Started (Local Development)

### 1. Environment Setup
Copy the template environment file:
```bash
cp .env.example .env
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv

# Windows:
.venv\Scripts\activate
# Unix/MacOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Backend will be available at: `http://localhost:8000`  
Interactive API Docs (Swagger): `http://localhost:8000/docs`

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend development server will be available at: `http://localhost:5173`

---

## Current Implementation Status
* **Current Phase**: Phase 0 (Foundation) — **Complete**
* See [`PROJECT_STATUS.md`](./PROJECT_STATUS.md) for detailed phase tracking and development roadmap.
