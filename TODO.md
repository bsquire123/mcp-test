# Implementation Plan: Full-stack Todo App

Goal: build a full-stack Todo application with a Vue 3 + TypeScript frontend and a Python Azure Functions backend using a MySQL database. This document defines the architecture, endpoints, development workflow, and exactly which files and directories the Developer Agent should create or modify.

High-level architecture
- Frontend: Vue 3 + TypeScript, Vite, single-page app that calls backend HTTP APIs.
- Backend: Azure Functions (Python) exposing REST endpoints for CRUD operations on todo tasks.
- Database: MySQL (Azure Database for MySQL or local MySQL for dev).
- CI/CD: GitHub Actions to build and (optionally) deploy frontend and backend to Azure.

API design
- GET  /api/tasks           -> list tasks
- GET  /api/tasks/{id}      -> get single task
- POST /api/tasks           -> create task (body: {title, completed, due_date?})
- PUT  /api/tasks/{id}      -> update task
- DELETE /api/tasks/{id}    -> delete task

Database schema (single table)
- tasks
  - id INT AUTO_INCREMENT PRIMARY KEY
  - title VARCHAR(255) NOT NULL
  - description TEXT NULL
  - completed TINYINT(1) DEFAULT 0
  - due_date DATETIME NULL
  - created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  - updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP

Local development
- Frontend: run `npm install` then `npm run dev` (Vite)
- Backend: use Azure Functions Core Tools (`func start`) with `local.settings.json` for configuration
- MySQL: run via Docker or Azure. Provide a docker-compose.yml for convenience.

Security & configuration
- Secrets (DB connection string, Azure credentials) stored in environment variables / local.settings.json (dev) and GitHub Secrets (CI/CD)
- CORS allowed origin configured in Azure Functions or infrastructure layer
- No auth initially; provide hooks to add JWT/OAuth later

Files and directories to create (exact paths)

1) Frontend (Vue 3 + TypeScript)
- /frontend/package.json
- /frontend/vite.config.ts
- /frontend/tsconfig.json
- /frontend/README.md
- /frontend/.gitignore
- /frontend/.env.example
- /frontend/index.html
- /frontend/src/main.ts
- /frontend/src/App.vue
- /frontend/src/components/TodoApp.vue
- /frontend/src/components/TodoItem.vue
- /frontend/src/services/api.ts      (axios wrapper to call backend)
- /frontend/src/types/todo.d.ts
- /frontend/src/assets/* (placeholder)
- /frontend/public/* (static files)
- /frontend/tests/* (Vitest config optional)
- /frontend/Dockerfile (optional)

2) Backend (Azure Functions - Python)
- /backend/host.json
- /backend/local.settings.json.example   (do NOT commit secrets)
- /backend/requirements.txt
- /backend/.python_packages (ignored)
- /backend/function_app.py   (optional shared helpers)
- /backend/__init__.py
- /backend/db/schema.sql     (create table script)
- /backend/db/migrate.py     (simple migration runner or note)

Azure Functions (HTTP-triggered functions)
- /backend/functions/tasks_list/function.json
- /backend/functions/tasks_list/__init__.py   (GET /api/tasks)
- /backend/functions/tasks_get/function.json
- /backend/functions/tasks_get/__init__.py    (GET /api/tasks/{id})
- /backend/functions/tasks_create/function.json
- /backend/functions/tasks_create/__init__.py (POST /api/tasks)
- /backend/functions/tasks_update/function.json
- /backend/functions/tasks_update/__init__.py (PUT /api/tasks/{id})
- /backend/functions/tasks_delete/function.json
- /backend/functions/tasks_delete/__init__.py (DELETE /api/tasks/{id})

Shared backend helpers
- /backend/shared/db.py        (connection pooling + helpers)
- /backend/shared/models.py    (Task model and serialization)
- /backend/shared/config.py    (reads env vars)

3) Infrastructure & Devops
- /.github/workflows/frontend-ci.yml   (install, build, test frontend)
- /.github/workflows/backend-ci.yml    (lint, test, package functions)
- /docker-compose.yml                  (MySQL + optional Adminer)
- /README.md  (update top-level readme to include setup instructions)

4) Tests & Linting
- /frontend/vitest.config.ts (optional)
- /backend/tests/test_tasks.py (pytest for function handlers)
- /backend/pyproject.toml or setup.cfg for linting

Implementation notes and conventions
- Use async DB calls where possible (aiomysql or PyMySQL with synchronous code if simpler).
- Keep business logic out of function handlers; handlers should parse request, call service layer, return HTTP response.
- Validate input and return appropriate 4xx/5xx codes.
- Use JSON for all request/response bodies.
- Use UTC timestamps for dates.

CI/CD and deployment notes
- Frontend can be deployed to Azure Static Web Apps or a storage static site. Build artifacts from `npm run build`.
- Backend should be deployed to Azure Function App for Python. Use Azure/login and azure/functions-action in GitHub Actions. Store publish credentials as secrets.
- Add workflow steps to run tests before deploy; require green tests for merge to main.

Developer Agent tasks (exact implementation tasks)
1. Create the files and folders listed above with placeholder content and TODO comments where implementation is required.
2. Add the DB schema file `/backend/db/schema.sql` containing the `CREATE TABLE tasks ...` statement.
3. Implement basic HTTP function templates with clear TODOs for connecting to DB and performing queries.
4. Add frontend scaffolding (Vite + Vue + TypeScript) with components that call the API endpoints; wire up axios base URL to `VITE_API_BASE_URL` env var.
5. Add docker-compose.yml to run a local MySQL instance for development.
6. Add GitHub Actions workflow files that run frontend build/tests and package backend artifacts.
7. Add clear README sections for how to run frontend, backend, and the database locally.

Notes for the Developer Agent
- Work on branch: feature/fullstack-vue-ts-azure-func-mysql
- Do NOT push secrets into the repo. Use `.example` files for configs and document environment variables.
- Keep initial implementation minimal but complete end-to-end: frontend can create/read/update/delete tasks against the backend using the local MySQL instance.

Once the Developer Agent has created the files above on the feature branch, notify me and I will review and provide next-step guidance.

End of plan.
