# RULES.md

## 1. Purpose

This document defines mandatory engineering rules, prohibited practices, approved libraries, error-handling standards, security constraints, and AI boundaries for the AI Resume Tailoring App.

All implementation decisions must follow:

1. `PRD.md`
2. `ARCHITECTURE.md`
3. `RULES.md`

If implementation behavior conflicts with these documents, the documented requirements take priority.

Do not introduce new features, infrastructure, libraries, architectural patterns, or AI capabilities unless they are necessary to satisfy the documented requirements.

---

# 2. Core Rules to Follow

## 2.1 Preserve the Existing Scope

Build only the functionality defined in the PRD and Architecture documents.

Do not add:

* Authentication.
* User accounts.
* Databases.
* Cloud storage.
* Job tracking.
* Cover letter generation.
* Analytics dashboards.
* Multiple AI providers.
* Resume upload functionality.
* Unrequested settings pages.
* Unrequested onboarding flows.
* Unrequested infrastructure.

Prefer the simplest reliable implementation.

---

## 2.2 Master Resume Is Immutable

`resume/master_resume.tex` is the single source of truth.

The application may:

* Read it.
* Parse it.
* Analyze it.
* Hash it.
* Copy it.

The application must never:

* Overwrite it.
* Edit it.
* Delete it.
* Rename it.
* Move it.
* Apply AI-generated changes directly to it.

Every tailored resume must be generated from a fresh copy of the master resume.

Verify master resume integrity before and after resume generation.

---

## 2.3 Gemini API Key Must Never Be Persisted

The Gemini API key is session-only.

The API key may temporarily exist in:

* Frontend runtime memory.
* Backend request memory.
* Gemini client memory during API requests.

The API key must never be stored in:

* `.env` files.
* Source code.
* Configuration files.
* JSON files.
* Databases.
* Browser `localStorage`.
* Browser `sessionStorage`.
* Cookies.
* IndexedDB.
* Backend session state.
* Generated files.
* Logs.
* Error messages.
* Analytics systems.
* Git history.

Never print, serialize, cache, or persist the API key.

Never return the API key from the backend.

---

## 2.4 Treat All External Input as Untrusted

Treat the following as untrusted input:

* Job Description.
* Job Title.
* Gemini API key.
* Session ID.
* Frontend request payloads.
* Change decisions.
* Gemini responses.
* AI-generated content.
* AI-generated LaTeX fragments.
* Filenames.
* Filesystem paths.

Validate inputs before use.

Never trust frontend validation alone.

---

## 2.5 Gemini Must Never Directly Modify Files

Gemini must never:

* Read files directly.
* Write files.
* Delete files.
* Rename files.
* Select filesystem paths.
* Execute commands.
* Invoke the LaTeX compiler.
* Modify `master_resume.tex`.
* Generate files directly.

Gemini receives only explicitly prepared application data.

Gemini returns structured analysis or structured proposed changes.

Backend application logic remains responsible for all filesystem operations and resume modifications.

---

## 2.6 Prefer Deterministic Code Over AI

Use normal application logic whenever the task can be implemented reliably without AI.

Use deterministic code for:

* Resume file loading.
* Resume parsing.
* Stable ID generation.
* Skill normalization where practical.
* Match score calculation.
* Change validation.
* Target verification.
* Original content verification.
* Accept/reject handling.
* Change application.
* Conflict detection.
* Filename sanitization.
* Path validation.
* Master resume integrity verification.
* Session management.
* File cleanup.
* LaTeX compilation.
* Export.

Use Gemini only where semantic understanding or language generation provides meaningful value.

---

# 3. AI Boundaries

## 3.1 Allowed AI Responsibilities

Gemini may:

* Analyze Job Descriptions.
* Infer Job Title when missing.
* Extract job requirements.
* Extract skills and technologies.
* Extract responsibilities.
* Extract important keywords.
* Classify semantic relevance.
* Identify resume content that could be emphasized.
* Suggest rewrites of existing resume content.
* Suggest reordering of existing resume content.
* Suggest removal or de-emphasis of irrelevant content.
* Explain why a change improves alignment.
* Return structured proposed change operations.

---

## 3.2 Prohibited AI Responsibilities

Gemini must not:

