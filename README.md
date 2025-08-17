perfume_shop/                # Main project folder (Git root)
│
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── README.md                # Documentation
│
├── perfume_shop/            # Project configuration
│   ├── __init__.py
│   ├── settings.py          # Django + PostgreSQL settings
│   ├── urls.py              # Project-wide URL routing
│   ├── wsgi.py              # WSGI entry point
│   ├── asgi.py              # For async support (optional)
│
├── catalog/                 # App for product catalog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/catalog/   # HTML templates for product list/detail
│   ├── static/catalog/      # App-specific CSS/JS/images
│
├── cart/                    # App for shopping cart
│   ├── __init__.py
│   ├── cart.py              # Session-based cart logic
│   ├── context_processors.py# Makes cart available globally in templates
│   ├── views.py
│   ├── urls.py
│   ├── templates/cart/
│
├── orders/                  # App for orders & checkout
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── forms.py             # Checkout form
│   ├── views.py
│   ├── urls.py
│   ├── templates/orders/
│
├── core/                    # App for homepage, about, contact
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   ├── templates/core/
│
├── static/                  # Global static files (CSS/JS/images)
│
├── media/                   # Uploaded product images
│
└── templates/               # Global templates (base.html, layout)
    ├── base.html
    ├── includes/            # Header, footer, navbar snippets
