# Architecture Document

## 1. Architecture Overview

The AI Resume Tailoring App is a local-first, single-user application that uses a React frontend, FastAPI backend, Gemini API, local filesystem storage, and a locally installed LaTeX compiler.

The system uses a clear separation between:

* User Interface
* API Layer
* Application Services
* AI Integration
* Domain Models
* Resume Processing
* LaTeX Compilation
* Local File Storage

The master LaTeX resume is the immutable source of truth.

The application must never directly modify `master_resume.tex`.

All tailoring operations create temporary or generated copies derived from the master resume.

---

## 2. High-Level Architecture

```text
┌─────────────────────────────────────────────┐
│                React Frontend               │
│                                             │
│  API Key Input                              │
│  Job Description Input                      │
│  Optional Job Title                         │
│  Job Analysis                               │
│  Match Report                               │
│  Change Review                              │
│  PDF Preview                                │
│  Export Controls                            │
└──────────────────────┬──────────────────────┘
                       │
                       │ HTTP / JSON
                       ▼
┌─────────────────────────────────────────────┐
│               FastAPI Backend               │
│                                             │
│  API Routes                                 │
│  Request Validation                         │
│  Session Workflow State                     │
│  Error Handling                             │
└──────────────────────┬──────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────┐
│             Application Services            │
│                                             │
│  Gemini Service                             │
│  JD Analyzer                                │
│  Resume Parser                              │
│  Resume Analyzer                            │
│  Match Scoring Service                      │
│  Tailoring Service                          │
│  Change Application Service                 │
│  LaTeX Service                              │
│  File Service                               │
└──────────────┬──────────────┬───────────────┘
               │              │
               ▼              ▼
┌──────────────────────┐   ┌──────────────────┐
│      Gemini API      │   │ Local Filesystem │
│                      │   │                  │
│ JD Analysis          │   │ master_resume   │
│ Change Generation    │   │ generated files │
└──────────────────────┘   └─────────┬────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ LaTeX Compiler   │
                            │                  │
                            │ latexmk /        │
                            │ pdflatex         │
                            └──────────────────┘
```

---

## 3. Core Architectural Principles

### 3.1 Immutable Master Resume

`resume/master_resume.tex` is the single source of truth.

Application code must:

* Read the master resume.
* Parse the master resume.
* Analyze the master resume.
* Create generated copies.

Application code must never:

* Modify the master resume.
* Overwrite the master resume.
* Apply AI-generated changes directly to the master resume.

The File Service should enforce this restriction.

---

### 3.2 Stateless API Key Handling

The Gemini API key is provided by the frontend for the current session.

The API key must:

* Exist only in frontend runtime memory and backend request/process memory.
* Never be persisted.
* Never be written to files.
* Never be stored in environment variables.
* Never be stored in browser `localStorage`.
* Never appear in logs.
* Never appear in exceptions returned to the frontend.

The frontend sends the API key only to backend endpoints that require Gemini access.

The backend must not return the API key in any response.

---

### 3.3 Structured AI Output

Gemini must never directly modify files.

Gemini is responsible only for generating structured analysis and proposed changes.

All Gemini responses must:

1. Request JSON output.

2. Be parsed by the backend.

3. Be validated against typed schemas.

4. Be checked against the master resume.

5. Be rejected if structurally invalid.

6. Be rejected if a proposed modification cannot be safely mapped to existing resume content.

Only deterministic backend application logic may apply accepted changes.

---

### 3.4 Deterministic Resume Modification

The system should avoid asking Gemini to return a complete rewritten LaTeX resume.

Instead:

```text
Master Resume
      │
      ▼
Parse Resume
      │
      ▼
Gemini Generates Structured Change Operations
      │
      ▼
Validate Operations
      │
      ▼
User Accepts / Rejects Changes
      │
      ▼
Backend Applies Accepted Operations
      │
      ▼
Generated LaTeX Resume
```

This architecture provides:

* Better transparency.
* Reliable diff generation.
* Granular accept/reject controls.
* Lower risk of LaTeX corruption.
* Protection against hallucinated content.
* Easier testing.

