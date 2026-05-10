# University Facility Management System

A Django-based facility management and complaint tracking platform for Lagos State University of Science and Technology.

## Project Summary

This project provides a central web system for reporting and managing university facility issues. Instead of handling complaints through scattered messages, phone calls, or manual follow-ups, users can log everything in one place and track it from submission to resolution.

The application is designed for the real people who use a university facilities office:

- Students and staff submit complaints from the browser.
- Maintenance staff receive assigned complaints and update progress.
- Administrators manage users, departments, complaint categories, and reporting.
- The notification system keeps users informed as complaint status changes.

The result is a structured workflow that makes facility issues easier to see, assign, resolve, and audit.

## What The Website Does

The website is both a public information portal and an internal management system.

Public visitors can browse the homepage, About page, Contact page, Help page, FAQ page, and complaint tracking page.
Registered users can create complaints, monitor their own tickets, and receive updates.
Administrators can work from role-based dashboards, manage university data, and generate reports.

In practice, the site handles these jobs:

- user registration and login
- profile and password management
- complaint submission with attachments
- complaint assignment and status updates
- complaint tracking by ticket ID
- notifications for activity on a complaint
- reporting and CSV export for administrators
- management of departments, users, and complaint categories

## Who Uses The System

### Public visitors

These users do not need an account just to understand the system. They can read the public pages, learn how the platform works, and use the complaint tracking page to look up a ticket by ID.

### Students, staff, and lecturers

These users register through the browser and then use the complaint form to report faults, request maintenance, and follow the status of their complaints.

### Maintenance staff

Maintenance users see complaints that are assigned to them or complaints that are in active handling states. They update the complaint status as they work.

### Administrators

Administrators have the broadest access. They manage the data used by the platform, review complaints, assign maintenance work, close cases, and generate reports.

## Typical User Journey

1. A user opens the site and creates an account, or signs in with an existing one.
2. The user is routed to the correct dashboard based on role.
3. The user creates a complaint by choosing a department and category, adding a location, explaining the issue, setting priority, and attaching evidence if needed.
4. The complaint receives a ticket ID and is stored in the system.
5. An administrator reviews the complaint and assigns it to maintenance staff.
6. Maintenance staff update the ticket as the issue is being investigated or resolved.
7. The original user receives notifications and can check the live status from the dashboard or the complaint tracking page.
8. Once resolved, the administrator can close the complaint and the record remains available for reporting and audit purposes.

## Main Features

- Public landing pages with a shared branded layout
- Responsive navigation with a mobile menu
- User registration, login, profile editing, and password change
- Login with either username or email
- Role-based dashboards for admin, maintenance staff, staff, and lecturers
- Complaint submission with department, category, priority, location, description, and attachments
- Complaint tracking by ticket ID
- Complaint assignment, comments, status updates, and closure flow
- Active notification system with a live polling badge in the navbar
- Email notification hooks for selected actions
- Admin tools for users, departments, and complaint categories
- Complaint summaries and reports for operational oversight
- CSV export from the administrator report page
- MySQL-backed runtime with SQLite fallback when explicitly forced

## Core Pages

- Home: explains the platform and points users to the main actions
- About: gives a project overview
- Contact: provides contact information or support context
- Help: offers additional guidance for using the platform
- FAQ: answers common usage questions
- Complaint create page: submits a new facility issue
- Complaint track page: checks complaint status using a ticket ID
- Complaint list/detail pages: show complaint history and full complaint records for signed-in users
- Dashboard pages: provide role-specific workspaces for admins, maintenance staff, and regular users
- Categories page: lets administrators manage complaint categories
- Users page: lets administrators update user role and department
- Departments page: lets administrators maintain department records
- Notification page: shows alerts and history for the signed-in user
- Reports page: summarizes complaint activity and supports CSV export

## Roles And Permissions

- Admin: full management access to users, departments, complaint categories, complaints, and reports
- Maintenance Staff: view and update assigned complaints
- Staff: submit and track complaints
- Lecturer: submit and track complaints like other regular users

The system routes users to the correct dashboard based on their role after login.

## Complaint Workflow

The complaint form is deliberately guided so people do not have to guess what to enter.

Users provide:

- Department
- Category
- Location
- Description
- Priority
- Attachment, if needed

The department and category lists are populated from the database. The app also seeds default departments and complaint categories so the form is usable immediately after migrations.

Each complaint receives a unique ticket ID. That ticket ID is used throughout the system for tracking, assignment, notifications, and reporting.

### Complaint states

The complaint lifecycle follows these states:

- Pending
- Assigned
- In Progress
- Resolved
- Closed

## Notifications And Live Updates

The system includes in-app notifications for complaint activity. A badge in the top navigation polls a JSON endpoint at regular intervals and updates without a full page reload.

That means users get practical live feedback when:

- a complaint is submitted
- a complaint is assigned
- a complaint status changes
- a complaint is closed

This project currently uses polling rather than WebSockets because it is simpler, stable, and sufficient for the current scope.

## Reports And Administration

The administrator report page shows complaint summaries grouped by:

- status
- category
- department

Administrators can also filter the report by ticket ID, status, category, department, priority, and date range. The report view supports CSV export, which allows the data to be opened in spreadsheet tools or shared with management.

The report page also records generated report events in the database, so there is an audit trail of report activity.

## Technology Stack

- Python 3.14
- Django 5.2
- MySQL 9.x
- `mysqlclient`
- `python-dotenv`
- Pillow

## Project Structure

- `accounts/`: authentication, registration, profile management, and user roles
- `complaints/`: complaint submission, tracking, assignment, categories, and status updates
- `dashboard/`: role-based dashboards and admin management pages
- `notifications/`: in-app notifications and live polling endpoint
- `reports/`: complaint reporting and summaries
- `pages/`: public site pages such as home, about, contact, help, and FAQ
- `templates/`: shared and page-specific Django templates
- `static/`: CSS, JavaScript, branding assets, and favicon files
- `config/`: project settings and root URL configuration

## Design Notes

- The UI uses a shared base template for the entire site.
- The site branding uses the LASUSTECH logo asset stored in `static/images`.
- The favicon is a circular PNG for better browser compatibility.
- The layout is responsive and includes a mobile navigation toggle.
- The complaint form uses a guided layout so users can complete it step by step.

## Prerequisites

- Python installed and available on your PATH
- MySQL Server running locally
- MySQL Workbench if you want a GUI database client
- A modern browser for using the website locally

## Setup

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

If you prefer MySQL Workbench, create the same schema there and make sure it matches the host, port, username, and password in `.env`.

The project includes seed data for departments and complaint categories so the complaint form is usable immediately after migrations.

## Run The Project

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

Then open:

- `http://127.0.0.1:8000/` for the public site
- `http://127.0.0.1:8000/accounts/register/` to create a new account
- `http://127.0.0.1:8000/accounts/login/` to log in
- `http://127.0.0.1:8000/complaints/create/` to submit a complaint
- `http://127.0.0.1:8000/complaints/track/` to track a complaint by ticket ID
- `http://127.0.0.1:8000/dashboard/` for role-based dashboards
- `http://127.0.0.1:8000/notifications/` for the notification inbox
- `http://127.0.0.1:8000/reports/` for the summary report page
- `http://127.0.0.1:8000/admin/` for Django admin

## Testing

Run the main app test suite with:

```bash
python manage.py test accounts complaints notifications dashboard reports -v 1
```

You can also run a narrower test slice while working on a specific feature, for example:

```bash
python manage.py test complaints.tests.ComplaintTests -v 2
python manage.py test notifications.tests.NotificationTests -v 2
```

## Troubleshooting

- If the database does not connect, verify the MySQL service is running and the credentials in `.env` are correct.
- If login fails after registration or password change, check that the auth backend settings are intact.
- If the complaint dropdowns look empty, confirm the seed migration for departments and complaint categories has been applied.
- If the notification badge does not update, confirm the development server is running and the browser can reach `/notifications/live/`.
- If you switch between SQLite and MySQL, remember that the data lives in whichever database is currently active.

## Notes

- The application is intended as a university facility management portal, not just a generic ticket system.
- It is structured so that users see only the information and actions relevant to their role.
- MySQL Workbench is only a client interface; it shows data written by the Django app to the MySQL server.