* Modify files.
* Modify the master resume.
* Return an unrestricted replacement resume.
* Decide which changes are accepted.
* Apply accepted changes.
* Calculate the authoritative Resume Match Score.
* Compile LaTeX.
* Execute shell commands.
* Select filesystem paths.
* Generate filenames used without sanitization.
* Create session IDs.
* Control application workflow.
* Bypass backend validation.
* Add unsupported resume information.
* Invent qualifications.
* Invent experience.
* Invent skills.
* Invent projects.
* Invent technologies.
* Invent achievements.
* Invent certifications.
* Invent responsibilities.
* Invent metrics.
* Invent dates.
* Change company names.
* Change institution names.
* Misrepresent the user's background.

---

## 3.3 AI Output Must Be Structured

Do not rely on free-form AI responses for application logic.

Gemini outputs used by the application must be structured JSON.

Every AI response must pass through:

```text
Gemini Response
      │
      ▼
JSON Parsing
      │
      ▼
Schema Validation
      │
      ▼
Semantic Validation
      │
      ▼
Target Validation
      │
      ▼
Truthfulness Checks
      │
      ▼
Conflict Detection
      │
      ▼
Application Use
```

If any validation stage fails, reject the affected output.

Never apply malformed AI output.

Never attempt to "best guess" corrupted structured output before applying resume modifications.

---

## 3.4 AI Changes Must Target Stable IDs

Every change operation must reference an existing stable resume item ID.

Examples:

```text
experience_01_bullet_02
project_02_bullet_01
skill_python
```

Never apply a change based only on:

* Section names.
* Text search.
* Array positions supplied by Gemini.
* Approximate string matching.
* AI-generated filesystem locations.

For rewrite and removal operations, verify that `original_content` matches the current content associated with the target ID.

Reject the change if the target or original content does not match.

---

## 3.5 AI Must Not Invent Missing Requirements

If the Job Description requires something unsupported by the master resume, classify it as:

`UNSUPPORTED_REQUIREMENT`

Do not add it to the resume.

Examples:

If the JD requires Kubernetes and the master resume contains no Kubernetes experience:

Correct behavior:

```text
Missing Requirement: Kubernetes
Status: Unsupported by Master Resume
Action: Do Not Add
```

Incorrect behavior:

```text
Added Kubernetes to Skills section.
```

Truthfulness takes priority over Resume Match Score improvement.

---

## 3.6 AI Prompts Must Be Centralized

Store prompts only inside:

```text
backend/prompts/
```

Do not place large prompt strings inside:

* API routes.
* React components.
* Service methods.
* Utility functions.
* Configuration files.

Prompts must explicitly define:

* AI responsibility.
* Input structure.
* Output schema.
* Truthfulness constraints.
* Prohibited behavior.
* LaTeX preservation requirements.

---

# 4. Approved Libraries and Frameworks

Use the smallest dependency set necessary.

## 4.1 Frontend

Approved core libraries:

```text
react
react-dom
typescript
vite
tailwindcss
react-router-dom
@tanstack/react-query
zustand
```

Use:

* React for UI.
* TypeScript with strict mode enabled.
* Vite for development and builds.
* Tailwind CSS for styling.
* React Router for screen routing when routing is necessary.
* TanStack Query for backend server state.
* Zustand for temporary client workflow state.

Do not use both Zustand and React Context for the same state.

Prefer local component state when global state is unnecessary.

---

## 4.2 Backend

Approved core libraries:

```text
fastapi
uvicorn
pydantic
google-genai
httpx
```

Standard Python libraries should be preferred when sufficient.

Examples:

```text
pathlib
uuid
hashlib
json
logging
subprocess
tempfile
shutil
threading
time
datetime
re
```

Use:

* FastAPI for backend APIs.
* Pydantic for request, response, and AI-output validation.
* `google-genai` as the Gemini SDK.
* `httpx` when explicit HTTP client behavior is required.

Do not use multiple Gemini SDKs.

Do not mix `google-generativeai` and `google-genai`.

Use only `google-genai`.

---

## 4.3 Testing

Approved testing libraries:

```text
pytest
pytest-asyncio
httpx
```

Frontend tests may use:

```text
vitest
@testing-library/react
@testing-library/user-event
```

Do not add large end-to-end testing frameworks during the initial MVP unless explicitly required.

---

## 4.4 LaTeX

Preferred compiler:

```text
latexmk
```

Fallback:

```text
pdflatex
```

Use Python `subprocess` with argument arrays.

Correct:

