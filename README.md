# University Facility Management System

A Django-based facility management and complaint tracking platform for Lagos State University of Science and Technology.

## Overview

The system centralizes university facility requests so students, staff, maintenance teams, and administrators can work from one place. It includes public information pages, role-based authentication, complaint workflows, notifications, reports, and management dashboards.

## Key Features

- Public landing pages with responsive navigation and shared site branding
- User registration, login, profile management, and password change
- Email-or-username authentication
- Role-based dashboards for admin, maintenance staff, and general staff
- Complaint submission with category, department, priority, details, and attachments
- Complaint assignment, comments, status updates, and closure flow
- In-app notifications and email notification hooks
- Admin tools for managing users, departments, and complaint categories
- Reports and summary views for complaint activity
- MySQL-backed runtime with a SQLite fallback for tests or local development when explicitly enabled

## Technology Stack

- Python 3.14
- Django 5.2
- MySQL 9.x
- `mysqlclient`
- `python-dotenv`
- Pillow

## Prerequisites

- Python installed and available on your PATH
- MySQL Server running locally
- MySQL Workbench installed if you want a GUI client
- A browser for running the application locally

## Project Setup

1. Open the project folder.
2. Create and activate a virtual environment.
3. Install dependencies:

	```bash
	pip install -r requirements.txt
	```

4. Copy `.env.example` to `.env`.
5. Set the MySQL values in `.env`.
6. Create the database `university_facility_management` in MySQL.
7. Run migrations.
8. Create a superuser.
9. Start the development server.

## Environment Variables

The project loads environment variables from `.env` at the repository root.

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DJANGO_FORCE_SQLITE=False
MYSQL_DATABASE=university_facility_management
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=localhost
EMAIL_PORT=1025
EMAIL_USE_TLS=False
DEFAULT_FROM_EMAIL=noreply@lasustech.edu.ng
```

Notes:

- Leave `DJANGO_FORCE_SQLITE=False` for normal MySQL-backed development.
- Set `DJANGO_FORCE_SQLITE=True` only if you want the app to use the local SQLite test database.
- The default email backend prints messages to the console.

## Database Setup

Create a MySQL schema named `university_facility_management`.

Example using the MySQL client:

```bash
mysql -u root -p
CREATE DATABASE university_facility_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

If you prefer MySQL Workbench, create the same schema there and ensure it matches the host, port, username, and password in `.env`.

## Run the Project

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

Then open:

- `http://127.0.0.1:8000/` for the public site
- `http://127.0.0.1:8000/admin/` for Django admin

## Testing

Run the main app test suite with:

```bash
python manage.py test accounts complaints notifications dashboard reports -v 1
```

## Default Roles

The application supports these user roles:

- Admin
- Maintenance Staff
- Staff
- Lecturer

Admins can manage users, departments, categories, complaints, and reports. Staff users can register, submit complaints, and track their requests. Maintenance users receive assigned complaints and update status.

## Notes

- The site uses a shared base template for navigation, branding, and layout.
- The logo and favicon are based on the uploaded LASUSTECH asset in `static/images`.
- The UI is responsive and uses a mobile navigation toggle for smaller screens.