---

## 4. Technology Stack

### Frontend

* React.
* TypeScript.
* Vite.
* Tailwind CSS.
* React Router.
* TanStack Query for server state.
* Zustand or React Context for temporary workflow state.

### Backend

* Python 3.12+.
* FastAPI.
* Pydantic.
* Uvicorn.
* Gemini Python SDK.

### LaTeX

Preferred:

`latexmk`

Fallback:

`pdflatex`

### Storage

Local filesystem only.

No database is required for the MVP.

---

## 5. System Components

## 5.1 Frontend Application

The frontend is responsible for:

* Collecting the Gemini API key.
* Collecting the Job Description.
* Collecting the optional Job Title.
* Displaying loading and error states.
* Displaying JD analysis.
* Displaying resume match analysis.
* Displaying proposed changes.
* Managing accept/reject decisions.
* Requesting generated resume creation.
* Displaying compilation status.
* Displaying PDF preview.
* Exporting generated files.

The frontend must not:

* Parse LaTeX.
* Modify LaTeX.
* Calculate authoritative match scores.
* Apply resume changes.
* Compile LaTeX.

These operations belong to the backend.

---

## 5.2 Frontend Workflow State

Recommended workflow states:

```text
SESSION_SETUP
      │
      ▼
JOB_INPUT
      │
      ▼
ANALYZING
      │
      ▼
ANALYSIS_READY
      │
      ▼
GENERATING_CHANGES
      │
      ▼
REVIEWING_CHANGES
      │
      ▼
GENERATING_RESUME
      │
      ▼
COMPILING
      │
      ▼
PREVIEW_READY
```

Error states:

```text
API_KEY_INVALID
ANALYSIS_FAILED
CHANGE_GENERATION_FAILED
CHANGE_VALIDATION_FAILED
RESUME_GENERATION_FAILED
LATEX_COMPILATION_FAILED
```

Workflow transitions should be explicit.

The frontend must prevent invalid transitions.

Example:

The user cannot generate a resume before proposed changes have been reviewed.

---

## 5.3 API Layer

Recommended API routes:

```text
POST /api/session/validate-key

POST /api/jobs/analyze

POST /api/resume/match

POST /api/resume/generate-changes

POST /api/resume/generate

POST /api/resume/compile

GET  /api/resume/preview/{session_id}

GET  /api/resume/export/{session_id}/tex

GET  /api/resume/export/{session_id}/pdf

DELETE /api/session/{session_id}
```

All request and response payloads must use typed Pydantic schemas.

---

## 5.4 Session Management

The application does not require authentication.

A temporary workflow session should be created for each tailoring process.

Each session receives a random UUID.

Example:

```text
8f5d1f31-44f0-45f2-b2b7-a20d9f75d82e
```

Session state may contain:

* Session ID.
* Job Description.
* Job Title.
* Parsed JD Analysis.
* Parsed Master Resume Snapshot.
* Initial Match Analysis.
* Proposed Changes.
* Accept/Reject Decisions.
* Generated Resume Path.
* Compiled PDF Path.
* Final Match Analysis.

The Gemini API key should not be stored inside session state.

Session state should exist only in backend process memory for the MVP.

Sessions should expire after a configurable period of inactivity.

Recommended default:

`60 minutes`

Expired sessions should have temporary generated files cleaned up.

---

## 5.5 Gemini Service

File:

```text
backend/services/gemini_service.py
```

Responsibilities:

* Initialize a Gemini client using the API key supplied with the current request.
* Send prompts to Gemini.
* Request structured output.
* Handle Gemini API failures.
* Apply request timeouts.
* Apply retry logic for transient failures.
* Return raw structured responses to the appropriate service.

The Gemini Service must not:

* Store API keys.
* Log API keys.
* Modify resumes.
* Write generated files.
* Calculate match scores.

---

## 5.6 Prompt Management

Prompts should exist separately from application logic.

Recommended structure:

```text
backend/prompts/
├── jd_analysis.py
├── resume_analysis.py
└── change_generation.py
```

Prompts must define:

