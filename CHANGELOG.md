# Changelog

## [Unreleased]
- (placeholder)
- Ensure all files end with a trailing newline for style consistency.

## [0.1.2] - 2025-08-24
### Added
- Recovery scaffold with CLI commands and tests.
- `.gitignore`, `requirements.txt`.

### Changed
- Pagination uses PageNumberPagination (django-ninja >= 1.4).

## [0.2.0] - 2025-08-25
### Added
- Multi-tenancy support:
  - Tenant-scoped manager (`Task.objects`) with fallback `all_objects`.
  - Middleware to set tenant context per request.
- JWT authentication:
  - Login endpoint (`/auth/login`) issuing signed tokens.
  - `/auth/me` endpoint returning current user/org.
  - Middleware support for Bearer tokens in API requests.
- API filtering:
  - Coercion of JSON query params (`metadata[sprint]=21`, `metadata[priority__gt]=2`).
- Test suite extended with:
  - Auth API tests (login success, invalid creds, unauthorized).
  - Multi-tenancy API tests (tasks scoped to org, metadata filters).

### Changed
- Unified error handling with `HttpError` (401 on invalid creds / unauthorized).

### Notes
- All 10 tests passing on SQLite backend.

## [0.3.0] - 2025-08-25
### Added
- **Multi-tenancy middleware** (`config/multitenancy.py`) with tenant context via JWT/session.
- **Tenant manager** with `Task.objects` scoped to current org; `all_objects` unscoped.
- **Task CRUD API**:
  - `POST /tasks/` create (with assigned_to validation).
  - `PUT /tasks/{id}/` update (scoped to org).
  - `DELETE /tasks/{id}/` delete (scoped to org).
- **Users API**:
  - `GET /users/` list users in same org.
  - `POST /users/` create user in current org.
- **Cursor pagination** (`tasks/pagination.py`) with rolling-window pattern.
- **Auth API**: `/auth/login`, `/auth/me` with JWT.
- **Tests**: coverage for models, commands, auth, tenancy, and org isolation.

### Changed
- `find_tasks` command switched to `Task.all_objects` to bypass tenant scoping.
- Schemas updated for input/output consistency.
