# Task Management (Django + Ninja)

## Quickstart
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py demo_data
python manage.py test
python manage.py runserver

## Environment Variables
Copy `.env.example` to `.env` and adjust as needed:

| Variable | Description | Default |
| --- | --- | --- |
| DJANGO_SECRET_KEY / SECRET_KEY | Django secret key used for cryptographic signing. | dev-secret-key |
| DJANGO_DEBUG / DEBUG | Enable debug mode (`1` turns it on). | 1 |
| SQLITE_PATH | Path to the SQLite database file. | ./db.sqlite3 |
| ALLOW_ORG_OVERRIDE | Allow dev-only `org_id` query override. | 0 |

## Multi-Tenancy
Each `User` belongs to an `Organization`, and data is scoped to the current
organization via a context variable. Models such as `Task` use a custom manager
that automatically filters queries to the active tenant, preventing cross-org
data leaks.

## Test Credentials
`python manage.py demo_data` seeds two organizations with demo users:

| Organization | Username | Password |
| --- | --- | --- |
| OrgA | alice | 1234 |
| OrgB | bob   | 1234 |

## Deployment Notes
- Generate a strong `SECRET_KEY` and set `DEBUG=0` in production.
- Run migrations to initialize the SQLite database.
- Execute `python manage.py collectstatic` for static assets.
- Serve the app with a production-ready server such as `gunicorn` or `uvicorn`.
- A sample `render.yaml` is provided for deployment on Render.

## Time Tracking
Measure runtime of commands during development:

```
time python manage.py test
python manage.py test --timing
```

## Coverage
Install `coverage` and generate a report:

```
pip install coverage
coverage run manage.py test
coverage html  # open htmlcov/index.html
```

## Simulating Org Context

API requests normally infer the organization from the authenticated user or
the `org` claim in a JWT token. For tests or local development you can avoid
query string overrides by setting the organization context directly:

```python
from core.tenant import set_org

set_org(org.id)
# run code that queries org-scoped models
set_org(None)
```

The legacy `?org_id=` override is disabled by default. It can be re-enabled by
setting `ALLOW_ORG_OVERRIDE=1` in the environment when running development or
test code.

