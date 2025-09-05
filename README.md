# Perfume Shop

A Django-based e-commerce application for selling perfumes. This project provides a complete online store with user authentication, product catalog, shopping cart, order management, and customer feedback features.

## Features

- **User Authentication**: Registration, login, password reset, and profile management
- **Product Catalog**: Browse and search perfumes with detailed product pages
- **Shopping Cart**: Add, update, and remove items from the cart
- **Order Management**: Place orders, view order history, and track status
- **Customer Feedback**: Submit and view customer reviews
- **Admin Panel**: Manage products, orders, and users through Django admin
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS

## Prerequisites

- Python 3.8 or higher
- Node.js and npm (for frontend assets)
- PostgreSQL or SQLite (configured in settings)

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd perfume_shop
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies:
   ```
   npm install
   ```

5. Apply database migrations:
   ```
   python manage.py migrate
   ```

6. Create a superuser (optional, for admin access):
   ```
   python manage.py createsuperuser
   ```

## Setup

1. Build frontend assets:
   ```
   npm run build
   ```

2. Run the development server:
   ```
   python manage.py runserver
   ```

3. Access the application at `http://127.0.0.1:8000/`

## Usage

- **Browse Products**: Visit the catalog to view available perfumes
- **User Registration**: Create an account to place orders and leave feedback
- **Shopping**: Add products to cart and proceed to checkout
- **Admin Interface**: Access `/admin/` with superuser credentials to manage the site

## Project Structure

- `accounts/`: User authentication and profile management
- `cart/`: Shopping cart functionality
- `catalog/`: Product catalog and listings
- `core/`: Main application views and templates
- `feedback/`: Customer feedback system
- `orders/`: Order processing and history
- `perfume_shop/`: Django project settings and configuration
- `static/`: CSS, images, and other static assets
- `templates/`: HTML templates

## License

This project is licensed under the MIT License.
