# Product Requirements Document (PRD)

## Product Name

**AI Resume Tailoring App**

## 1. Product Overview

The AI Resume Tailoring App is a local-first, single-user application that tailors a master LaTeX resume to a specific job description using the Gemini API.

The master resume is stored directly within the project and acts as the single source of truth. Users do not upload their resume through the frontend.

The user provides:

1. A Job Description (required).
2. A Job Title (optional).

The application analyzes the job description, compares it against the master resume, proposes truthful resume modifications, allows the user to review and accept or reject changes, generates the final LaTeX resume, compiles it to PDF, and provides both formats for export.

The Gemini API key is entered through the frontend for every session and must never be permanently stored.

---

## 2. Product Goals

The application should:

* Tailor the master resume to a specific job description.
* Improve alignment between the resume and job requirements.
* Preserve factual accuracy.
* Never fabricate skills, experience, projects, achievements, education, certifications, or metrics.
* Clearly explain every proposed resume modification.
* Allow granular control over AI-generated changes.
* Preserve valid LaTeX structure.
* Maintain the existing resume design and formatting.
* Prefer keeping the final resume within one page.
* Generate both LaTeX and PDF outputs.
* Keep the Gemini API key private and session-only.

---

## 3. Target User

The initial version is a personal, single-user application.

The application does not require:

* Authentication.
* User accounts.
* Multi-user support.
* Cloud databases.
* Job application tracking.
* Cover letter generation.

---

## 4. Core User Flow

1. User launches the application.

2. User enters a Gemini API key.

3. The application validates the API key.

4. The API key is kept only for the current session.

5. User enters:

   * Job Description (required).
   * Job Title (optional).

6. If the Job Title is empty, the application attempts to infer it from the Job Description.

7. User clicks **Analyze Job**.

8. The application analyzes the Job Description.

9. The application loads the master LaTeX resume from the backend.

10. The application compares the master resume against the Job Description.

11. The application displays the initial Resume Match Analysis.

12. User clicks **Generate Tailoring Suggestions**.

13. Gemini generates structured resume modification suggestions.

14. The application displays all proposed changes.

15. The user reviews each change and can:

    * Accept the change.
    * Reject the change.
    * Accept all changes.
    * Reject all changes.

16. Accepted changes are applied to a generated copy of the master resume.

17. The master resume is never modified.

18. The application validates and compiles the generated LaTeX.

19. The user previews the generated PDF.

20. The application displays the final Resume Match Analysis.

21. The user exports the final `.tex` file and/or `.pdf` file.

---

## 5. Functional Requirements

### 5.1 Gemini API Key Management

The application must provide a frontend interface for entering the Gemini API key.

Features:

* API key input field.
* Password-masked input.
* Show/Hide API key.
* Validate API key.
* Replace API key.
* Clear API key.
* Display API key validation status.
* Disable AI functionality until a valid API key is provided.

Security requirements:

* Never store the API key in the project.
* Never commit the API key to GitHub.
* Never write the API key to `.env` files.
* Never write the API key to application files.
* Never store the API key in a database.
* Never store the API key in browser `localStorage`.
* Never include the API key in application logs.
* Never include the API key in error messages.
* Never expose the API key in generated files.

The API key may temporarily exist in frontend and backend process memory while processing Gemini requests.

The key must be discarded when the session ends.

---

### 5.2 Job Input Interface

The primary application interface must contain two job-related inputs.

#### Job Description

Required multiline text area.

Features:

* Paste Job Description.
* Edit Job Description.
* Clear Job Description.
* Character count.
* Input validation.

The application must prevent analysis when the Job Description is empty.

#### Job Title

Optional text input.

Features:

* Enter Job Title manually.
* Edit Job Title.
* Clear Job Title.

If no Job Title is provided, the application should infer the most likely Job Title from the Job Description.

---

### 5.3 Master Resume Management

The master resume must exist directly inside the project.

Recommended location:

`/resume/master_resume.tex`

Requirements:

* Automatically load the master resume.
* Treat the master resume as read-only during application execution.
* Never allow Gemini to directly modify the master resume.
* Never overwrite the master resume.
* Create generated copies for every tailoring session.
* Preserve the original LaTeX formatting and commands.

The user will manually update `master_resume.tex` when necessary.

---

### 5.4 Job Description Analysis

The application must analyze the Job Description and extract:

* Job Title.
* Company Name, when available.
* Seniority Level.
* Required Skills.
* Preferred Skills.
* Technologies.
* Programming Languages.
* Frameworks.
* Tools.
* Responsibilities.
* Experience Requirements.
* Education Requirements.
* Important Keywords.

The output should be structured data rather than unstructured AI-generated text.

---

### 5.5 Resume Match Analysis

The application must compare the Job Description against the master resume.

The analysis should identify:

* Resume Match Score.
* Matched Skills.
* Missing Skills.
* Matched Keywords.
* Missing Keywords.
* Strongly represented qualifications.
* Weakly represented qualifications.
* Relevant Projects.
* Relevant Experience.
* Irrelevant or low-priority content.
* Job requirements that cannot truthfully be added to the resume.