```text
subprocess.run(
    ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "resume.tex"]
)
```

Avoid:

```text
subprocess.run("latexmk ...", shell=True)
```

Never use `shell=True`.

Never enable `--shell-escape`.

---

# 5. Libraries and Technologies to Avoid

Do not add the following without an explicit requirement.

## 5.1 Frontend

Avoid:

* Next.js.
* Remix.
* Angular.
* Vue.
* Redux.
* Redux Toolkit.
* MobX.
* Recoil.
* Multiple state management libraries.
* Axios when `fetch` or existing infrastructure is sufficient.
* Component libraries such as Material UI, Chakra UI, or Ant Design unless explicitly requested.
* Large animation libraries unless necessary.
* Large PDF libraries when browser-native PDF preview is sufficient.

Do not replace the approved frontend stack.

---

## 5.2 Backend

Avoid:

* Django.
* Flask.
* Node.js backend services.
* Express.
* NestJS.
* SQLAlchemy.
* ORMs.
* Redis.
* Celery.
* RabbitMQ.
* Kafka.
* Background queue infrastructure.
* Persistent databases.
* Docker-only architecture.
* Kubernetes.
* Microservices.

The MVP should remain a single FastAPI backend.

---

## 5.3 AI Frameworks

Avoid:

* LangChain.
* LlamaIndex.
* CrewAI.
* AutoGen.
* Semantic Kernel.
* Agent frameworks.
* Multi-agent architectures.
* Autonomous agents.
* Vector databases.
* Embedding databases.
* RAG infrastructure.

The application does not need an agent framework.

Call Gemini directly through `google-genai`.

---

## 5.4 Resume Parsing Libraries

Do not add generic PDF resume parsers or document extraction libraries.

The source resume is LaTeX.

Build a parser designed around the structure of `master_resume.tex`.

Do not over-engineer a universal LaTeX parser.

Support the actual resume structure used by the application.

---

# 6. Error Handling Rules

## 6.1 Never Swallow Errors

Avoid:

```python
try:
    operation()
except Exception:
    pass
```

Every caught exception must be:

* Handled.
* Converted to a domain error.
* Logged safely when appropriate.
* Propagated when the current layer cannot recover.

---

## 6.2 Do Not Expose Raw Exceptions

Never return raw Python exceptions, stack traces, filesystem paths, API responses, or subprocess output directly to the frontend.

Incorrect:

```text
FileNotFoundError: /Users/name/project/resume/master_resume.tex
```

Correct:

```text
code: MASTER_RESUME_NOT_FOUND
message: The master resume could not be loaded.
retryable: false
```

Detailed diagnostics may be logged locally if they contain no secrets.

---

## 6.3 Use Typed Domain Errors

Use a centralized error hierarchy.

Recommended examples:

```text
AppError
ValidationError
GeminiError
GeminiAuthenticationError
GeminiRateLimitError
GeminiTimeoutError
GeminiResponseValidationError
SessionError
SessionNotFoundError
SessionExpiredError
MasterResumeError
MasterResumeIntegrityError
ResumeParsingError
ChangeValidationError
ChangeConflictError
ResumeGenerationError
LatexCompilationError
LatexCompilationTimeoutError
FileSecurityError
```

Map domain errors to consistent API responses.

---

## 6.4 Use Consistent API Error Responses

All API errors must use:

```json
{
  "code": "ERROR_CODE",
  "message": "Safe user-facing message.",
  "details": null,
  "retryable": false
}
```

Do not invent different error formats for different endpoints.

---

## 6.5 Validate at System Boundaries

Validate data when it crosses boundaries.

### Frontend → Backend

Validate:

* Required fields.
* Input length.
* Job Description.
* Job Title.
* Session ID.
* Change decisions.
* API key presence.

### Gemini → Backend

Validate:

* JSON parsing.
* Required fields.
* Types.
* Enums.
* Stable target IDs.
* Original content.
* Unsupported claims.
* Conflicting operations.

### Backend → Filesystem

Validate:

* Paths.
* Filenames.
* Session directories.
* Generated directory containment.
* Master resume protection.

### Backend → LaTeX Compiler

Validate:

* Input file location.
* Working directory.
* Command arguments.
* Timeout.
* Output file existence.
* Output size.

---

## 6.6 Use Timeouts

All external or potentially blocking operations must have timeouts.

Required:

* Gemini API calls.
* API key validation requests.
* LaTeX compilation.

