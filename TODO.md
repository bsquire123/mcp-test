# TODO: Habits App — Vue TypeScript frontend + Azure Functions (Python) backend

This document is the implementation plan for a Habits app with a Vue 3 + TypeScript frontend using PrimeVue components and a Python backend implemented as Azure Functions. Work will happen on the feature branch: feature/habits-app-vue-azure-python.

Goals
- Small, testable habits tracker with CRUD for habits and marking completions.
- Modern frontend (Vue 3 + TypeScript + Vite) using PrimeVue UI components.
- Serverless backend using Azure Functions (Python) exposing a REST API.
- Persist data in Azure Cosmos DB (Core (SQL) API) — local development with Azurite or Cosmos DB emulator.
- Well structured repo for iterative development and automated CI.

High-level architecture
- Frontend: SPA built with Vite + Vue 3 + TypeScript. Communicates with backend via REST -> JSON.
- Backend: Azure Functions (HTTP-triggered) written in Python. Functions implement REST endpoints for habits and habit entries (completions).
- Storage: Azure Cosmos DB (recommended) with two collections (habits, completions). Alternative: Azure Table Storage or SQLite for a quick PoC.
- Auth: initial implementation will not include auth (public API) for PoC. Later we can add Azure AD / EasyAuth or JWT-based auth.

API design (HTTP JSON)
- GET /api/habits -> list habits
- POST /api/habits -> create habit (body: {name, cadence, target, notes})
- GET /api/habits/{id} -> get habit
- PUT /api/habits/{id} -> update habit
- DELETE /api/habits/{id} -> delete habit
- POST /api/habits/{id}/completions -> create completion (body: {date})
- GET /api/habits/{id}/completions -> list completions for habit
- (Optional) GET /api/stats -> aggregated stats

Data model (suggested)
- Habit
  - id: string (GUID)
  - name: string
  - cadence: enum (daily, weekly, custom)
  - target: int (optional)
  - notes: string
  - created_at, updated_at
- Completion
  - id: string
  - habit_id: string
  - date: ISO-8601 date
  - created_at

Frontend: project structure and key files
Create a dedicated frontend folder using Vite + Vue 3 + TypeScript.
Files to create:
- frontend/package.json -> project manifests, scripts (dev, build, preview, lint, test)
- frontend/vite.config.ts -> Vite config
- frontend/tsconfig.json -> TS configuration
- frontend/src/main.ts -> Vue app bootstrap (PrimeVue init)
- frontend/src/App.vue -> App shell with RouterView
- frontend/src/router/index.ts -> Vue Router (routes: /, /habits/:id, /settings)
- frontend/src/store/ (Pinia)
  - frontend/src/store/index.ts -> Pinia setup
  - frontend/src/store/habits.ts -> habits store (calls API)
- frontend/src/services/api.ts -> wrapper for fetch/axios with baseUrl and helpers
- frontend/src/views/HabitList.vue -> list habits UI
- frontend/src/views/HabitDetail.vue -> view/edit habit, completions list, mark complete
- frontend/src/components/HabitForm.vue -> create/edit habit form
- frontend/src/components/CompletionList.vue -> list of completions, mark/unmark
- frontend/src/components/Header.vue -> app header/navigation
- frontend/src/assets/ -> icons/styles
- frontend/.eslintrc.cjs -> linting rules
- frontend/.prettierrc -> formatting

Frontend dependencies (examples)
- vue, vue-router, pinia
- primevue, primeicons, primeflex
- axios
- vite, typescript, @vitejs/plugin-vue
- eslint + @typescript-eslint plugin + vue plugin

Backend: project structure and key files
Create an Azure Functions Python project in backend/functions/.
Files to create:
- backend/host.json -> Azure Functions host config
- backend/local.settings.json (gitignored) -> local settings (Azure cosmos connection string, FUNCTIONS_WORKER_RUNTIME=python)
- backend/requirements.txt -> Python dependencies (azure-functions, azure-cosmos, python-dotenv (optional), pydantic)
- backend/functions/__init__.py (package init)
- backend/functions/habits/__init__.py -> HTTP-triggered functions index for /api/habits
- backend/functions/habits/function.json -> function bindings for list/create
- backend/functions/habit_item/__init__.py -> HTTP functions for GET/PUT/DELETE /api/habits/{id}
- backend/functions/completions/__init__.py -> POST and GET for completions
- backend/functions/shared/cosmos_client.py -> helper to create Cosmos client, encapsulate connection + helper methods
- backend/functions/shared/models.py -> Pydantic models for Habit and Completion (validation)
- backend/.funcignore -> ignore rules for Azure Functions deploy

