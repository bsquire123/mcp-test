Habit Tracker App — Technical Execution Plan

Overview

This document defines a pragmatic, incremental plan to create a cross-platform habit tracking application (web-first, mobile-compatible). It focuses on a maintainable architecture, clear APIs, test coverage, CI, and deployment. This is an architecture and implementation checklist for the Developer Agent to execute.

Goals

- Allow users to create and track habits with flexible schedules and recurrence.
- Track daily completions and show streaks, summaries and simple analytics.
- Support user accounts and secure authentication.
- Provide a clean REST+JSON API and a responsive web UI (React).
- Be deployable to cloud (Heroku/Render/Vercel) and use a managed database.

High-level architecture

- Backend: FastAPI (Python) with SQLAlchemy ORM, Alembic migrations.
- DB: PostgreSQL (development: Docker Compose / sqlite option for quick dev).
- Auth: JWT-based (access + refresh) plus password hashing (bcrypt / passlib).
- Frontend: React + TypeScript + Vite; component library (Chakra UI or Material UI).
- Mobile: optional later via React Native / Expo reusing API.
- Notifications / Reminders: schedule jobs (Celery + Redis or APScheduler for simple cron).
- Hosting: Backend on Render/Heroku, Frontend on Vercel, Postgres managed DB.

Core domain models

- User
  - id (UUID)
  - email (unique)
  - password_hash
  - name (optional)
  - created_at, updated_at

- Habit
  - id (UUID)
  - user_id (FK)
  - title
  - description (optional)
  - color (optional)
  - is_public (optional)
  - schedule: type (daily/weekly/custom), days_of_week (array), interval (every N days)
  - goal (e.g., target per period)
  - created_at, updated_at

- HabitEntry (a logged completion)
  - id (UUID)
  - habit_id (FK)
  - user_id (FK) (denormalized for queries)
  - date (ISO date) or timestamp
  - note (optional)
  - created_at

- Reminder (optional)
  - id (UUID)
  - habit_id
  - user_id
  - time_of_day
  - timezone
  - enabled

- Tag (optional) / HabitTag join

Key features / user flows

1. Sign up / sign in (email + password). Verify email optional.
2. CRUD habits with schedule and settings.
3. Track completions for a day (create/delete HabitEntry).
4. View habit list, weekly views, streaks, success rate.
5. Simple analytics: current streak, best streak, completion rate.
6. Reminders: local push or email reminders (deferred to v2).
7. Export data (CSV) and mobile support later.

API design (REST, base /api/v1)

Authentication
- POST /api/v1/auth/register -> register user
- POST /api/v1/auth/login -> returns access & refresh tokens
- POST /api/v1/auth/refresh -> exchange refresh token
- POST /api/v1/auth/logout

Habits
- GET /api/v1/habits -> list user's habits (with optional date window)
- POST /api/v1/habits -> create habit
- GET /api/v1/habits/{id} -> detail
- PUT /api/v1/habits/{id} -> update
- DELETE /api/v1/habits/{id} -> delete

Entries
- GET /api/v1/habits/{id}/entries?start=YYYY-MM-DD&end=YYYY-MM-DD -> list entries
- POST /api/v1/habits/{id}/entries -> create entry (mark completed for date)
- DELETE /api/v1/habits/{id}/entries/{entry_id} -> remove

Analytics
- GET /api/v1/habits/{id}/stats?from=&to= -> current streak, best streak, rate

Reminders (v2)
- CRUD endpoints to manage reminders

Non-functional concerns

- Security: secure password storage, JWT expiration, rate limiting, input validation.
- Data integrity: DB constraints, transactions for related ops.
- Observability: logging, error reporting (Sentry optional), health endpoints.
- Testing: unit tests for business logic, integration tests for API (pytest + httpx), e2e optional.
- CI: GitHub Actions to run linters, tests, build, and optionally deploy to staging.

Folder layout (suggested)

backend/
  app/
    main.py
    api/
      v1/
        auth.py
        habits.py
        entries.py
        stats.py
    core/
      config.py
      security.py
    db/
      base.py (SQLAlchemy Base)
      models.py
      schemas.py (Pydantic)
      crud.py
    services/
      analytics.py
      reminders.py
    migrations/ (alembic)
  tests/
  Dockerfile
  docker-compose.yml
  requirements.txt

frontend/
  web/
    src/
      App.tsx
      pages/
        Dashboard.tsx
        HabitDetail.tsx
        Login.tsx
        Signup.tsx
      components/
        HabitCard.tsx
        EntryToggle.tsx
    vite.config.ts
    package.json

mobile/ (optional)
  expo/...

