# OneStep Pharmacy

A modern Django-based pharmacy e-commerce platform for browsing medicines, managing a cart, placing orders, and tracking purchases. Customers can search products, view real-time stock and expiry details, add items to a cart, and complete checkout. Administrators manage products, orders, and users through the Django admin dashboard. Deployed on Vercel via a serverless ASGI wrapper.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 6.0.5 (Python) |
| Database | SQLite (development) / PostgreSQL (production) |
| Frontend | Server-side rendered Django templates |
| CSS | Custom responsive stylesheet with light/dark themes |
| Image Handling | Django ImageField + Pillow |
| Deployment | Vercel (serverless via ASGI + Whitenoise) |

## Features

- **Product Catalog** — Browse medicines with images, pricing, stock levels (color-coded badges), and expiry dates
- **Search** — Full-text search across product names and descriptions
- **Shopping Cart** — Add/update/remove items; persists in session; stock-validated at checkout
- **Checkout** — Create an order from cart contents with quantity and stock validation
- **User Authentication** — Sign up, log in, and log out with session-based auth
- **User Profiles** — View order history with status tracking (Pending, Shipped, Delivered)
- **Admin Dashboard** — Full admin interface for managing products, orders, and user profiles
- **Dark Mode** — Theme toggle persisted in localStorage
- **Responsive Design** — Mobile-friendly layout with hamburger menu and breakpoints at 768px and 480px
- **Informational Pages** — About, Help Center, Shipping Info, Returns, Contact, Privacy Policy, Terms of Service, License Info, Careers
- **Security** — CSRF protection, XSS filter, `X-Frame-Options: DENY`, HTTP-only cookies, SameSite=Lax, content-type nosniff

## Project Structure

