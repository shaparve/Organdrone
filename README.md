# OrganDrone

OrganDrone is a Django REST API for coordinating organ requests, hospital data, and drone-based deliveries.

## Features

- Custom user roles for administrators, hospitals, and drone operators
- Hospital and organ inventory records
- Organ requests with priority, matching, and delivery status tracking
- Drone assignment and live location records
- PostgreSQL support with an optional SQLite development database
- Authenticated Django REST Framework endpoints

## Tech stack

- Python
- Django
- Django REST Framework
- PostgreSQL or SQLite

## Setup

1. Clone the repository and enter the project directory.

2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

4. For local development with SQLite, set the database flag:

   ```powershell
   $env:USE_SQLITE = "1"
   ```

   Without this flag, the application uses PostgreSQL and reads its connection settings from `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, and `POSTGRES_PORT`.

5. Set a local Django secret key:

   ```powershell
   $env:DJANGO_SECRET_KEY = "replace-with-a-local-secret"
   ```

6. Apply migrations and run the checks:

   ```powershell
   py manage.py migrate
   py manage.py check
   ```

7. Start the development server:

   ```powershell
   py manage.py runserver
   ```

The API is available at `http://127.0.0.1:8000/api/` and the Django admin is available at `http://127.0.0.1:8000/admin/`.

## API routes

All API routes require authentication by default.

| Resource | Base route |
| --- | --- |
| Organ requests | `/api/organ-requests/` |
| Drones | `/api/drones/` |
| Drone locations | `/api/drone-locations/` |

Use the Django admin to create users, hospitals, organs, drones, and initial operational data.

## Testing

Run the test suite with:

```powershell
py manage.py test
```

## Project structure

```text
apps/accounts    Custom user model and role permissions
apps/hospitals   Hospital profiles and location data
apps/organs      Organ inventory and request workflows
apps/logistics   Drones, deliveries, and drone locations
config           Django project settings and URL configuration
```