Devops
- GitHub Actions workflows:
  - tests.yml -> run backend and frontend tests
  - lint.yml -> run black/isort/ruff for Python; eslint/prettier for TS
  - docker-build.yml -> build images

Data migration
- Alembic migration initial schema for users, habits, entries, reminders.

Milestones and tasks (sprint-style)

M1 — Project scaffolding (1 week)
- Create backend skeleton, package setup, Dockerfile.
- Create frontend skeleton (Vite + TS) with basic routes.
- Add GitHub Actions to run tests and linters.

M2 — Core auth + models (1 week)
- Implement User model, auth endpoints, JWT, and signup/login flows.
- Add DB integration + Alembic initial migration.

M3 — CRUD for habits + entries (1-2 weeks)
- Implement habits endpoints and data model.
- Implement entries endpoints and tracking logic.
- Add unit and integration tests.

M4 — UI (2 weeks)
- Build dashboard, habit list, detail page, entry toggles.
- Connect to backend (mock initially, then live API).

M5 — Analytics + reminders + polish (2 weeks)
- Implement streak calculations and stats endpoint.
- Add reminders (APScheduler initially) and UI.
- UX polish, mobile adjustments.

Tasks for Developer Agent (exact files to create / modify)

Create these top-level directories and files (initial commit tasks):

- backend/ (dir)
  - backend/app/main.py -> FastAPI app entrypoint (skeleton)
  - backend/app/api/v1/__init__.py
  - backend/app/api/v1/auth.py -> routes stub + docstrings
  - backend/app/api/v1/habits.py -> routes stub + docstrings
  - backend/app/api/v1/entries.py -> routes stub + docstrings
  - backend/app/core/config.py -> configuration settings skeleton
  - backend/app/core/security.py -> auth helpers skeleton (placeholders)
  - backend/app/db/base.py -> SQLAlchemy base and session factory skeleton
  - backend/app/db/models.py -> SQLAlchemy models skeleton (User/Habit/HabitEntry/Reminder)
  - backend/app/db/schemas.py -> Pydantic schemas skeleton
  - backend/app/db/crud.py -> CRUD function skeletons
  - backend/app/services/analytics.py -> service skeleton for streaks and stats
  - backend/app/services/reminders.py -> reminder scheduling skeleton
  - backend/requirements.txt
  - backend/Dockerfile
  - backend/docker-compose.yml (Postgres + optional Redis)
  - backend/ale mbic.ini and migrations/ (initial migration stub)
  - backend/tests/test_auth.py (skeleton)
  - backend/tests/test_habits.py (skeleton)

- frontend/web/ (dir)
  - frontend/web/package.json
  - frontend/web/vite.config.ts
  - frontend/web/src/main.tsx (app root)
  - frontend/web/src/App.tsx
  - frontend/web/src/pages/Dashboard.tsx (skeleton)
  - frontend/web/src/pages/HabitDetail.tsx (skeleton)
  - frontend/web/src/pages/Login.tsx (skeleton)
  - frontend/web/src/pages/Signup.tsx (skeleton)
  - frontend/web/src/components/HabitCard.tsx (skeleton)
  - frontend/web/src/components/EntryToggle.tsx (skeleton)
  - frontend/web/README.md (dev notes)

- infra/
  - .github/workflows/tests.yml -> CI for backend tests
  - .github/workflows/lint.yml -> linters

- README.md -> update to describe project and development quickstart
- TODO.md -> (this file) high-level plan and task list

Notes and implementation guidance

- Keep business logic in services/ and CRUD in db/crud.py to keep routes thin.
- Prefer UUID primary keys for portability; use Postgres uuid_generate_v4() or SQLAlchemy UUID types.
- Implement paginated endpoints for lists where appropriate.
- Use feature toggles for things like reminders and social features.

Acceptance criteria for first iteration (MVP)

- User can register and log in.
- User can create, update, delete habits.
- User can mark a habit as completed for a date and unmark it.
- UI shows a list of habits and a way to toggle completion for today.
- Basic tests and CI passing.

Estimated team responsibilities

- Backend developer: API, DB, auth, CI, tests (primary)
- Frontend developer: React UI, API integration, styling
- DevOps: CI, Docker, deployment pipelines (can be combined with backend)

Next steps for Developer Agent

1. Create the branch feature/habit-tracker-plan (done).
2. Add file skeletons listed above in that branch as empty files with TODO placeholders.
3. Open a draft PR from feature/habit-tracker-plan -> main and request review once skeletons are in place.

If you want, I can: 
- Create the skeleton files now on this branch (I will only add skeletons and TODOs, no implementation), or
- Only keep this plan here and wait for you to approve the approach.

End of plan.
