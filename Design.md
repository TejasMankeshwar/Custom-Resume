# DESIGN.md

## 1. Design Goal

The AI Resume Tailoring App should feel like a premium developer productivity tool.

The interface should be:

* Minimal.
* Modern.
* Clean.
* Fast.
* Focused.
* Professional.
* Desktop-first but fully responsive.
* Easy to understand without instructions.

The design should prioritize the resume tailoring workflow and avoid unnecessary visual complexity.

Use a refined SaaS/developer-tool aesthetic inspired by modern AI coding tools and productivity applications.

Do not copy any existing product directly.

---

# 2. Design Principles

## Keep the Interface Focused

Every screen should have one clear primary action.

Avoid dashboards filled with unrelated cards, metrics, navigation items, or features.

The application should guide the user naturally through:

```text
Setup → Job Input → Analysis → Review Changes → Resume Preview
```

---

## Use Progressive Disclosure

Do not show every feature at once.

Only display information relevant to the current stage.

Examples:

* Do not show Resume Match Analysis before a JD is analyzed.
* Do not show Change Review before suggestions are generated.
* Do not show PDF controls before a resume is generated.
* Do not show export controls before the corresponding file exists.

---

## Prioritize Readability

The app contains:

* Job descriptions.
* Resume content.
* AI explanations.
* Match analysis.
* LaTeX compilation errors.

Typography, spacing, and layout must make large amounts of text easy to scan.

Avoid excessive decorative elements.

---

## Preserve User Control

AI suggestions must feel like proposals, not automatic actions.

The design must clearly distinguish:

* Original content.
* Proposed content.
* Accepted changes.
* Rejected changes.
* Pending changes.

Users should always understand what the application is doing.

---

# 3. Visual Style

Use a clean dark interface.

The design should feel professional rather than futuristic.

Avoid:

* Neon effects.
* Heavy gradients.
* Excessive glow.
* Glassmorphism everywhere.
* Animated backgrounds.
* Large decorative illustrations.
* Excessive rounded cards.
* Oversized headings.
* Excessive icons.
* AI-generated visual clutter.

Use subtle borders, restrained shadows, strong typography, and spacing to create hierarchy.

---

# 4. Color System

Use neutral dark colors as the foundation.

Recommended semantic tokens:

```text
--background
--surface
--surface-elevated
--border
--border-strong

--text-primary
--text-secondary
--text-muted

--accent
--accent-hover

--success
--warning
--danger
--info
```

Recommended visual direction:

```text
Background: Near-black / charcoal
Surface: Slightly lighter charcoal
Elevated Surface: Dark gray
Borders: Subtle neutral gray

Primary Text: Soft white
Secondary Text: Light gray
Muted Text: Medium gray

Accent: Restrained blue or indigo
Success: Green
Warning: Amber
Danger: Red
```

Use semantic color tokens instead of hardcoded colors throughout components.

The accent color should be used sparingly for:

* Primary buttons.
* Active workflow stages.
* Selected controls.
* Important interactive elements.

Do not use the accent color for large backgrounds.

---

# 5. Typography

Use a clean sans-serif font.

Preferred:

```text
Inter
```

Fallback:

```text
system-ui
```

Use monospace typography for:

* Resume content comparisons.
* LaTeX errors.
* Technical IDs when displayed.
* Compiler output snippets.

Preferred monospace:

```text
JetBrains Mono
```

Fallback:

```text
ui-monospace
```

Typography hierarchy:

```text
Page Title: 28–32px

Section Title: 18–22px

Card Title: 15–17px

Body Text: 14–16px

Secondary Text: 13–14px

Metadata / Labels: 12–13px
```

Avoid excessively large typography.

---

# 6. Application Layout

Use a centered application shell.

Recommended maximum width:

```text
1400px
```

General structure:

```text
┌─────────────────────────────────────────────────────┐
│ Header                                              │
├─────────────────────────────────────────────────────┤
│ Workflow Progress                                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│ Main Content                                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

Use generous but controlled spacing.

Recommended desktop page padding:

```text
24px – 32px
```

Recommended mobile page padding:

```text
16px
```

---

# 7. Header

Keep the header simple.

Display:

* Product name.
* Current session status.
* API key status indicator.
* Optional Clear Session action.

Example:

```text
Resume Tailor                         ● Gemini Connected
```

Avoid:

* Sidebar navigation.
* Large logos.
* Multiple navigation links.
* User profile menus.
* Settings menus.

The workflow itself should be the primary navigation.

---

# 8. Workflow Progress Indicator

Display a compact step indicator near the top of the application.

Steps:

```text
1. Job Input

2. Analysis

3. Review Changes

