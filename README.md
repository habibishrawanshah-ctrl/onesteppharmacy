# OneStep Pharmacy

A modern Django-based pharmacy e-commerce platform for managing medicines, orders, and users. Customers can browse a product catalog, view medicine details (price, stock, expiry), place orders, and manage their accounts. Administrators manage everything through the Django admin dashboard.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0.5 (Python) |
| Database | SQLite (development) |
| Frontend | Server-side rendered Django templates |
| CSS | Custom responsive stylesheet |
| Image Handling | Django ImageField + Pillow |

## Features

- **Product Catalog** — Browse medicines with images, pricing, stock levels (color-coded badges), and expiry dates
- **User Authentication** — Sign up, log in, and log out with session-based auth
- **Order Placement** — Authenticated users can place orders with quantity selection (capped by stock)
- **Order Tracking** — Orders tracked by status: Pending, Shipped, Delivered
- **Admin Dashboard** — Full admin interface for managing products, orders, and user profiles
- **Responsive Design** — Mobile-friendly layout with breakpoints at 768px and 480px
- **Security** — CSRF protection, XSS filter, `X-Frame-Options: DENY`, HTTP-only cookies, SameSite=Lax

## Project Structure

```
pharmacy_ecommerce/                # Django project root
├── manage.py                      # Django CLI entry point
├── db.sqlite3                     # SQLite database
├── media/product_images/          # Uploaded product images
├── pharmacy_ecommerce/            # Project configuration
│   ├── settings.py                # Django settings (91 lines)
│   ├── urls.py                    # Root URL configuration
│   ├── views.py                   # Home, login, logout views
│   ├── wsgi.py                    # WSGI application
│   └── asgi.py                    # ASGI application (async support)
├── products/                      # Products app
│   ├── models.py                  # Product model (name, price, stock, expiry, image)
│   ├── views.py                   # Product list/detail views
│   ├── admin.py                   # Product admin config
│   ├── urls.py                    # Product routes
│   ├── templates/products/        # Product templates
│   └── static/css/styles.css      # Main stylesheet
├── orders/                        # Orders app
│   ├── models.py                  # Order model (user, product, quantity, status)
│   ├── views.py                   # Place order, success views
│   ├── forms.py                   # Order form
│   ├── admin.py                   # Order admin config
│   ├── urls.py                    # Order routes
│   └── templates/orders/          # Order templates
├── users/                         # Users app
│   ├── models.py                  # UserProfile (address, phone)
│   ├── views.py                   # Signup view
│   ├── admin.py                   # UserProfile admin config
│   ├── urls.py                    # User routes
│   └── templates/users/           # User templates
├── templates/                     # Project-level templates
│   ├── base.html                  # Main layout
│   └── home.html                  # Homepage with featured products
└── scripts/                       # Utility scripts
    ├── create_superuser.py        # Seed admin user
    ├── create_paracetamol.py      # Seed sample product
    ├── check_urls.py              # Test URL responses
    └── ... (17 helper scripts)
```

## Data Models

| Model | Key Fields | Description |
|-------|-----------|-------------|
| **Product** | `name`, `description`, `price`, `image`, `stock`, `expiry_date`, `created_at` | Medicine/product listing |
| **Order** | `user` (FK), `product` (FK), `quantity`, `order_date`, `status` | Customer order |
| **UserProfile** | `user` (OneToOne), `address`, `phone` | Extended user profile |

## Quick Start

```bash
# 1. Clone and enter the project
git clone <repo-url> onesteppharmacy
cd onesteppharmacy

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate          # Linux / macOS
# venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install django pillow

# 4. Run database migrations
cd pharmacy_ecommerce
python manage.py migrate

# 5. (Optional) Create a superuser for admin access
python manage.py createsuperuser

# 6. (Optional) Seed sample data
python scripts/create_paracetamol.py

# 7. Start the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** to access the application.

Admin dashboard: **http://127.0.0.1:8000/admin/**

## Routes

| URL | View | Auth Required |
|-----|------|--------------|
| `/` | Homepage | No |
| `/products/` | Product listing | No |
| `/products/<id>/` | Product detail | No |
| `/orders/place/<product_id>/` | Place order | Yes |
| `/orders/success/` | Order confirmation | No |
| `/users/signup/` | User registration | No |
| `/login/` | Login | No |
| `/logout/` | Logout | POST only |
| `/admin/` | Django admin | Staff |

## Available Commands

### Django management
```bash
python manage.py runserver        # Start dev server
python manage.py migrate          # Apply migrations
python manage.py makemigrations   # Create new migrations
python manage.py test             # Run tests
python manage.py createsuperuser  # Create admin user
python manage.py collectstatic    # Collect static files
```

### Utility scripts (from `pharmacy_ecommerce/`)
```bash
python scripts/create_superuser.py    # Seed hardcoded superuser
python scripts/create_paracetamol.py  # Seed sample product
python scripts/list_products.py       # List all products
python scripts/check_urls.py          # Verify URL responses
```

## Deployment Notes

- Set `DEBUG=False` in production
- Use a strong, randomized `SECRET_KEY` via environment variable
- Configure a production-grade database (PostgreSQL recommended)
- Serve static files via `python manage.py collectstatic`
- Use `gunicorn` + `nginx` or `daphne` for ASGI deployment
- Set `ALLOWED_HOSTS` to your domain(s)
- Configure media file serving for product images

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
