---
id: 1
title: update-project-constitution
stage: constitution
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Hp
command: sp.constitution
labels: [constitution,spec-driven-development,todo-app]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
Project: Phase II – Spec-Driven Full-Stack Todo Web Application

🔹 Core Principles

Spec-Driven Development (Specs are the single source of truth)

Agentic Implementation (All code generated via Claude Code)

Deterministic Architecture (Frontend, Backend, Database clearly separated)

Security-First Design (JWT authentication enforced everywhere)

User Data Isolation (No user can access another user's data)

Reproducibility (Project can be cloned and run by others)

Minimal but Complete Feature Set (Only required features, fully correct)

🔹 Key Standards

All features must originate from a spec file

No direct manual coding of application logic

Every backend endpoint must:

Require authentication

Verify JWT

Enforce ownership checks

All frontend API calls must go through a single API client

Database access must only occur through SQLModel ORM

Folder structure must follow monorepo layout

Claude Code must be referenced with spec paths in prompts

🔹 Technology Lock (Non-Negotiable)

Frontend: Next.js (App Router) + TypeScript + Tailwind CSS

Backend: Python FastAPI

ORM: SQLModel

Database: Neon Serverless PostgreSQL

Authentication: Better Auth with JWT

Spec System: Spec-Kit Plus

AI Implementer: Claude Code

No alternative frameworks allowed.

🔹 Architectural Constraints

Frontend and backend must be separate services

Backend must expose REST API only

No frontend direct database access

Authentication occurs on frontend, verification on backend

JWT secret shared through environment variable

All routes prefixed with /api

🔹 Security Rules

All API routes require JWT

Tokens must be verified on every request

User ID extracted from token

URL user IDs must match token user ID

401 returned for missing or invalid tokens

403 returned for unauthorized resource access

🔹 Data Rules

Tasks must always include:

id

user_id

title

completed

Task queries must always filter by user_id

No global task queries allowed

🔹 Spec Rules

Specs must exist before implementation

Specs must describe:

User stories

Acceptance criteria

Validation rules

If behavior changes → update spec first

🔹 Development Workflow

Write or update spec

Ask Claude Code to read spec

Generate plan

Implement feature

Test

Iterate

Skipping steps is not allowed.

🔹 Testing Standards

Manual end-to-end testing required

Verify:

Signup

Login

Task CRUD

Token enforcement

User isolation

Broken features must be fixed before adding new ones

🔹 Documentation Requirements

README must explain:

Project purpose

Tech stack

Setup instructions

How auth works

CLAUDE.md must exist at:

Root

frontend/

backend/

🔹 Constraints

Phase II scope only:

Task CRUD

Authentication

No chatbot

No advanced AI features

No extra features beyond specs

🔹 Success Criteria

Application runs locally

Users can sign up and log in

Users only see their own tasks

Tasks persist in database

All requests require JWT

Repo follows monorepo structure

Specs exist and match implementation
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

You are updating the project constitution at `.specify/memory/constitution.md`. This file is a TEMPLATE containing placeholder tokens in square brackets (e.g. `[PROJECT_NAME]`, `[PRINCIPLE_1_NAME]`). Your job is to (a) collect/derive concrete values, (b) fill the template precisely, and (c) propagate any amendments across dependent artifacts.

Follow this execution flow:

1. Load the existing constitution template at `.specify/memory/constitution.md`.
   - Identify every placeholder token of the form `[ALL_CAPS_IDENTIFIER]`.
   **IMPORTANT**: The user might require less or more principles than the ones used in the template. If a number is specified, respect that - follow the general template. You will update the doc accordingly.

2. Collect/derive values for placeholders:
   - If user input (conversation) supplies a value, use it.
   - Otherwise infer from existing repo context (README, docs, prior constitution versions if embedded).
   - For governance dates: `RATIFICATION_DATE` is the original adoption date (if unknown ask or mark TODO), `LAST_AMENDED_DATE` is today if changes are made, otherwise keep previous.
   - `CONSTITUTION_VERSION` must increment according to semantic versioning rules:
     - MAJOR: Backward incompatible governance/principle removals or redefinitions.
     - MINOR: New principle/section added or materially expanded guidance.
     - PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
   - If version bump type ambiguous, propose reasoning before finalizing.

3. Draft the updated constitution content:
   - Replace every placeholder with concrete text (no bracketed tokens left except intentionally retained template slots that the project has chosen not to define yet—explicitly justify any left).
   - Preserve heading hierarchy and comments can be removed once replaced unless they still add clarifying guidance.
   - Ensure each Principle section: succinct name line, paragraph (or bullet list) capturing non‑negotiable rules, explicit rationale if not obvious.
   - Ensure Governance section lists amendment procedure, versioning policy, and compliance review expectations.

4. Consistency propagation checklist (convert prior checklist into active validations):
   - Read `.specify/templates/plan-template.md` and ensure any "Constitution Check" or rules align with updated principles.
   - Read `.specify/templates/spec-template.md` for scope/requirements alignment—update if constitution adds/removes mandatory sections or constraints.
   - Read `.specify/templates/tasks-template.md` and ensure task categorization reflects new or removed principle-driven task types (e.g., observability, versioning, testing discipline).
   - Read each command file in `.specify/templates/commands/*.md` (including this one) to verify no outdated references (agent-specific names like CLAUDE only) remain when generic guidance is required.
   - Read any runtime guidance docs (e.g., `README.md`, `docs/quickstart.md`, or agent-specific guidance files if present). Update references to principles changed.

5. Produce a Sync Impact Report (prepend as an HTML comment at top of the constitution file after update):
   - Version change: old → new
   - List of modified principles (old title → new title if renamed)
   - Added sections
   - Removed sections
   - Templates requiring updates (✅ updated / ⚠ pending) with file paths
   - Follow-up TODOs if any placeholders intentionally deferred.

6. Validation before final output:
   - No remaining unexplained bracket tokens.
   - Version line matches report.
   - Dates ISO format YYYY-MM-DD.
   - Principles are declarative, testable, and free of vague language ("should" → replace with MUST/SHOULD rationale where appropriate).

7. Write the completed constitution back to `.specify/memory/constitution.md` (overwrite).

8. Output a final summary to the user with:
   - New version and bump rationale.
   - Any files flagged for manual follow-up.
   - Suggested commit message (e.g., `docs: amend constitution to vX.Y.Z (principle additions + governance update)`).

Formatting & Style Requirements:

- Use Markdown headings exactly as in the template (do not demote/promote levels).
- Wrap long rationale lines to keep readability (<100 chars ideally) but do not hard enforce with awkward breaks.
- Keep a single blank line between sections.
- Avoid trailing whitespace.

If the user supplies partial updates (e.g., only one principle revision), still perform validation and version decision steps.

If critical info missing (e.g., ratification date truly unknown), insert `TODO(<FIELD_NAME>): explanation` and include in the Sync Impact Report under deferred items.

Do not create a new template; always operate on the existing `.specify/memory/constitution.md` file.

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.

## Response snapshot

<!-- SYNC IMPACT REPORT:
Version change: N/A → 1.0.0 (initial version)
Modified principles: None (new constitution)
Added sections: All sections (initial constitution)
Removed sections: None
Templates requiring updates: ⚠ pending - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->

# Phase II – Spec-Driven Full-Stack Todo Web Application Constitution

## Core Principles

### Spec-Driven Development
Specs are the single source of truth
<!-- Core principle: All features must originate from a spec file; Specs must exist before implementation; If behavior changes → update spec first -->

### Agentic Implementation
All code generated via Claude Code
<!-- Core principle: No direct manual coding of application logic; Claude Code must be referenced with spec paths in prompts -->

### Deterministic Architecture
Frontend, Backend, Database clearly separated
<!-- Core principle: Frontend and backend must be separate services; No frontend direct database access; Database access must only occur through SQLModel ORM -->

### Security-First Design
JWT authentication enforced everywhere
<!-- Core principle: All API routes require JWT; Tokens must be verified on every request; Authentication occurs on frontend, verification on backend -->

### User Data Isolation
No user can access another user's data
<!-- Core principle: User ID extracted from token; URL user IDs must match token user ID; 401 returned for missing or invalid tokens; 403 returned for unauthorized resource access -->

### Reproducibility
Project can be cloned and run by others
<!-- Core principle: Minimal but Complete Feature Set (Only required features, fully correct); Repo follows monorepo structure -->

## Key Standards
All features must originate from a spec file

Every backend endpoint must:
- Require authentication
- Verify JWT
- Enforce ownership checks

All frontend API calls must go through a single API client

Database access must only occur through SQLModel ORM

Folder structure must follow monorepo layout

Technology Lock (Non-Negotiable):
- Frontend: Next.js (App Router) + TypeScript + Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Spec System: Spec-Kit Plus
- AI Implementer: Claude Code

Architectural Constraints:
- Backend must expose REST API only
- JWT secret shared through environment variable
- All routes prefixed with /api

Data Rules:
- Tasks must always include: id, user_id, title, completed
- Task queries must always filter by user_id
- No global task queries allowed

## Development Workflow
Write or update spec → Ask Claude Code to read spec → Generate plan → Implement feature → Test → Iterate

Skipping steps is not allowed.

Testing Standards:
- Manual end-to-end testing required
- Verify: Signup, Login, Task CRUD, Token enforcement, User isolation
- Broken features must be fixed before adding new ones

Documentation Requirements:
- README must explain: Project purpose, Tech stack, Setup instructions, How auth works
- CLAUDE.md must exist at: Root, frontend/, backend/

Constraints:
- Phase II scope only: Task CRUD, Authentication
- No chatbot, No advanced AI features, No extra features beyond specs

## Governance
Spec Rules:
- Specs must describe: User stories, Acceptance criteria, Validation rules

Success Criteria:
- Application runs locally
- Users can sign up and log in
- Users only see their own tasks
- Tasks persist in database
- All requests require JWT

**Version**: 1.0.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-01-30

## Outcome

- ✅ Impact: Created initial project constitution document with core principles for the todo web application
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md with project-specific principles
- 🔁 Next prompts: Implement features following the established constitution
- 🧠 Reflection: The constitution establishes clear guidelines for spec-driven development, security-first design, and deterministic architecture

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing features according to the constitution