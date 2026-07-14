# AI Resume Tailoring App

A local-first, single-user application that tailors a master LaTeX resume to a job description.

## Project Overview

This app is designed to help you quickly, transparently, and securely tailor your LaTeX resume for specific job descriptions. 
It uses the Gemini API to analyze job descriptions and propose granular, structured changes that you can individually accept or reject.
Most importantly, it ensures your "Master Resume" is never directly modified and relies on strict security and privacy constraints.

**Key Features:**
* **Immutable Master Resume:** Your `Resume/master_resume.tex` (or `Resume/main.tex`) acts as the ultimate source of truth and is strictly protected.
* **Session-Only API Keys:** The Gemini API key is provided during runtime and is never saved, logged, or cached.
* **Deterministic Scoring:** Gives you a consistent breakdown of your resume match score, separating actual content fit from AI suggestion logic.
* **Granular Review:** Shows diffs for every change and allows you to decide exactly what is accepted or rejected before generating a final PDF.
* **Privacy Focused:** Everything executes locally except for the structured API calls to Gemini. Generated files are written to a temporary local `generated/` directory that is automatically purged.

---

## Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- LaTeX compiler (`latexmk` or `pdflatex`) installed on your system path.
  - MacOS: `brew install mactex` or `mactex-no-gui`
  - Ubuntu/Debian: `sudo apt-get install texlive-full` (or `latexmk`)

### 1. Set Up the Backend
Ensure you are in the root directory.

Initialize and activate the virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
# Install requirements
pip install -r backend/requirements.txt
```
*(If `requirements.txt` is not present, use: `pip install fastapi uvicorn pydantic google-genai httpx pytest`)*

Start the FastAPI application server:
```bash
PYTHONPATH=. uvicorn backend.main:app --reload --port 8001
```
The API documentation is available at `http://localhost:8001/docs`.

### 2. Set Up the Frontend
In a new terminal window, navigate to the frontend directory:
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser to launch the AI Resume Tailor application.

### 3. Provide Your Master Resume
The application expects your master resume to be located at:
```
Resume/main.tex
```
*(Make sure this file is a valid LaTeX resume document.)*

### 4. Running the Test Suite
To run the automated backend test suite verifying the resume parser, AI generation bounds, safe LaTeX compilation, and secure path boundaries:
```bash
source .venv/bin/activate
PYTHONPATH=. pytest tests/backend/
```

---

## Architecture & Security Model

The system uses a strict pipeline for generating changes:
1. **Gemini API** is instructed to generate *structured JSON changes* mapping only to stable target IDs parsed deterministically from your resume.
2. **Backend Validation** guarantees Gemini does not fabricate data, change dates/companies, or inject unrequested skills.
3. **Change Pipeline** guarantees that Gemini has no filesystem or LaTeX compiler access. It merely provides JSON diff recommendations.
4. **Session Cleanup** ensures temporary artifacts (`generated/<uuid>/`) are purged automatically after a timeout (default 60 minutes) or upon session completion.