The application must clearly distinguish between:

* Requirements already supported by the resume.
* Requirements that can be better emphasized.
* Requirements unsupported by the resume.

Unsupported requirements must never be fabricated.

---

### 5.6 Resume Match Score

The application must calculate a Resume Match Score before tailoring.

The score should be based on deterministic application logic using structured analysis data rather than asking Gemini to directly generate an arbitrary score.

The scoring system should consider:

* Required skill coverage.
* Preferred skill coverage.
* Keyword alignment.
* Relevant experience alignment.
* Relevant project alignment.
* Education requirement alignment.

The same scoring algorithm must be used before and after tailoring.

The final interface should display:

`Before Tailoring Score → After Tailoring Score`

The scoring system must clearly indicate that it is an internal alignment score and not an official ATS score.

---

### 5.7 AI Resume Tailoring

Gemini should analyze the Job Description and master resume and propose resume modifications.

Allowed modifications include:

* Rewrite existing bullet points.
* Improve clarity and impact.
* Emphasize relevant technologies.
* Emphasize relevant experience.
* Emphasize relevant projects.
* Reorder existing bullet points.
* Reorder skills.
* Reorder projects.
* Reorder experience entries when appropriate.
* Remove or de-emphasize irrelevant content.
* Add relevant Job Description terminology when factually supported.
* Improve ATS keyword alignment.

Gemini must not:

* Invent skills.
* Invent experience.
* Invent projects.
* Invent employment.
* Invent education.
* Invent certifications.
* Invent achievements.
* Invent metrics.
* Invent responsibilities.
* Change dates.
* Change company names.
* Change institution names.
* Misrepresent the user's background.

The system prompt used for Gemini must explicitly enforce these constraints.

---

### 5.8 Structured Change Generation

Gemini must return proposed resume changes in structured JSON.

Each proposed change should contain:

* Unique Change ID.
* Change Type.
* Resume Section.
* Original Content.
* Proposed Content.
* Reason for Change.
* Related Job Description Requirements.
* Related Keywords.
* Confidence Level.

Supported Change Types may include:

* Rewrite.
* Reorder.
* Remove.
* Keyword Alignment.
* Emphasis.
* Formatting.

The application must validate Gemini's structured output before displaying or applying changes.

Invalid AI responses must never directly modify the generated resume.

---

### 5.9 Change Review Interface

The application must provide a dedicated interface for reviewing proposed changes.

Each change should display:

* Resume Section.
* Change Type.
* Original Content.
* Proposed Content.
* Reason for Change.
* Related Job Description requirement or keyword.
* Confidence Level.
* Accept button.
* Reject button.

The interface should visually distinguish additions, removals, and modifications.

Global controls:

* Accept All.
* Reject All.
* Reset Decisions.

No proposed change should be applied without an explicit acceptance decision.

---

### 5.10 Generated Resume Creation

After the user reviews the changes:

1. Create a copy of `master_resume.tex`.

2. Apply only accepted changes.

3. Validate that the master resume remains unchanged.

4. Generate the tailored LaTeX resume.

5. Save generated files separately from the master resume.

Recommended structure:

`/generated/<job-title>/<timestamp>/resume.tex`

`/generated/<job-title>/<timestamp>/resume.pdf`

Generated files should not be committed to GitHub by default.

---

### 5.11 LaTeX Validation and Compilation

The application must validate generated LaTeX before PDF generation.

Requirements:

* Detect invalid LaTeX syntax.
* Detect missing braces where possible.
* Detect broken environments.
* Detect missing packages.
* Display compilation errors clearly.
* Never modify the master resume during error recovery.

The application should use a locally installed LaTeX compiler.

Recommended compiler:

`latexmk`

Alternative:

`pdflatex`

Compilation should use appropriate security restrictions and timeouts because AI-generated LaTeX must be treated as untrusted input.

---

### 5.12 PDF Preview

After successful compilation, display the generated PDF inside the application.

Features:

* Embedded PDF preview.
* Refresh preview after recompilation.
* Display compilation status.
* Display compilation errors.
* Allow the user to return to the Change Review interface.

---

### 5.13 Final Resume Match Report

After applying accepted changes, calculate the Resume Match Score again.

Display:

* Before Score.
* After Score.
* Score Improvement.
* Newly Covered Requirements.
* Improved Keywords.
* Remaining Missing Requirements.
* Unsupported Requirements.
* Accepted Changes.
* Rejected Changes.

The application must not imply that a higher internal score guarantees passing an ATS or receiving an interview.

---

### 5.14 Export

The application must allow exporting:

* Tailored `.tex` file.
* Compiled `.pdf` file.

Filename format:

`<Name>_<Job_Title>_Resume.tex`

`<Name>_<Job_Title>_Resume.pdf`

Filenames must be sanitized before use.

---

## 6. User Interface Structure

### Screen 1: Session Setup

Components:

* Application title.
* Gemini API key input.
* Show/Hide Key.
* Validate Key.
* Clear Key.
* API key security message.