* AI role.
* Expected input.
* Expected output schema.
* Truthfulness constraints.
* Prohibited modifications.
* LaTeX preservation requirements.

Prompt strings should not be scattered throughout route handlers or services.

---

## 5.7 JD Analyzer

File:

```text
backend/services/jd_analyzer.py
```

Input:

```text
Job Description
Optional Job Title
Gemini API Key
```

Output:

```text
JDAnalysis
```

Responsibilities:

* Send the JD to Gemini through Gemini Service.
* Infer Job Title when missing.
* Extract structured job requirements.
* Normalize skills and keywords.
* Validate Gemini output.

Example domain model:

```text
JDAnalysis

job_title
company_name
seniority_level
required_skills[]
preferred_skills[]
technologies[]
programming_languages[]
frameworks[]
tools[]
responsibilities[]
experience_requirements[]
education_requirements[]
keywords[]
```

---

## 5.8 Resume Parser

File:

```text
backend/services/resume_parser.py
```

The Resume Parser converts the master LaTeX resume into a structured internal representation.

Example:

```text
ParsedResume

metadata
education[]
experience[]
projects[]
skills[]
achievements[]
other_sections[]
```

Every parsed resume item should receive a stable internal ID.

Example:

```text
experience_01_bullet_02
project_02_bullet_01
skill_python
```

These IDs allow Gemini-generated change operations to reference specific resume content safely.

The parser should preserve:

* Original LaTeX content.
* Section order.
* Entry order.
* Bullet order.
* Custom LaTeX commands.

---

## 5.9 Resume Analyzer

File:

```text
backend/services/resume_analyzer.py
```

Responsibilities:

* Compare the Parsed Resume against JD Analysis.
* Identify matched requirements.
* Identify missing requirements.
* Identify weakly represented requirements.
* Identify relevant projects.
* Identify relevant experience.
* Identify irrelevant or low-priority content.
* Identify unsupported JD requirements.

The Resume Analyzer should use deterministic logic where practical.

Gemini may assist with semantic relevance classification, but the backend remains responsible for validation and final scoring inputs.

---

## 5.10 Match Scoring Service

File:

```text
backend/services/scoring_service.py
```

The Resume Match Score must be deterministic.

Example scoring model:

```text
Required Skills Coverage       35%
Preferred Skills Coverage      10%
Keyword Alignment              20%
Experience Alignment           15%
Project Alignment              10%
Education Alignment            10%
                              ----
                              100%
```

The exact weights should be configurable.

The same scoring algorithm must be used before and after tailoring.

The scoring service must return:

```text
MatchScore

total_score
required_skills_score
preferred_skills_score
keyword_score
experience_score
project_score
education_score
matched_requirements[]
missing_requirements[]
unsupported_requirements[]
```

The UI must describe this as an internal Resume Match Score, not an official ATS score.

---

## 5.11 Tailoring Service

File:

```text
backend/services/tailoring_service.py
```

Responsibilities:

* Provide Gemini with JD Analysis.
* Provide Gemini with Parsed Resume.
* Provide Gemini with Resume Match Analysis.
* Request structured change operations.
* Validate returned changes.
* Reject unsupported or unsafe changes.
* Return validated proposed changes.

Gemini should receive structured resume data rather than unrestricted filesystem access.

---

## 5.12 Change Operation Model

Each proposed change should use a structure similar to:

```text
ResumeChange

change_id
change_type
target_id
section
original_content
proposed_content
reason
jd_requirements[]
keywords[]
confidence
```

Supported operations:

```text
REWRITE
REORDER
REMOVE
KEYWORD_ALIGNMENT
EMPHASIS
FORMATTING
```

Each operation must target an existing stable resume item ID.

For rewrite and remove operations:

`original_content` must match the current resume item.

If it does not match, the operation must be rejected.

---

## 5.13 Change Validation Pipeline

Every proposed change must pass through:

```text
Gemini Response
      │
      ▼
JSON Parsing
      │
      ▼
Pydantic Schema Validation
      │
      ▼
Target ID Validation
      │
      ▼
Original Content Verification
      │
      ▼
Truthfulness / Unsupported Claim Checks
      │
      ▼
Operation Conflict Detection
      │
      ▼
Validated Proposed Changes
```