4. Resume Preview
```

States:

* Completed.
* Active.
* Upcoming.

Users may navigate backward to completed stages when application state allows it.

Users must not skip required workflow stages.

On mobile, use a compact horizontal stepper or simplified progress indicator.

---

# 9. API Key Interface

The API key interface should be compact and should not dominate the application.

Display it as a setup panel before the main workflow becomes available.

Components:

```text
Gemini API Key

[••••••••••••••••••••••••••••]

[Show] [Validate Key]

Your API key is used only for the current session and is never stored.
```

States:

```text
Not Entered
Validating
Connected
Invalid
Request Failed
```

When validated successfully:

* Collapse the setup panel.
* Display a small Connected indicator in the header.
* Allow replacing or clearing the key.

Never display the full API key after validation.

---

# 10. Job Input Screen

This should be the simplest screen.

Desktop layout:

```text
┌─────────────────────────────────────────────────────┐
│ Tailor your resume                                  │
│ Paste the job description to analyze resume fit.    │
│                                                     │
│ Job Title (Optional)                                │
│ [ Software Engineer                              ]  │
│                                                     │
│ Job Description                                    │
│ ┌─────────────────────────────────────────────────┐ │
│ │                                                 │ │
│ │ Paste job description here...                  │ │
│ │                                                 │ │
│ │                                                 │ │
│ └─────────────────────────────────────────────────┘ │
│ 4,218 characters                         [Clear]    │
│                                                     │
│                                      [Analyze Job]  │
└─────────────────────────────────────────────────────┘
```

Job Description textarea should:

* Be large.
* Support comfortable long-form editing.
* Have a minimum desktop height of approximately 350px.
* Grow reasonably with viewport height.
* Show character count.
* Preserve pasted formatting where practical.

Primary action:

```text
Analyze Job
```

Disable it when:

* API key is invalid.
* Job Description is empty.
* Analysis is already running.

---

# 11. Loading States

Long-running AI operations should clearly communicate progress.

Do not use only a spinning loader.

Display a descriptive state.

Examples:

```text
Analyzing job requirements...
```

```text
Comparing the job description with your master resume...
```

```text
Generating tailoring suggestions...
```

Use:

* Small spinner.
* Status text.
* Optional elapsed time.

Do not display fake progress percentages.

---

# 12. Job Analysis Screen

Use a two-column desktop layout.

```text
┌───────────────────────────────┬───────────────────────────────┐
│ Job Analysis                  │ Resume Match                  │
│                               │                               │
│ Job Title                     │ Match Score                   │
│ Company                       │                               │
│ Seniority                     │            72                 │
│                               │           /100                │
│ Required Skills               │                               │
│ Preferred Skills              │ Matched Requirements          │
│ Technologies                  │ Missing Requirements          │
│ Keywords                      │ Unsupported Requirements      │
│ Responsibilities              │                               │
└───────────────────────────────┴───────────────────────────────┘
```

On mobile:

```text
Job Analysis
      ↓
Resume Match
```

---

# 13. Skills and Keywords

Display skills and keywords as compact tags.

Example:

```text
Python   FastAPI   React   TypeScript   AWS
```

Tag states:

```text
Matched
Missing
Unsupported
Preferred
```

Use color carefully.

Do not create a large rainbow of tag colors.

Use semantic states consistently.

---

# 14. Resume Match Score

The Match Score should be visually important but not dominate the page.

Recommended:

* Circular progress indicator.

or

* Large numeric score with compact progress bar.

Example:

```text
Resume Match

72 / 100

██████████████░░░░░

Internal resume-to-job alignment score.
Not an official ATS score.
```

Display score categories below:

```text
Required Skills       80%
Preferred Skills      60%
Keywords              75%
Experience            70%
Projects              85%
Education             100%
```

Avoid unnecessary charts.

---

# 15. Analysis Requirement Lists

Separate requirements into three clear groups.

## Matched

Requirements already supported by the master resume.

## Missing

Requirements that may be better represented or emphasized.

## Unsupported

Requirements not supported by the master resume and which must not be added.

Unsupported requirements should be clearly visible.

Example:

```text
Kubernetes