Never allow an external call or compiler process to wait indefinitely.

---

## 6.7 Retry Only Transient Failures

Retries may be used for:

* Temporary Gemini network failures.
* Gemini service unavailable responses.
* Rate limits when retry guidance is available.

Do not retry:

* Invalid API keys.
* Invalid Job Descriptions.
* Schema validation failures.
* Unsupported AI changes.
* Missing master resume.
* Master resume integrity failures.
* Invalid LaTeX caused by generated content.

Use bounded retries.

Recommended maximum:

```text
2 retries
```

Use exponential backoff with jitter for transient Gemini failures.

---

# 7. Filesystem Rules

## 7.1 Use `pathlib`

Use Python `pathlib.Path` for filesystem operations.

Avoid manual path construction using string concatenation.

---

## 7.2 Prevent Path Traversal

All generated paths must remain inside approved directories.

Resolve paths before access.

Verify containment.

Never trust:

* Session IDs.
* Job Titles.
* Filenames.
* AI-generated values.

as filesystem paths.

---

## 7.3 Sanitize Filenames

Export filenames may use:

* User name configured in application code.
* Job Title.
* `Resume`.

Remove or replace:

* `/`
* `\`
* `..`
* Control characters.
* Reserved filesystem characters.
* Excessive whitespace.

Never use unsanitized AI output as a filename.

---

## 7.4 Generated Files Must Be Isolated

Each session must have its own generated directory.

```text
generated/<session_id>/
```

Do not allow sessions to share writable directories.

---

## 7.5 Generated Files Must Not Be Committed

Add generated output directories to `.gitignore`.

At minimum:

```text
generated/
frontend/node_modules/
frontend/dist/
backend/__pycache__/
.pytest_cache/
*.pyc
```

Do not ignore `resume/master_resume.tex`.

---

# 8. LaTeX Rules

## 8.1 Preserve Resume Formatting

The application should preserve:

* Document class.
* Packages.
* Custom commands.
* Section order unless an accepted reorder operation changes it.
* Formatting commands.
* Spacing rules.
* Existing resume design.

Do not regenerate the full LaTeX document from scratch.

Apply accepted changes to a fresh master resume copy.

---

## 8.2 Treat Generated LaTeX as Untrusted

Before compilation:

* Verify file location.
* Scan for prohibited dangerous commands.
* Enforce compilation timeout.
* Disable shell escape.
* Restrict compiler working directory.
* Limit output size where practical.

Reject dangerous commands when introduced through generated content.

Examples include:

```text
\write18
\input
\include
\openout
\openin
\usepackage{shellesc}
```

Allow required static commands already present in the trusted master resume only when explicitly necessary.

---

## 8.3 Do Not Automatically Repair LaTeX with Gemini

If compilation fails:

1. Capture the compiler error.

2. Parse it into a safe application error.

3. Show the error to the user.

4. Allow the user to return to Change Review.

Do not automatically send the full generated resume and compiler logs back to Gemini for unrestricted repair.

Automatic AI repair is outside the MVP scope.

---

# 9. Session Rules

Use random UUIDs for session IDs.

Never derive session IDs from:

* Job Titles.
* User names.
* Timestamps alone.
* Sequential integers.

The Gemini API key must never be stored in session state.

Session state must remain in memory.

Sessions must expire after inactivity.

Default expiration:

```text
60 minutes
```

Cleanup interval:

```text
15 minutes
```

Expired sessions must:

* Be removed from memory.
* Have temporary files deleted.
* Release associated locks.

---

# 10. Logging Rules

Use structured logging.

Allowed log fields:

* Request ID.
* Session ID.
* Route.
* HTTP status.
* Processing duration.
* Gemini request duration.
* Number of generated changes.
* Number of invalid AI changes.
* Number of accepted changes.
* Compilation duration.
* Error code.

Never log:

* Gemini API keys.
* Authorization headers.
* Full request bodies.
* Full Job Descriptions by default.
* Full resume content.
* Full Gemini prompts containing resume content.
* Full Gemini responses containing resume content.
* Generated LaTeX.
* Personal resume information.
* Raw compiler logs at normal log levels.

---

# 11. Frontend Rules

Use TypeScript strict mode.

Avoid `any`.

Prefer explicit domain types.

Do not duplicate backend business logic in the frontend.

The frontend may:

* Validate forms.
* Manage temporary UI state.
* Display backend results.
* Manage accept/reject decisions.
* Request backend operations.

The frontend must not:

* Calculate the authoritative Resume Match Score.
* Parse the master resume.
* Apply resume changes.
* Compile LaTeX.
* Persist the Gemini API key.

Every async operation must display:

* Loading state.
* Success state when appropriate.
* Error state.
* Disabled duplicate-submit controls.

---

# 12. Backend Rules

Keep route handlers thin.

Route handlers should:

1. Validate request data.

2. Call the appropriate service.

3. Return typed responses.

Do not place business logic inside API routes.

Services must have clear responsibilities.

Avoid circular dependencies between services.

Do not create generic `utils.py` files containing unrelated logic.

Prefer focused modules with explicit names.

---

# 13. Code Quality Rules

Follow:

* Single Responsibility Principle.
* Clear module boundaries.
* Explicit typing.
* Small focused functions.
* Descriptive names.
* Dependency injection where it improves testing.
* Minimal side effects.
* Deterministic behavior where possible.

Avoid:

* Premature abstraction.
* Deep inheritance hierarchies.
* Generic base classes without clear value.
* Large service classes.
* God objects.
* Hidden global state.
* Magic strings.
* Magic numbers.
* Duplicate business logic.
* Dead code.
* Commented-out code.
* Placeholder implementations presented as complete.

---

# 14. Testing Rules

Every critical deterministic component must have unit tests.

Required unit tests:

* Master resume loading.
* Master resume hashing.
* Stable resume ID generation.
* Resume parsing.
* Match scoring.
* AI output schema validation.
* Target ID validation.
* Original content validation.
* Unsupported claim rejection.
* Change conflict detection.
* Accept/reject behavior.
* Change application.
* Filename sanitization.
* Path containment.
* Session expiration.
* Session cleanup.

Required integration tests:

* API key validation.
* Job analysis.
* Match analysis.
* Change generation with mocked Gemini responses.
* Resume generation.
* LaTeX compilation.
* PDF generation.
* Export.

Never use real Gemini API calls in automated tests.

Mock external Gemini requests.

---

# 15. Stuff to Avoid

Do not:

* Rewrite the entire resume when targeted changes are sufficient.
* Ask Gemini to return the final `.tex` file.
* Let Gemini apply changes.
* Trust AI output without validation.
* Add missing skills just because they appear in the JD.
* Optimize the Resume Match Score by introducing unsupported claims.
* Use an AI-generated score as the authoritative score.
* Modify the master resume.
* Persist the Gemini API key.
* Add a database.
* Add authentication.
* Add agent frameworks.
* Add vector databases.
* Add unnecessary dependencies.
* Add multiple state management solutions.
* Add microservices.
* Add cloud infrastructure.
* Add background queues.
* Use `shell=True`.
* Use LaTeX shell escape.
* Expose raw exceptions.
* Swallow exceptions.
* Retry permanent failures.
* Trust frontend validation.
* Trust Gemini responses.
* Trust user-provided filenames.
* Trust session IDs as paths.
* Log sensitive resume content.
* Mix business logic into route handlers.
* Mix business logic into React components.
* Create abstractions before they are needed.
* Implement future features during the MVP.
* Change the approved technology stack without a concrete requirement.
* Silently ignore invalid AI changes.
* Automatically accept AI changes.
* Automatically repair failed LaTeX using Gemini.
* Claim that the Resume Match Score is an official ATS score.

---

# 16. Decision Priority

When making an implementation decision, use the following priority order:

```text
1. Protect Master Resume Integrity

2. Preserve Truthfulness

3. Protect Gemini API Key

4. Prevent Unsafe AI Behavior

5. Validate External Inputs

6. Preserve Valid LaTeX

7. Maintain User Control Over Changes

8. Prefer Deterministic Code

9. Keep Architecture Simple

10. Improve Resume-to-JD Alignment
```

A higher Resume Match Score must never take priority over truthfulness, security, resume integrity, or user control.

---

# 17. Final Implementation Rule

When uncertain whether to add a library, abstraction, feature, AI capability, infrastructure component, or automatic behavior:

Do not add it by default.

Implement the smallest reliable solution that satisfies `PRD.md`, `ARCHITECTURE.md`, and `RULES.md`.

If a requested implementation conflicts with these documents, identify the conflict before changing the architecture or system behavior.
