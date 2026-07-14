# AI Resume Tailoring App

A local-first, single-user application that tailors a master LaTeX resume to a job description.

## Current Project State (Phase 1 Complete)
Phase 1 has been completed. The app foundation contains:
* FastAPI backend setup with health check, session management, master resume loading/hashing, structural resume parser, and deterministic match scoring.
* React + TypeScript + Vite frontend configured with Tailwind CSS styling and Zustand store.
* Fully passing backend test suite.

---

## Getting Started

### 1. Run the Backend
Ensure you are in the root directory.

Initialize and activate the virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt # or install manually: fastapi uvicorn pydantic pytest httpx
```

Start the FastAPI application server:
```bash
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000
```
The API documentation is available at `http://localhost:8000/docs` and the health endpoint can be checked at `http://localhost:8000/api/health`.

### 2. Run the Frontend
In a new terminal window, navigate to the frontend directory:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser to view the prototype application shell and verify frontend-to-backend communication.

### 3. Run the Tests
To run the automated test suite verifying parser integrity, deterministic scoring boundaries, path safety, and session handling:
```bash
source .venv/bin/activate
PYTHONPATH=. pytest tests/backend/test_phase1.py -v
```
