# Habit Tracker App - Technical Execution Plan

Objective

- Build a cross-platform habit tracking application (web-first) with a REST API backend, React frontend, authentication, persistence, analytics (streaks, completions) and CI/deployment support.

High-level architecture

- Backend: Python + FastAPI, PostgreSQL (SQLite for dev), SQLAlchemy ORM, alembic for migrations, JWT authentication.
- Frontend: React (Vite or Create React App), TypeScript optional (start JS for MVP), React Router, simple responsive UI.
- Dev deployment: Docker + docker-compose; CI via GitHub Actions.

Data model (entities)

- User: id, email, password_hash, created_at
- Habit: id, user_id, title, description, schedule (daily/weekly/custom), active (bool), created_at
- HabitEntry: id, habit_id, date (ISO date), status (done/failed/skipped), note
- Tag (optional): id, user_id, name

Core features / API endpoints

- Auth
  - POST /api/auth/register -> register user (email, password)
  - POST /api/auth/login -> returns JWT
  - GET /api/auth/me -> get current user

- Habits
  - GET /api/habits -> list user's habits
  - POST /api/habits -> create habit
  - GET /api/habits/{id} -> get habit
  - PUT /api/habits/{id} -> update
  - DELETE /api/habits/{id} -> delete

- Habit Entries
  - GET /api/habits/{habit_id}/entries?start=&end= -> list entries
  - POST /api/habits/{habit_id}/entries -> create entry for date
  - PUT /api/habits/{habit_id}/entries/{entry_id} -> update entry

- Analytics
  - GET /api/habits/{habit_id}/stats -> streaks, completion % in range

Non-functional

- JWT auth with secure password hashing (bcrypt)
- Input validation with Pydantic schemas
- Unit tests for backend endpoints (pytest + httpx)
- Frontend component tests (jest + react-testing-library)
- Linting (flake8/ruff for Python, eslint + prettier for JS)

Files to create (branch: feat/habit-tracker-architecture)

Backend (Python/FastAPI)
- backend/Dockerfile - container for the backend service
- backend/pyproject.toml or requirements.txt - dependencies
- backend/app/__init__.py
- backend/app/main.py - FastAPI app, include routers
- backend/app/models.py - SQLAlchemy models: User, Habit, HabitEntry, Tag
- backend/app/schemas.py - Pydantic models for requests/responses
- backend/app/crud.py - DB CRUD operations
- backend/app/db.py - DB session setup
- backend/app/auth.py - JWT utilities and auth dependencies
- backend/app/routers/auth.py - auth endpoints
- backend/app/routers/habits.py - habit endpoints
- backend/app/routers/entries.py - habit entry endpoints
- backend/tests/test_auth.py - basic auth tests
- backend/tests/test_habits.py - habit endpoint tests

Frontend (React)
- frontend/Dockerfile
- frontend/package.json
- frontend/vite.config.js or CRA config
- frontend/src/main.jsx (or index.js)
- frontend/src/App.jsx - router + auth wrapper
- frontend/src/pages/Dashboard.jsx - overview with streaks
- frontend/src/pages/Habits.jsx - list/create/update habits
- frontend/src/components/HabitCard.jsx - display a habit and actions
- frontend/src/components/EntryPicker.jsx - mark today's completion
- frontend/src/services/api.js - API client with auth token handling

DevOps / CI / infra
- .github/workflows/ci.yml - run backend tests, lint, build frontend
- docker-compose.yml - compose for backend, frontend, db
- README.md - update with setup & run instructions

Optional (phase 2)
- websocket/notifications for real-time updates
- mobile: React Native or PWA

Milestones (sprints)

- Sprint 1 (3 days): Project scaffolding, backend models, auth, basic habits API (CRUD), SQLite dev DB.
- Sprint 2 (3 days): Habit entries API, stats endpoint, unit tests for backend, basic API docs (OpenAPI).
- Sprint 3 (3 days): Frontend scaffolding and pages for habits and entries, integrate auth, basic UI.
- Sprint 4 (2 days): Dockerize services, add CI workflow, polish, docs, handoff.

Acceptance criteria (MVP)

- User can register/login
- User can create/update/delete habits
- User can mark a habit as done for a date and view entries
- Basic streak/completion calculation endpoint exists
- Frontend allows the above flows and persists login token
- Tests exist for core backend behaviour and CI runs successfully

Testing & quality

- Backend: pytest + coverage; target >=80% for critical modules
- Frontend: smoke tests for main pages
- Linting: ruff/flake8 and eslint

Developer instructions (for Developer Agent)

1. Checkout branch feat/habit-tracker-architecture
2. Implement backend scaffolding under backend/ as listed above
3. Add database models, alembic migrations (optional), and run basic tests
4. Implement auth (JWT) and habit/entries routers
5. Create frontend app under frontend/ and wire auth and API client
6. Add dockerfiles and docker-compose for local dev
7. Add GitHub Actions CI workflow to run tests and build
8. Open PR for review

Files to be created/modified in this branch (exact paths)

- TODO.md (this file)
- README.md (update with setup notes)
- backend/Dockerfile
- backend/requirements.txt
- backend/app/__init__.py
- backend/app/main.py
- backend/app/models.py
- backend/app/schemas.py
- backend/app/crud.py
- backend/app/db.py
- backend/app/auth.py
- backend/app/routers/auth.py
- backend/app/routers/habits.py
- backend/app/routers/entries.py
- backend/tests/test_auth.py
- backend/tests/test_habits.py
- frontend/Dockerfile
- frontend/package.json
- frontend/vite.config.js
- frontend/src/main.jsx
- frontend/src/App.jsx
- frontend/src/pages/Dashboard.jsx
- frontend/src/pages/Habits.jsx
- frontend/src/components/HabitCard.jsx
- frontend/src/components/EntryPicker.jsx
- frontend/src/services/api.js
- .github/workflows/ci.yml
- docker-compose.yml

Notes / constraints

- Start with SQLite for speed; switch to PostgreSQL for production.
- Keep authentication simple (JWT) but provide hooks for OAuth later.
- Keep UI minimal and accessible; focus on core flows.

Ready state

- This branch contains the technical plan and file list. It's ready for the Developer Agent to implement the application according to the plan.