Changes that fail validation should not be displayed as valid suggestions and must never be applied.

---

## 5.14 Change Application Service

Recommended file:

```text
backend/services/change_service.py
```

Responsibilities:

* Receive validated changes.
* Receive user accept/reject decisions.
* Load a fresh copy of the master resume.
* Verify the master resume hash.
* Apply accepted changes.
* Preserve rejected content.
* Detect conflicting accepted operations.
* Generate final LaTeX content.

The Change Application Service must be deterministic.

Gemini must not participate in applying accepted changes.

---

## 5.15 Master Resume Integrity

At application startup:

1. Read `master_resume.tex`.

2. Calculate SHA-256 hash.

Before generating a tailored resume:

1. Read `master_resume.tex`.

2. Calculate SHA-256 hash again.

3. Verify expected master resume integrity.

After generating a tailored resume:

1. Calculate master resume hash again.

2. Verify that the file remains unchanged.

If unexpected modification is detected:

* Stop resume generation.
* Return an integrity error.
* Do not compile the generated resume.

---

## 5.16 File Service

File:

```text
backend/services/file_service.py
```

Responsibilities:

* Read master resume.
* Create session directories.
* Write generated `.tex` files.
* Write compilation outputs.
* Sanitize filenames.
* Resolve safe filesystem paths.
* Prevent path traversal.
* Clean expired session files.
* Enforce master resume protection.

Recommended generated file structure:

```text
generated/
└── <session_id>/
    ├── resume.tex
    ├── resume.pdf
    └── compilation.log
```

The Gemini API key must never be written into this directory.

---

## 5.17 LaTeX Service

File:

```text
backend/services/latex_service.py
```

Responsibilities:

* Validate generated LaTeX.
* Create an isolated compilation workspace.
* Run the LaTeX compiler.
* Enforce compilation timeout.
* Capture stdout and stderr.
* Parse compilation errors.
* Return compilation status.
* Copy successful PDF output to the session directory.

Recommended command:

```text
latexmk -pdf -interaction=nonstopmode -halt-on-error resume.tex
```

Never use:

```text
--shell-escape
```

Compilation should execute only inside the generated session directory.

---

## 5.18 PDF Preview

The backend should expose the generated PDF through:

```text
GET /api/resume/preview/{session_id}
```

The frontend should display the PDF using the browser's native PDF viewer or an embedded PDF component.

The preview endpoint must:

* Validate the session ID.
* Resolve the PDF path safely.
* Verify that the PDF belongs to the requested session.
* Return 404 if compilation has not succeeded.

---

## 6. Core Request Flows

### 6.1 Validate Gemini API Key

```text
Frontend
   │
   │ API Key
   ▼
FastAPI Route
   │
   ▼
Gemini Service
   │
   ▼
Minimal Gemini Request
   │
   ▼
Validation Result
   │
   ▼
Frontend
```

The API key is discarded after request completion.

---

### 6.2 Analyze Job

```text
Frontend
   │
   │ JD + Optional Job Title + API Key
   ▼
FastAPI
   │
   ▼
JD Analyzer
   │
   ▼
Gemini Service
   │
   ▼
Structured JD Analysis
   │
   ▼
Resume Parser
   │
   ▼
Resume Analyzer
   │
   ▼
Scoring Service
   │
   ▼
Initial Match Report
   │
   ▼
Frontend
```

---

### 6.3 Generate Proposed Changes

```text
Frontend
   │
   │ Session ID + API Key
   ▼
FastAPI
   │
   ▼
Tailoring Service
   │
   ▼
Gemini Service
   │
   ▼
Structured Changes
   │
   ▼
Change Validation Pipeline
   │
   ▼
Validated Changes
   │
   ▼
Frontend
```

---

### 6.4 Generate Tailored Resume

```text
Frontend
   │
   │ Session ID + Accept/Reject Decisions
   ▼
FastAPI
   │
   ▼
Change Application Service
   │
   ▼
Fresh Master Resume Copy
   │
   ▼
Apply Accepted Changes
   │
   ▼
Generated resume.tex
   │
   ▼
Final Resume Analysis
   │
   ▼
Final Match Score
   │
   ▼
Frontend
```

