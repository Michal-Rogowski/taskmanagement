# Changelog

## [Unreleased]
- (placeholder)

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
