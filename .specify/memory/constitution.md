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