---

### 6.5 Compile Resume

```text
Frontend
   │
   │ Session ID
   ▼
FastAPI
   │
   ▼
LaTeX Service
   │
   ▼
Isolated Compilation Workspace
   │
   ▼
latexmk
   │
   ├──── Failure ────► Parsed Compilation Errors
   │
   ▼
resume.pdf
   │
   ▼
PDF Preview + Export
```

---

## 7. Data Models

Recommended Pydantic models:

```text
ValidateKeyRequest
ValidateKeyResponse

AnalyzeJobRequest
JDAnalysis

ParsedResume
ResumeSection
ResumeEntry
ResumeBullet

ResumeMatchAnalysis
MatchScore

GenerateChangesRequest
ResumeChange
GenerateChangesResponse

ChangeDecision
GenerateResumeRequest
GenerateResumeResponse

CompileResumeRequest
CompileResumeResponse

SessionState
APIError
```

Pydantic models should be shared conceptually with TypeScript frontend types.

---

## 8. Error Handling Architecture

All API errors should use a consistent structure:

```text
APIError

code
message
details
retryable
```

Example error codes:

```text
INVALID_API_KEY
GEMINI_RATE_LIMITED
GEMINI_TIMEOUT
GEMINI_INVALID_RESPONSE

INVALID_JOB_DESCRIPTION

MASTER_RESUME_NOT_FOUND
MASTER_RESUME_PARSE_FAILED
MASTER_RESUME_INTEGRITY_FAILED

CHANGE_VALIDATION_FAILED
CHANGE_CONFLICT

RESUME_GENERATION_FAILED

LATEX_COMPILER_NOT_FOUND
LATEX_COMPILATION_TIMEOUT
LATEX_COMPILATION_FAILED

SESSION_NOT_FOUND
SESSION_EXPIRED

FILE_ACCESS_DENIED
```

Sensitive data must never appear in API errors.

---

## 9. Logging

Use structured backend logging.

Logs may contain:

* Request ID.
* Session ID.
* Route.
* Processing duration.
* Gemini request duration.
* Number of proposed changes.
* Number of rejected AI changes.
* Compilation duration.
* Error code.

Logs must never contain:

* Gemini API key.
* Authorization headers.
* Full Job Description by default.
* Full resume content by default.
* Generated resume content.
* Sensitive request payloads.

---

## 10. Security Boundaries

### Boundary 1: Frontend to Backend

Treat all frontend data as untrusted.

Validate:

* Job Description.
* Job Title.
* Session IDs.
* Change decisions.
* Filenames.
* API key presence.

### Boundary 2: Gemini to Backend

Treat all Gemini responses as untrusted.

Validate:

* JSON structure.
* Target IDs.
* Original content.
* Operation types.
* Unsupported claims.
* Conflicting changes.

### Boundary 3: Backend to Filesystem

Validate:

* Paths.
* Session IDs.
* Filenames.
* Master resume protection.
* Generated directory containment.

### Boundary 4: Backend to LaTeX Compiler

Treat generated LaTeX as untrusted input.

Enforce:

* No shell escape.
* Compilation timeout.
* Restricted working directory.
* Safe subprocess invocation.
* Output size limits.

---

## 11. Concurrency

The backend may process multiple requests concurrently even though the MVP is single-user.

Therefore:

* Never use global mutable variables for active workflow state without synchronization.
* Use a thread-safe in-memory Session Store.
* Use unique session directories.
* Prevent concurrent generation or compilation operations for the same session.
* Use per-session locks where necessary.

---

## 12. Session Cleanup

A background cleanup task should periodically:

1. Identify expired sessions.

2. Remove session state from memory.

3. Delete generated session directories.

4. Delete temporary compilation files.

5. Release per-session locks.

Recommended cleanup interval:

`15 minutes`

Recommended session inactivity expiration:

`60 minutes`

---

## 13. Testing Architecture

### Unit Tests