---

### Screen 2: Job Input

Components:

* Job Description textarea.
* Job Title optional input.
* Character count.
* Clear inputs.
* Analyze Job button.

---

### Screen 3: Job Analysis

Components:

* Detected Job Title.
* Company Name.
* Seniority Level.
* Required Skills.
* Preferred Skills.
* Technologies.
* Responsibilities.
* Important Keywords.
* Initial Resume Match Score.
* Matched Requirements.
* Missing Requirements.
* Generate Tailoring Suggestions button.

---

### Screen 4: Change Review

Components:

* List of proposed changes.
* Change category filters.
* Original vs. Proposed content.
* Reason for each change.
* Related Job Description requirements.
* Confidence level.
* Accept.
* Reject.
* Accept All.
* Reject All.
* Reset Decisions.
* Generate Resume button.

---

### Screen 5: Resume Preview

Components:

* LaTeX compilation status.
* Embedded PDF preview.
* Before Match Score.
* After Match Score.
* Remaining gaps.
* Accepted change count.
* Rejected change count.
* Return to Change Review.
* Export `.tex`.
* Export `.pdf`.

---

## 7. Technical Architecture

Recommended architecture:

### Frontend

* React.
* TypeScript.
* Vite.
* Tailwind CSS.

Responsibilities:

* API key session interface.
* Job Description input.
* Job Title input.
* Job analysis visualization.
* Change review interface.
* Accept/reject state management.
* PDF preview.
* Export controls.

### Backend

Recommended:

* Python.
* FastAPI.

Responsibilities:

* Load master LaTeX resume.
* Gemini API communication.
* Job Description analysis.
* Resume analysis.
* Structured change generation.
* AI response validation.
* Apply accepted changes.
* Resume scoring.
* LaTeX validation.
* LaTeX compilation.
* Generated file management.

---

## 8. Recommended Project Structure

```text
resume-tailoring-app/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   └── package.json
│
├── backend/
│   ├── api/
│   ├── services/
│   │   ├── gemini_service.py
│   │   ├── jd_analyzer.py
│   │   ├── resume_analyzer.py
│   │   ├── tailoring_service.py
│   │   ├── scoring_service.py
│   │   ├── latex_service.py
│   │   └── file_service.py
│   ├── models/
│   ├── schemas/
│   ├── prompts/
│   └── main.py
│
├── resume/
│   └── master_resume.tex
│
├── generated/
│
├── tests/
│
├── .gitignore
├── README.md
└── PRD.md
```

---

## 9. Security Requirements

* Gemini API key must never be persisted.
* Gemini API key must never appear in logs.
* Gemini API key must never appear in generated files.
* Gemini API key must never be committed to GitHub.
* Generated resumes should be ignored by Git.
* The master resume must never be modified by application logic.
* Validate all Gemini responses.
* Treat AI-generated LaTeX as untrusted input.
* Sanitize generated filenames.
* Restrict filesystem access.
* Use compilation timeouts.
* Restrict dangerous LaTeX shell execution.
* Never compile with unrestricted `--shell-escape`.
* Display safe error messages without exposing secrets.

---

## 10. Non-Functional Requirements

### Performance

* The interface should remain responsive during AI requests and LaTeX compilation.
* Display loading states for long-running operations.
* Prevent duplicate AI requests from repeated button clicks.

### Reliability

* Invalid Gemini responses must be handled gracefully.
* LaTeX compilation failures must not crash the application.
* The master resume must remain recoverable and unchanged.

### Usability

* The workflow should be understandable without technical knowledge.
* The user should always know the current stage of the tailoring process.
* AI-generated changes must be transparent and reversible.

### Maintainability

* Separate Gemini communication, resume analysis, scoring, LaTeX processing, and file management.
* Use typed schemas for API requests and responses.
* Keep prompts separate from application logic.
* Add automated tests for scoring, change application, filename sanitization, and master resume protection.

---

## 11. MVP Success Criteria

The MVP is successful when the user can:

1. Launch the application locally.

2. Enter and validate a Gemini API key.

3. Paste a Job Description.

4. Optionally enter a Job Title.

5. Analyze the Job Description.

6. View an initial Resume Match Score and gap analysis.

7. Generate truthful, structured resume tailoring suggestions.

8. Review every proposed change.

9. Accept or reject individual changes.

10. Generate a valid tailored LaTeX resume without modifying the master resume.

11. Compile the tailored resume into a PDF.

12. Preview the PDF.

13. View the before and after Resume Match Scores.

14. Export the `.tex` and `.pdf` files.

15. Close the application without the Gemini API key being persisted.

---

## 12. Future Enhancements

The following features are outside the MVP:

* Multiple master resume profiles.
* Resume version history.
* Job application tracking.
* Cover letter generation.
* Multiple AI provider support.
* Batch Job Description processing.
* Cloud synchronization.
* User accounts.
* Authentication.
* Hosted SaaS version.
* Interview question generation.
* LinkedIn profile tailoring.
* Historical match score analytics.
