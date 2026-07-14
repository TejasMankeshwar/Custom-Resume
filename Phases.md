# PHASES.md

## Purpose

This document defines the development phases for the AI Resume Tailoring App.

The app should **not be built entirely in one shot**, because AI-generated resume changes, LaTeX modification, compilation, and API-key security need to be tested separately.

The application should be built in **4 phases**.

Before starting any phase, Antigravity must read:

* `PRD.md`
* `ARCHITECTURE.md`
* `RULES.md`
* `PHASES.md`

Antigravity must implement only the requested phase and must not prematurely implement future phases.

---

# Phase 1 — Project Setup and Core Backend

## Goal

Create the project foundation and implement the core non-AI resume functionality.

## Implement

### Project Setup

Create:

* React + TypeScript + Vite frontend.
* Tailwind CSS.
* FastAPI backend.
* Required project structure.
* `.gitignore`.
* Basic frontend/backend communication.

### Master Resume

Implement:

* Load `resume/master_resume.tex`.
* Treat the master resume as read-only.
* Calculate and verify its SHA-256 hash.
* Create generated resume copies without modifying the master resume.

### Resume Parser

Implement:

* Parse the actual structure of `master_resume.tex`.
* Extract sections, entries, bullets, projects, experience, education, and skills.
* Generate stable IDs for resume items.

Examples:

```text
experience_01_bullet_02
project_02_bullet_01
skill_python
```

### Session Management

Implement:

* Temporary in-memory sessions.
* UUID session IDs.
* Session creation and deletion.
* Generated session directories.

Do not store Gemini API keys in sessions.

### Match Scoring

Implement the deterministic Resume Match Score system.

The score must:

* Use structured JD data.
* Produce scores from 0–100.
* Use the same algorithm before and after tailoring.
* Never use Gemini to directly generate the score.

### Tests

Test:

* Master resume loading.
* Master resume protection.
* Resume parsing.
* Stable IDs.
* Session management.
* Filename sanitization.
* Path safety.
* Match scoring.

## Phase Completion Criteria

Phase 1 is complete when:

* Frontend and backend run.
* Master resume loads and remains unchanged.
* Resume parsing works.
* Stable IDs are generated.
* Sessions work.
* Deterministic scoring works.
* Tests pass.

---

# Phase 2 — Gemini Integration and Resume Tailoring Logic

## Goal

Implement the complete AI workflow without building the final polished UI.

## Implement

### Session-Only Gemini API Key

Implement:

* API key input.
* Show/Hide Key.
* Validate Key.
* Clear Key.

The API key must never be persisted, logged, or stored in backend session state.

### Job Inputs

Implement:

* Job Description input.
* Optional Job Title input.
* Job Title inference when missing.

### JD Analysis

Use Gemini to extract:

* Job Title.
* Company.
* Seniority.
* Required Skills.
* Preferred Skills.
* Technologies.
* Responsibilities.
* Keywords.
* Experience requirements.
* Education requirements.

Validate all Gemini responses with Pydantic schemas.

### Initial Match Analysis

Compare the structured JD analysis against the master resume.

Display:

* Initial Match Score.
* Matched requirements.
* Missing requirements.
* Unsupported requirements.

### Tailoring Suggestions

Use Gemini to generate structured resume changes.

Each change must contain:

```text
change_id
change_type
target_id
section
original_content
proposed_content
reason
jd_requirements
keywords
confidence
```

### Change Validation

Validate:

* Target IDs.
* Original content.
* Unsupported claims.
* Fabricated skills.
* Fabricated metrics.
* Changed dates.
* Changed company names.
* Changed institution names.
* Duplicate changes.
* Conflicting changes.
* Dangerous LaTeX commands.

Gemini must never directly modify files.

### Tests

Use mocked Gemini responses.

Test:

* Valid and invalid API keys.
* JD analysis.
* Invalid Gemini output.
* Structured change generation.
* Unsupported claim rejection.
* Target validation.
* Original content validation.
* AI key non-persistence.

## Phase Completion Criteria

Phase 2 is complete when:

* Gemini API integration works.
* API key remains session-only.
* JD analysis works.
* Initial Match Score is generated.
* Structured changes are generated.
* Invalid or unsafe changes are rejected.
* No resume files are modified by Gemini.
* Tests pass.

---

# Phase 3 — Change Review, Resume Generation, and PDF

## Goal

