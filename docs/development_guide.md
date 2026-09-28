# FitCore — Local Development Guide

## Prerequisites
- **Python**: 3.11+
- **Node.js**: 18.0+
- **PostgreSQL**: 14+ (or Docker)

## Step-by-Step Local Setup

### 1. Repository Setup
```bash
git clone <repository-url>
cd FitCore
cp .env.example .env
```

### 2. Backend Setup
1. Create and activate a virtual environment:
   ```bash
   cd backend
   python -m venv .venv
   
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   - Health check: `http://localhost:8000/api/v1/health`
   - Interactive docs: `http://localhost:8000/docs`

### 3. Frontend Setup
1. Install Node dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the Vite development server:
   ```bash
   npm run dev
   ```
   - Application URL: `http://localhost:5173`

### 4. Running Backend Tests
From the `backend` directory:
```bash
pytest ../tests/backend -v
```