Backend dependencies and local dev
- Use azure-functions Python worker and azure-cosmos library.
- Local dev: Azure Functions Core Tools (v4), Python 3.9+/3.10, Azurite or Cosmos DB emulator recommended.
- local.settings.json (NOT checked into git) will hold connection strings.

Infrastructure & IaC (optional initial steps)
- Add an ARM / Bicep / Terraform plan folder later to provision:
  - Azure Function App (Linux, Python)
  - Cosmos DB account + database + containers
  - Application Settings (COSMOS_CONN_STRING, FUNCTIONS_WORKER_RUNTIME, etc.)

Testing
- Frontend: unit tests with Vitest + @vue/test-utils for components; e2e tests with Playwright (optional).
- Backend: unit tests with pytest for helper functions and local integration tests using emulator/mocks.

CI/CD
- Add GitHub Actions workflows after PoC for:
  - Frontend lint & tests & build (on push to main)
  - Backend lint & tests
  - CD: deploy Functions (via Azure/functions-action) and static frontend to Azure Static Web Apps or Azure Storage + CDN.

Security & env
- Do not commit secrets. Use GitHub secrets / Azure Key Vault.
- local.settings.json should be added to .gitignore.

Files to create/modify (exact list)
- Create branch: feature/habits-app-vue-azure-python (already created)

Root-level changes
- TODO.md (this file) — create/modify (created on branch)
- .gitignore — add entries for frontend/node_modules, backend/.venv, backend/local.settings.json, frontend/dist

Frontend (create)
- frontend/package.json
- frontend/vite.config.ts
- frontend/tsconfig.json
- frontend/.eslintrc.cjs
- frontend/.prettierrc
- frontend/index.html (Vite entry)
- frontend/src/main.ts
- frontend/src/App.vue
- frontend/src/router/index.ts
- frontend/src/store/index.ts
- frontend/src/store/habits.ts
- frontend/src/services/api.ts
- frontend/src/views/HabitList.vue
- frontend/src/views/HabitDetail.vue
- frontend/src/components/HabitForm.vue
- frontend/src/components/CompletionList.vue
- frontend/src/components/Header.vue
- frontend/src/assets/ (folder)
- frontend/public/ (optional static assets)

Backend (create)
- backend/host.json
- backend/local.settings.json (will be gitignored; create a template local.settings.template.json)
- backend/requirements.txt
- backend/.funcignore
- backend/functions/__init__.py
- backend/functions/shared/__init__.py
- backend/functions/shared/cosmos_client.py
- backend/functions/shared/models.py
- backend/functions/habits/__init__.py
- backend/functions/habits/function.json
- backend/functions/habit_item/__init__.py
- backend/functions/habit_item/function.json
- backend/functions/completions/__init__.py
- backend/functions/completions/function.json

Dev tasks and sequence (high level)
1. Scaffold frontend with Vite + Vue 3 + TypeScript; wire PrimeVue and a simple Home/HabitList page that calls a mock API service.
2. Scaffold backend Azure Functions Python project; implement simple in-memory storage endpoints so frontend can be integrated quickly.
3. Implement Cosmos DB client and replace in-memory storage with Cosmos calls; add local.settings.json template and instructions to run emulator/Azurite.
4. Add linting, unit tests for both sides.
5. Add CI workflows for building, linting and tests.
6. Prepare deployment instructions (Azure CLI commands or GitHub Actions). Optionally add Terraform/Bicep for infra.

Local dev commands (examples)
- Frontend
  - npm install
  - npm run dev
  - npm run build
- Backend
  - cd backend
  - python -m venv .venv && source .venv/bin/activate
  - pip install -r requirements.txt
  - func start

Acceptance criteria (PoC)
- Running frontend dev server shows habit list UI.
- Backend Functions are reachable locally and return JSON for GET /api/habits.
- Frontend can create and list habits through the backend (initially in-memory, later persisted in Cosmos).

Notes & assumptions
- This initial plan intentionally omits authentication and multi-tenant concerns; we can add auth in a subsequent iteration.
- Cosmos DB is recommended for scalability; SQLite or file-based JSON can be used for a quick prototype.

Next step for Developer Agent
- Implement the scaffolding listed above in the feature branch. Create the files enumerated under "Files to create/modify" with basic stubs (no production code) and wire a minimal in-memory backend to enable frontend end-to-end development.

Plan ready for Developer Agent to implement. Target branch: feature/habits-app-vue-azure-python