Test:

* JD normalization.
* Resume parsing.
* Stable resume ID generation.
* Match scoring.
* Change validation.
* Change application.
* Change conflict detection.
* Filename sanitization.
* Safe path resolution.
* Master resume integrity checks.
* Session expiration.

### Integration Tests

Test:

* Analyze Job flow.
* Generate Changes flow.
* Accept/Reject flow.
* Generate Resume flow.
* LaTeX compilation.
* PDF generation.
* Session cleanup.

### Security Tests

Test:

* API key does not appear in logs.
* API key is not persisted.
* Path traversal attempts.
* Invalid session IDs.
* Malicious filenames.
* Invalid Gemini responses.
* Unknown resume target IDs.
* Modified original content.
* Dangerous LaTeX commands.
* Compilation timeout behavior.

---

## 14. Recommended Project Structure

```text
resume-tailoring-app/
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── session/
│   │   │   ├── job-input/
│   │   │   ├── job-analysis/
│   │   │   ├── change-review/
│   │   │   └── resume-preview/
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── store/
│   │   ├── types/
│   │   └── utils/
│   └── package.json
│
├── backend/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── session.py
│   │   │   ├── jobs.py
│   │   │   └── resume.py
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── errors.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── models/
│   │   └── session.py
│   │
│   ├── schemas/
│   │   ├── session.py
│   │   ├── job.py
│   │   ├── resume.py
│   │   └── errors.py
│   │
│   ├── services/
│   │   ├── gemini_service.py
│   │   ├── jd_analyzer.py
│   │   ├── resume_parser.py
│   │   ├── resume_analyzer.py
│   │   ├── scoring_service.py
│   │   ├── tailoring_service.py
│   │   ├── change_service.py
│   │   ├── latex_service.py
│   │   └── file_service.py
│   │
│   ├── prompts/
│   │   ├── jd_analysis.py
│   │   ├── resume_analysis.py
│   │   └── change_generation.py
│   │
│   ├── tests/
│   │
│   └── main.py
│
├── resume/
│   └── master_resume.tex
│
├── generated/
│
├── .gitignore
├── README.md
├── PRD.md
└── ARCHITECTURE.md
```

---

## 15. Implementation Order

Antigravity should implement the system in the following order:

1. Create project structure.

2. Configure FastAPI and React applications.

3. Implement typed schemas and domain models.

4. Implement File Service and master resume protection.

5. Implement Resume Parser and stable resume IDs.

6. Implement in-memory Session Store.

7. Implement Gemini Service with session-only API key handling.

8. Implement JD Analyzer.

9. Implement Resume Analyzer.

10. Implement deterministic Match Scoring Service.

11. Implement Tailoring Service.

12. Implement Change Validation Pipeline.

13. Implement Change Application Service.

14. Implement LaTeX compilation.

15. Implement API routes.

16. Implement frontend workflow state.

17. Implement Session Setup screen.

18. Implement Job Input screen.

19. Implement Job Analysis screen.

20. Implement Change Review screen.

21. Implement Resume Preview and Export screen.

22. Implement session cleanup.

23. Add unit tests.

24. Add integration tests.

25. Add security tests.

26. Perform end-to-end testing with the real master resume.

---

## 16. Key Architectural Decision Summary

1. The master LaTeX resume is immutable.

2. Gemini never receives filesystem access.

3. Gemini never directly modifies LaTeX files.

4. Gemini returns structured analysis and change operations.

5. All AI output is treated as untrusted input.

6. Resume changes are applied deterministically by backend code.

7. Every proposed change targets a stable resume item ID.

8. Users explicitly accept or reject proposed changes.

9. The Resume Match Score is deterministic and uses the same algorithm before and after tailoring.

10. The Gemini API key exists only in runtime memory and is never persisted.

11. Temporary workflow state uses an in-memory session store.

12. Generated files are isolated by session.

13. LaTeX compilation occurs locally with shell escape disabled and strict timeouts.

14. The application uses no authentication and no database for the MVP.

15. The architecture prioritizes truthfulness, transparency, master resume protection, and reliable LaTeX generation.