```
onesteppharmacy/                    # Repository root
├── api/
│   ├── __init__.py
│   └── index.py                    # Vercel serverless ASGI entry point
├── pharmacy_ecommerce/             # Django project root
│   ├── manage.py                   # Django CLI entry point
│   ├── db.sqlite3                  # SQLite database (local dev, gitignored)
│   ├── requirements.txt            # Python dependencies
│   ├── media/product_images/       # Uploaded product images
│   ├── pharmacy_ecommerce/         # Project configuration
│   │   ├── settings.py             # Django settings
│   │   ├── urls.py                 # Root URL configuration
│   │   ├── views.py                # Home, login, logout, about, page views
│   │   ├── wsgi.py                 # WSGI application
│   │   └── asgi.py                 # ASGI application (async support)
│   ├── products/                   # Products app
│   │   ├── models.py               # Product model
│   │   ├── views.py                # Product list/detail/search views
│   │   ├── admin.py                # Product admin config
│   │   ├── urls.py                 # Product routes
│   │   └── templates/products/     # Product templates
│   ├── orders/                     # Orders app
│   │   ├── models.py               # Order model
│   │   ├── views.py                # Cart, checkout, place order views
│   │   ├── forms.py                # Order forms
│   │   ├── admin.py                # Order admin config
│   │   ├── urls.py                 # Order routes
│   │   └── templates/orders/       # Order templates (cart, checkout)
│   ├── users/                      # Users app
│   │   ├── models.py               # UserProfile model
│   │   ├── views.py                # Signup, profile views
│   │   ├── admin.py                # UserProfile admin config
│   │   ├── urls.py                 # User routes
│   │   └── templates/users/        # User templates (login, logout, signup, profile)
│   ├── templates/                  # Project-level templates
│   │   ├── base.html               # Main layout (header, footer, nav, theme toggle)
│   │   ├── home.html               # Homepage with hero, categories, featured products
│   │   ├── about.html              # About page
│   │   └── pages/                  # Static informational pages
│   │       ├── careers.html
│   │       ├── contact_us.html
│   │       ├── help_center.html
│   │       ├── license_info.html
│   │       ├── privacy_policy.html
│   │       ├── returns.html
│   │       ├── shipping_info.html
│   │       └── terms_of_service.html
│   ├── scripts/                    # Utility scripts (20 helpers)
│   │   ├── vercel-build.sh         # Vercel build script
│   │   ├── create_superuser.py     # Seed admin user
│   │   ├── seed_prod.py            # Seed full production data (6 users, 10 products, 10 orders)
│   │   ├── seed_products.py        # Seed sample products
│   │   ├── create_paracetamol.py   # Seed single product
│   │   ├── delete_products.py      # Delete all products
│   │   ├── list_products.py        # List all products
│   │   ├── check_urls.py           # Verify URL responses
│   │   ├── acceptance_test.py      # Run acceptance criteria tests
│   │   ├── fetch_pages.py          # Fetch and validate all pages
│   │   └── ... (10 more helper scripts)
│   └── static/css/styles.css       # Main stylesheet
├── .gitignore
├── vercel.json                     # Vercel deployment configuration
├── ACCEPTANCE_CRITERIA.md          # Detailed acceptance criteria & edge cases
├── README.md                       # This file
├── append_css.py                   # CSS generation helpers (root-level)
├── append_products_css.py
├── generate_css.py
└── report/                         # OJT reports and screenshots
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
pip install -r pharmacy_ecommerce/requirements.txt

# 4. Run database migrations
cd pharmacy_ecommerce
python manage.py migrate

# 5. (Optional) Create a superuser for admin access
python manage.py createsuperuser

# 6. (Optional) Seed full production data
python scripts/seed_prod.py

# 7. Start the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** to access the application.

Admin dashboard: **http://127.0.0.1:8000/admin/**

## Routes

| URL | View | Auth Required |
|-----|------|--------------|
| `/` | Homepage with featured products | No |
| `/about/` | About page | No |
| `/products/` | Product listing | No |
| `/products/<id>/` | Product detail | No |
| `/products/search/?q=` | Product search | No |
| `/cart/` | Shopping cart | No |
| `/cart/add/<product_id>/` | Add to cart (POST) | No |
| `/cart/remove/<product_id>/` | Remove from cart (POST) | No |
| `/cart/update/<product_id>/` | Update cart quantity (POST) | No |
| `/checkout/` | Checkout / place order | No |
| `/orders/place/` | Product selection for ordering | Yes |
| `/orders/place/<product_id>/` | Place order (legacy) | Yes |
| `/orders/success/` | Order confirmation | No |
| `/users/signup/` | User registration | No |
| `/users/profile/` | User profile with order history | Yes |
| `/login/` | Login | No |
| `/logout/` | Logout (GET: confirm, POST: execute) | No |
| `/admin/` | Django admin | Staff |
| `/contact-us/` | Contact / prescription upload | No |
| `/help-center/` | Help center | No |
| `/shipping-info/` | Shipping information | No |
| `/returns/` | Returns policy | No |
| `/privacy-policy/` | Privacy policy | No |
| `/terms-of-service/` | Terms of service | No |
| `/license-info/` | License information | No |
| `/careers/` | Careers | No |

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
python scripts/seed_prod.py           # Seed 6 users, 10 products, 10 orders
python scripts/seed_products.py       # Seed sample products
python scripts/create_superuser.py    # Seed hardcoded superuser
python scripts/create_paracetamol.py  # Seed single paracetamol product
python scripts/list_products.py       # List all products
python scripts/check_urls.py          # Verify URL responses
python scripts/acceptance_test.py     # Run acceptance criteria tests
python scripts/delete_products.py     # Delete all products from DB
python scripts/fetch_pages.py         # Fetch and validate all public pages
```

## Deployment (Vercel)

The project is pre-configured for Vercel deployment:

- **Entry point**: `api/index.py` — ASGI serverless function
- **Build**: `pharmacy_ecommerce/scripts/vercel-build.sh` runs `collectstatic`
- **Static files**: Served via Whitenoise at `/static/` URL prefix
- **Database**: Uses `DATABASE_URL` env var if set (PostgreSQL recommended); falls back to SQLite

Configuration is in `vercel.json` at the repository root.

### Production Checklist
- Set `DEBUG=False` in `settings.py` or via environment
- Use a strong, randomized `SECRET_KEY` via environment variable
- Configure `DATABASE_URL` for PostgreSQL
- Set `ALLOWED_HOSTS` to include your Vercel domain
- Run `python manage.py collectstatic` during build

## Security

- CSRF tokens on all POST forms
- `SECURE_CONTENT_TYPE_NOSNIFF = True`
- `SECURE_BROWSER_XSS_FILTER = True`
- `X_FRAME_OPTIONS = 'DENY'`
- `SESSION_COOKIE_HTTPONLY = True`, `CSRF_COOKIE_HTTPONLY = True`
- `SESSION_COOKIE_SAMESITE = 'Lax'`, `CSRF_COOKIE_SAMESITE = 'Lax'`

## Acceptance Criteria

See [ACCEPTANCE_CRITERIA.md](ACCEPTANCE_CRITERIA.md) for the full matrix of acceptance criteria and edge cases covering product catalog, authentication, order placement, admin dashboard, seed data, and sanitization.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
