# Django Authentication System

A complete authentication system built with Django that includes user registration, login, and a dashboard with profile management.

## Features

- User registration with email
- User login and logout
- User dashboard with profile information
- Profile picture upload
- Profile information update
- Responsive design using Bootstrap 5
- Admin interface for user management

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd auth_system
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the application at `http://127.0.0.1:8000/`
2. Register a new account or login with existing credentials
3. Access the admin interface at `http://127.0.0.1:8000/admin/`

## Directory Structure

```
auth_system/
├── accounts/              # Main application
│   ├── migrations/       # Database migrations
│   ├── templates/       # HTML templates
│   ├── admin.py         # Admin interface configuration
│   ├── forms.py         # Form definitions
│   ├── models.py        # Data models
│   ├── urls.py          # URL routing
│   └── views.py         # View logic
├── auth_system/          # Project settings
├── media/               # User uploaded files
├── manage.py            # Django management script
├── requirements.txt     # Project dependencies
└── README.md           # This file
``` 