Complete the main user workflow.

## Implement

### Change Review Interface

Display:

* Original content.
* Proposed content.
* Change type.
* Reason.
* Related JD requirements.
* Keywords.
* Confidence.

Controls:

* Accept.
* Reject.
* Accept All.
* Reject All.
* Reset Decisions.

No change should be accepted automatically.

### Resume Generation

After all decisions are made:

* Load a fresh master resume copy.
* Verify master resume integrity.
* Apply only accepted changes.
* Preserve rejected content.
* Generate `resume.tex`.
* Never modify `master_resume.tex`.

### LaTeX Compilation

Implement:

* Local `latexmk` compilation.
* `pdflatex` fallback.
* Compilation timeout.
* Safe subprocess execution.
* No `shell=True`.
* No shell escape.
* Safe compilation errors.

### PDF Preview

Implement:

* Embedded PDF preview.
* Compilation status.
* Compilation errors.

### Final Match Report

Display:

```text
Before Match Score → After Match Score
```

Also display:

* Score improvement.
* Newly covered requirements.
* Remaining gaps.
* Unsupported requirements.
* Accepted changes.
* Rejected changes.

### Export

Allow export of:

* Tailored `.tex`.
* Compiled `.pdf`.

### Tests

Test:

* Accept/reject changes.
* Only accepted changes are applied.
* Master resume remains unchanged.
* LaTeX compilation.
* Compilation failures.
* PDF generation.
* Final scoring.
* `.tex` export.
* `.pdf` export.

## Phase Completion Criteria

Phase 3 is complete when the complete workflow works:

```text
Enter API Key
      ↓
Paste JD + Optional Job Title
      ↓
Analyze Job
      ↓
View Initial Match
      ↓
Generate Suggestions
      ↓
Review Changes
      ↓
Accept / Reject
      ↓
Generate Resume
      ↓
Compile LaTeX
      ↓
Preview PDF
      ↓
View Final Match
      ↓
Export TEX / PDF
```

Tests must pass.

---

# Phase 4 — UI Polish, Security Review, and Final Testing

## Goal

Turn the working application into a stable and polished MVP.

## Implement

### UI Polish

Improve:

* Responsive layout.
* Loading states.
* Error states.
* Empty states.
* Workflow progress indicator.
* Match Score visualization.
* Change diff visualization.
* PDF preview experience.
* Buttons and disabled states.
* Clear API key security messaging.

Do not redesign working functionality unnecessarily.

### Security Review

Verify:

* API key is never persisted.
* API key is never logged.
* API key is never included in errors.
* Master resume cannot be modified.
* Path traversal is blocked.
* Gemini output is always validated.
* Unsupported claims are rejected.
* Dangerous LaTeX commands are blocked.
* `shell=True` is never used.
* Shell escape is disabled.

### Session Cleanup

Implement:

* Session expiration.
* Generated file cleanup.
* Temporary file cleanup.

### Final Testing

Run:

* Backend tests.
* Frontend tests.
* Integration tests.
* Security tests.

Perform full manual testing with:

* Strong-match JD.
* Partial-match JD.
* Weak-match JD.
* JD requiring unsupported skills.
* Invalid API key.
* Invalid Gemini response.
* LaTeX compilation failure.

### Documentation

Create/update `README.md` with:

* Installation.
* Running frontend.
* Running backend.
* LaTeX requirements.
* Updating `master_resume.tex`.
* Gemini API key behavior.
* Running tests.

## Phase Completion Criteria

Phase 4 is complete when:

* Full workflow works reliably.
* UI is polished and responsive.
* Security requirements are satisfied.
* API key is never persisted.
* Master resume remains unchanged.
* AI cannot introduce unsupported claims.
* Tests pass.
* README is complete.

The MVP is now complete.

---

# Antigravity Phase Execution Rule

When starting a phase, use:

```text
Read PRD.md, ARCHITECTURE.md, RULES.md, and PHASES.md.

Inspect the existing project.

Implement only Phase <NUMBER>.

Do not implement future phases.

Preserve working functionality from previous phases.

Follow all architecture, security, AI, library, and error-handling rules.

After implementation:

1. Run relevant tests.
2. Verify the application starts.
3. Report files created or modified.
4. Report tests performed and results.
5. Report any remaining issues.
6. Confirm whether the phase completion criteria are satisfied.

Do not proceed to the next phase.
```
