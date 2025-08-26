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
| SECRET_KEY | Django secret key used for cryptographic signing. | changeme |
| DEBUG | Enable debug mode (`1` turns it on). | 1 |
| DB_ENGINE | Database backend (`sqlite` or `postgres`). | sqlite |
| DB_NAME | Postgres database name when using `postgres`. | multitenant |
| DB_USER | Postgres user when using `postgres`. | postgres |
| DB_PASSWORD | Postgres user's password. | password |
| DB_HOST | Postgres host. | localhost |
| DB_PORT | Postgres port. | 5432 |

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
- Configure database credentials and run migrations.
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