Not found in the master resume.
This skill will not be added automatically.
```

---

# 16. Generate Suggestions Action

Place one clear primary action after the user reviews the analysis.

```text
Generate Tailoring Suggestions
```

Display estimated purpose, not fake timing.

Example:

```text
Gemini will analyze your existing resume content and propose truthful changes.
```

---

# 17. Change Review Screen

This is the most important screen in the application.

Use a spacious layout.

Recommended structure:

```text
┌─────────────────────────────────────────────────────┐
│ Review Changes                                      │
│                                                     │
│ 12 Suggestions     7 Accepted     3 Rejected        │
│                                                     │
│ [All] [Rewrite] [Reorder] [Remove] [Keyword]        │
│                                                     │
│ [Accept All] [Reject All] [Reset Decisions]         │
│                                                     │
│ ┌─────────────────────────────────────────────────┐ │
│ │ REWRITE                        Experience       │ │
│ │                                                 │ │
│ │ Original                                        │ │
│ │ Built a web application using React.            │ │
│ │                                                 │ │
│ │ Proposed                                        │ │
│ │ Developed a React application focused on...     │ │
│ │                                                 │ │
│ │ Why this change                                 │ │
│ │ Better aligns with the frontend development     │ │
│ │ responsibilities described in the JD.           │ │
│ │                                                 │ │
│ │ Keywords: React, Frontend Development            │ │
│ │ Confidence: High                                │ │
│ │                                                 │ │
│ │                          [Reject] [Accept]       │ │
│ └─────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

---

# 18. Change Cards

Each change should be displayed in its own card.

Display:

* Change Type.
* Resume Section.
* Original Content.
* Proposed Content.
* Reason.
* Related requirements.
* Keywords.
* Confidence.
* Decision controls.

Card states:

```text
Pending
Accepted
Rejected
```

Accepted cards should have a subtle success indicator.

Rejected cards should become visually muted.

Pending cards should remain neutral.

Avoid filling the entire card background with bright semantic colors.

---

# 19. Diff Visualization

Clearly distinguish removed and added text.

Recommended:

```text
Original

- Built a machine learning application.

Proposed

+ Developed and evaluated a machine learning application...
```

Use:

* Subtle red background for removed text.
* Subtle green background for added text.
* Monospace typography where helpful.

Do not build a complex code-editor-style diff system for the MVP.

A clear line or word-level visual difference is sufficient.

---

# 20. Change Review Controls

Global controls:

```text
Accept All
Reject All
Reset Decisions
```

Individual controls:

```text
Accept
Reject
```

Primary resume generation action:

```text
Generate Resume
```

Display decision progress:

```text
9 of 12 changes reviewed
```

Disable Generate Resume until every change has an explicit decision.

Keep the Generate Resume action visible near the bottom of the screen.

A sticky action bar may be used on long change lists.

---

# 21. Compilation State

After resume generation, clearly communicate compilation status.

States:

```text
Preparing Resume

Compiling LaTeX

Compilation Successful

Compilation Failed
```

On failure:

Display:

* Short explanation.
* Safe compiler error.
* Return to Change Review button.

Do not display raw compiler logs by default.

---

# 22. Resume Preview Screen

Desktop layout:

```text
┌───────────────────────┬─────────────────────────────┐
│ Final Match Report    │ PDF Preview                 │
│                       │                             │
│ Before       After    │                             │
│   72    →      86     │                             │
│                       │                             │
│ +14 Improvement       │                             │
│                       │                             │
│ Newly Covered         │                             │
│ Remaining Gaps        │                             │
│ Unsupported           │                             │
│                       │                             │
│ 9 Accepted            │                             │
│ 3 Rejected            │                             │
│                       │                             │
│ [Export TEX]          │                             │
│ [Export PDF]          │                             │
└───────────────────────┴─────────────────────────────┘
```

Recommended desktop proportions:

```text
Report: 35–40%

PDF Preview: 60–65%
```

On mobile:

```text
Final Match Report
        ↓
Export Controls
        ↓
PDF Preview
```

---

# 23. Before and After Score

Make the improvement immediately understandable.

Example:

```text
Resume Match

72  →  86

+14 points
```

Do not use celebratory effects or confetti.

The application should remain professional.

Always display:

```text
Internal resume-to-job alignment score.
Not an official ATS score.
```

---

# 24. PDF Preview

Use the browser's native PDF viewer when practical.

Requirements:

* Fill available vertical space.
* Minimum desktop height around 700px.
* Clear loading state.
* Clear failure state.
* Refresh after recompilation.

Do not add a large PDF library unless browser-native preview proves insufficient.

---

# 25. Buttons

Button hierarchy:

## Primary

Use for:

* Validate Key.
* Analyze Job.
* Generate Tailoring Suggestions.
* Generate Resume.
* Export PDF.

## Secondary

Use for:

* Export TEX.
* Return to Change Review.
* Reset Decisions.

## Destructive / Negative

Use for:

* Reject.
* Reject All.
* Clear Session.

Do not use multiple primary buttons in the same action group.

---

# 26. Form Inputs

All inputs must have:

* Visible labels.
* Clear focus states.
* Error states.
* Disabled states.
* Sufficient contrast.

Do not rely only on placeholder text as labels.

Recommended border radius:

```text
6px – 10px
```

Avoid excessive pill-shaped inputs.

---

# 27. Cards and Surfaces

