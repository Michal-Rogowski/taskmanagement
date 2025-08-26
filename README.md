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
| SECRET_KEY | Django secret key used for cryptographic signing. | dev-secret-key |
| DEBUG | Enable debug mode (`1` turns it on). | 1 |
| DB_ENGINE | Database backend (`sqlite` or `postgres`). | sqlite |
| DB_NAME | Postgres database name when using `postgres`. | multitenant |
| DB_USER | Postgres user when using `postgres`. | postgres |
| DB_PASSWORD | Postgres user's password. | password |
| DB_HOST | Postgres host. | localhost |
| DB_PORT | Postgres port. | 5432 |

## Sample Credentials
`python manage.py demo_data` creates an organization and a demo user:

- username: `alice`
- password: `1234`

