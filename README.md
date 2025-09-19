# Sai Baba Cafe - Django Web Application

## Description

Sai Baba Cafe is a comprehensive Django-based web application designed for an online cafe ordering system. It provides a platform for customers to browse food and beverage products, manage shopping carts, place orders, and interact with the cafe through reviews and contact forms. The application includes user authentication, admin panel for management, and a blog section for announcements and updates.

## Features

- **User Authentication**: Custom user model with email-based login, registration, and profile management
- **Product Catalog**: Organized products by categories and subcategories with images and descriptions
- **Shopping Cart**: Add, remove, and update item quantities in the cart
- **Checkout Process**: Secure checkout with address details and payment integration (PayPal)
- **Order Management**: Track orders and generate bills
- **Customer Reviews**: Submit and view customer reviews
- **Contact Form**: Easy communication with the cafe
- **Blog Section**: News, updates, and announcements
- **Admin Panel**: Comprehensive Django admin interface for content management
- **Responsive Design**: Mobile-friendly interface

## Technologies Used

- **Backend**: Django 4.0.3
- **Database**: SQLite (default), with MySQL support
- **Frontend**: HTML, CSS, JavaScript
- **Static Files**: WhiteNoise for serving static files
- **Deployment**: Gunicorn for production server
- **PDF Generation**: xhtml2pdf for bill generation
- **Other Libraries**: BeautifulSoup4 for web scraping (if needed)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sai-baba-cafe.git
   cd sai-baba-cafe
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Usage

### For Customers

1. **Browse Products**: Visit the homepage to view products by category
2. **Register/Login**: Create an account or log in to access cart and checkout
3. **Add to Cart**: Select products and add them to your shopping cart
4. **Checkout**: Provide shipping details and complete payment
5. **Track Orders**: Use the tracker page to monitor your orders
6. **Leave Reviews**: Share your experience with the cafe
7. **Contact**: Use the contact form for inquiries

### For Administrators

1. **Access Admin Panel**: Log in at /admin/ with superuser credentials
2. **Manage Products**: Add, edit, or remove products
3. **View Orders**: Monitor customer orders and payments
4. **Manage Users**: Handle user accounts and permissions
5. **Content Management**: Update blog posts and static content

## Project Structure

```
sai-baba-cafe/
├── cafe/                 # Main Django project settings
├── home/                 # Main app for cafe functionality
├── users/                # User authentication app
├── blog/                 # Blog app for news and updates
├── staticfiles/          # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── media/                # User-uploaded media files
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── Procfile              # Heroku deployment configuration
└── README.md             # This file
```

## Database Models

- **UserAccount**: Custom user model with email authentication
- **Product**: Food and beverage items with categories
- **CartItem**: Shopping cart items
- **Checkout**: Order checkout information
- **Order**: Individual order items
- **Payment**: Payment records
- **Reviews**: Customer reviews
- **ContactUs**: Contact form submissions

## Deployment

### Heroku Deployment

1. Install Heroku CLI
2. Create a Heroku app
3. Set environment variables in Heroku dashboard
4. Push code to Heroku:
   ```bash
   git push heroku main
   ```

### Environment Variables

Set the following environment variables for production:

- `DEBUG=False`
- `SECRET_KEY=your-secret-key`
- `DATABASE_URL` (if using PostgreSQL on Heroku)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact the development team or use the contact form within the application.

---

**Note**: This application is for educational and demonstration purposes. For production use, ensure proper security measures are implemented, including HTTPS, secure payment processing, and regular security updates.# Cafe-Management