Use cards only to group meaningful content.

Recommended:

```text
Border: 1px subtle neutral border

Border Radius: 8px – 12px

Shadow: None or extremely subtle

Padding: 16px – 24px
```

Avoid placing every element inside a card.

Avoid deeply nested cards.

---

# 28. Icons

Use icons only when they improve comprehension.

If an icon library is required, use:

```text
lucide-react
```

Use icons for:

* Show/Hide API Key.
* Success.
* Warning.
* Error.
* Export.
* Refresh.
* Clear.

Do not use decorative icons next to every heading.

---

# 29. Animations

Animations should be subtle and functional.

Allowed:

* Button state transitions.
* Panel expansion/collapse.
* Screen transitions.
* Loading indicators.
* Accepted/rejected card state transitions.
* Score number transitions.

Recommended duration:

```text
150ms – 250ms
```

Avoid:

* Scroll hijacking.
* Parallax.
* Large entrance animations.
* Bouncing elements.
* Continuous background animation.
* Excessive spring animations.

Do not add an animation library unless CSS transitions are insufficient.

---

# 30. Responsive Design

The application must work on:

```text
Desktop
Laptop
Tablet
Mobile
```

Desktop is the primary experience.

Responsive rules:

* Two-column layouts collapse into one column.
* PDF preview moves below final analysis.
* Change cards remain readable.
* Textareas remain comfortable to use.
* Buttons must not overflow.
* Long skills and keywords must wrap.
* Long Job Descriptions must not create horizontal scrolling.
* Sticky action bars must not cover content.
* Workflow indicator should simplify on small screens.

Minimum supported width:

```text
320px
```

No horizontal page overflow should occur.

---

# 31. Accessibility

Requirements:

* Semantic HTML.
* Keyboard-accessible controls.
* Visible focus states.
* Sufficient contrast.
* Form labels.
* Accessible error messages.
* Buttons must use actual `<button>` elements.
* Inputs must use proper labels.
* Status changes should be understandable without relying only on color.

Do not sacrifice accessibility for visual appearance.

---

# 32. Error States

Errors should be displayed near the relevant operation.

Examples:

```text
We couldn't validate this Gemini API key.
Check the key and try again.
```

```text
Gemini returned an invalid response.
Try generating suggestions again.
```

```text
The tailored resume could not be compiled.
Review the proposed changes and try again.
```

Do not display:

* Raw stack traces.
* Raw Gemini responses.
* API keys.
* Internal filesystem paths.
* Full compiler logs.

---

# 33. Empty States

Provide clear empty states.

Examples:

Before JD analysis:

```text
Paste a job description to analyze how well your resume matches the role.
```

Before suggestions:

```text
Generate tailoring suggestions to review potential resume improvements.
```

Before PDF generation:

```text
Review all proposed changes before generating your tailored resume.
```

Keep empty states concise.

---

# 34. Design Consistency Rules

Always:

* Use design tokens.
* Use consistent spacing.
* Use consistent border radius.
* Use consistent button hierarchy.
* Use consistent status colors.
* Use consistent error presentation.
* Use reusable UI components.

Do not:

* Hardcode random colors.
* Introduce one-off spacing values repeatedly.
* Create multiple versions of the same button.
* Use different visual patterns for identical actions.
* Mix unrelated design styles.

---

# 35. Stuff to Avoid

Avoid:

* Dashboard-style sidebar navigation.
* Large hero sections.
* Marketing pages inside the application.
* Excessive gradients.
* Neon AI aesthetics.
* Glassmorphism everywhere.
* Excessive shadows.
* Excessive rounded cards.
* Oversized typography.
* Decorative charts.
* Fake progress percentages.
* Confetti.
* Gamification.
* Chat-style AI interfaces.
* Floating AI assistant buttons.
* Complex settings pages.
* Modals for primary workflow steps.
* Horizontal scrolling.
* Unnecessary animation libraries.
* Unnecessary component libraries.
* Rebuilding browser-native PDF functionality without need.
* Displaying technical IDs unless required for debugging.
* Exposing raw AI output.
* Exposing raw compiler output.
* Hiding unsupported requirements to make the Match Score appear better.

---

# 36. Final Design Rule

The interface should make the following workflow immediately obvious:

```text
Enter Gemini API Key
        ↓
Paste Job Description
        ↓
Analyze Resume Fit
        ↓
Generate Suggestions
        ↓
Review Every Change
        ↓
Accept or Reject
        ↓
Generate Resume
        ↓
Preview PDF
        ↓
Export
```

When choosing between a more visually impressive design and a simpler design that makes the workflow clearer, choose the simpler design.

The final application should feel like a focused professional tool for carefully tailoring a resume, not a generic AI dashboard.
