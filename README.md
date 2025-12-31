# 🏭 TradeEngine

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-orange)](https://flask.palletsprojects.com/)

**Platform:** Web (Flask / Python)  
**Database:** SQLite  
**Architecture:** MVC + Blueprint Modular Design  

TradeEngine is a web-based marketplace platform designed to facilitate buying, selling, and managing industrial machines. Users can browse products, manage shopping carts and wishlists, leave reviews, and securely checkout using multiple payment methods.

---

## 📱 About The Project

TradeEngine provides an intuitive interface for users to explore machines, manage orders, and interact with the platform securely. Admins can manage products, view orders, and monitor platform activity.

---

## ✨ Key Features

- 🔐 **User Authentication** – Secure login and registration with session management.
- 🏠 **Dynamic Product Catalog** – Browse machines by category, brand, and search queries.
- 🛒 **Shopping Cart Management** – Add, remove, and modify items in your cart.
- ❤️ **Wishlist** – Save favorite products for later purchase.
- 📝 **Customer Reviews** – Rate products and leave comments.
- 💳 **Checkout & Payment** – Supports credit card payments and cash-on-delivery.
- 📦 **Order History** – View past orders with full details.
- 🌙 **Responsive Design** – Works on desktop and mobile browsers.

---

## 🛠️ Built With

**Architecture & Design Patterns:**

- MVC Pattern via Flask Blueprints
- Repository Pattern for database operations
- Template Inheritance for HTML layout consistency
- Jinja2 for dynamic HTML rendering

**Libraries & Technologies:**

| Technology | Purpose |
|------------|---------|
| Python 3 | Core backend logic |
| Flask | Web framework |
| Flask-Login | User authentication management |
| SQLite | Local database storage |
| Jinja2 | HTML templating |
| FontAwesome | UI icons |
| HTML/CSS/JS | Frontend rendering and interactivity |

---

## 📸 Screenshots

- **Home Page** – Browse categories and products  
- **Product Detail** – View machine specs and customer reviews  <img width="1600" height="798" alt="image" src="https://github.com/user-attachments/assets/5fd0abd1-cf3e-4a6b-b783-013651b7368f" />

- **Customer Reviews** – Review Rating  <img width="1600" height="803" alt="image" src="https://github.com/user-attachments/assets/9d05e353-7dac-4a77-96fe-31ee27064e37" />
<img width="1600" height="801" alt="image" src="https://github.com/user-attachments/assets/8adb039e-2062-40e1-ab5f-d07fe4bdf364" />

- **Cart Page** – Manage selected products  <img width="1600" height="804" alt="image" src="https://github.com/user-attachments/assets/240d9535-a69e-4d2d-8ddb-9f78ea5a09ab" />

- **Wishlist** – Wishlist Page <img width="1600" height="797" alt="image" src="https://github.com/user-attachments/assets/7566d279-37b2-4b15-b1ae-e7d3422504f7" />


- **Checkout Page** – Complete orders securely  <img width="1600" height="815" alt="image" src="https://github.com/user-attachments/assets/3f7d428d-74f9-4120-873f-9936f86acf75" />


- **Payment** – Payement Method <img width="1600" height="800" alt="image" src="https://github.com/user-attachments/assets/66450b70-cd5c-4fe7-84d9-f507a8e16e90" />

- **Order Confirmation** – Order Success! <img width="1600" height="783" alt="image" src="https://github.com/user-attachments/assets/56aec216-ba53-46b3-87cb-23590a3ffbf8" />



---

## 🏗️ Project Structure
```
TradeEngine/
│
├── app.py
├── payment_processor.py
├── README.md
├── .gitignore
│
├── Database/
│   ├── db_manager.py
│   ├── schema.sql
│   ├── TradeEngine.db
│   └── Repositories/
│       ├── user_repo.py
│       ├── product_repo.py
│       ├── cart_repo.py
│       ├── order_repo.py
│       ├── review_repo.py
│       └── wishlist_repo.py
│
├── models/
│   ├── __init__.py
│   ├── user_model.py
│   ├── product_model.py
│   ├── shopping_cart.py
│   ├── cart_item.py
│   ├── order.py
│   ├── payment_processor.py
│   ├── review_model.py
│   ├── wishlist.py
│   └── wishlist_item.py
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── product_route.py
│   ├── admin_routes.py
│   ├── cart_routes.py
│   ├── wishlist_routes.py
│   ├── review_routes.py
│   ├── checkout_routes.py
│   └── html_checkout_routes.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│
└── templates/
    ├── layout.html
    ├── layout_auth.html
    ├── index.html
    ├── cart.html
    ├── checkout.html
    ├── wishlist.html
    ├── orders.html
    ├── product_detail.html
    ├── order_success.html
    ├── order_error.html
    │
    ├── auth/
    │   ├── login.html
    │   └── register.html
    │
    └── admin/
        ├── dashboard.html
        ├── products.html
        └── add_edit_product.html

```

## 📋 Features Implementation

### Authentication Flow
- Email/password login and registration
- Session-based authentication
- Secure logout

### Data Management
- Repository pattern for database operations
- Dynamic product listings and user cart management

### UI/UX
- Responsive HTML templates
- Interactive cart, wishlist, and checkout pages
- Star rating system for reviews

---

## 🎯 Future Enhancements
- Integrate real payment gateways (Stripe/PayPal)
- Multi-language support
- Admin dashboard analytics
- Advanced search and filtering
- Email notifications for orders

---
## 🤝 Team Contributors

- **Zeyad Ashraf Tawfik**
- **Mona Mohamed Awad**
- **Nouran Wael ELsharkawy**
- **Nancy Ahmed Abd El-fattah**
- **Hussain Sabri Youssef**
---
