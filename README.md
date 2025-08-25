# GolfClubStuds — Django Members Demo

This project was built as part of a technical interview task.
It demonstrates clean Django practices with production-readiness in mind.

---

## Features

- **Centralised models** in `core/` for scalability across multiple apps.
- **Members app**: list, detail, create, and toggle status (Current ↔ Ex-Member).
- **Authentication**: login/logout using Django’s built-in views.
- **HTMX** integration: toggle status without page reloads.
- **Crispy Forms (Bootstrap 5)** for clean form rendering.
- **Environment-based settings** via `django-environ` (`ENV` file).
- **Ready for production**: Postgres, SMTP, security headers, static/media split.

---

## Requirements

- Python 3.11+
- Django 5.x
- Packages:
  - `django-environ`
  - `django-crispy-forms`
  - `crispy-bootstrap5`
  - `django-htmx`

Install with:

```bash
pip install -r requirements.txt
```

---

## Setup (development)

1. Clone repository and create a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `ENV` file in project root:
   ```dotenv
   DEBUG=True
   SECRET_KEY=your-secret-key
   ALLOWED_HOSTS=127.0.0.1,localhost
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Start development server:
   ```bash
   python manage.py runserver
   ```
7. Visit:
   - Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - Members list: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Project structure

```text
golfclubstuds/
├── core/
│   ├── __init__.py
│   ├── asgi.py
│   ├── models.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── migrations/
│       └── 0001_initial.py
│
├── members/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── core/
│   │   └── base.html
│   ├── members/
│   │   ├── list.html
│   │   ├── detail.html
│   │   └── form.html
│   └── registration/
│       └── login.html
│
├── media/
├── static/
│
├── .gitignore
├── ENV
├── manage.py
├── requirements.txt
└── README.md
```

---

## Production notes

- Switch `DEBUG=False` and configure Postgres/SMTP in `ENV`.
- Run `python manage.py collectstatic` → deploy `STATIC_ROOT`.
- Serve static/media via CDN or reverse proxy (e.g. Nginx).
- Security headers are already included in `settings.py`.

---

## License

MIT — for interview/demo purposes.
