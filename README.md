# 🛒 E-Commerce Management System

## 📌 Project Overview

This project is a full-featured E-Commerce Management System developed using **Python**, **Flask**, and **SQLite**, following **Object-Oriented Programming (OOP)** principles and a **layered architecture**.

The system supports:

- User authentication and role management
- Product catalog and detailed product pages
- Stock and inventory control
- Shopping cart and order processing
- Review and rating system
- Search and sorting functionalities
- REST-style API endpoints for product browsing

---

## 🏗️ System Architecture

The project follows a modular architecture with clear separation of concerns:

Presentation Layer (Flask / Routes)
↓
Business Logic Layer (Models)
↓
Data Access Layer (Repositories)
↓
Database (SQLite)

---

## 📂 Project Structure

project/
│
├── app.py
├── Database/
│ ├── db_manager.py
│ ├── schema.sql
│ └── Repositories/
│ ├── user_repo.py
│ ├── product_repo.py
│ ├── order_repo.py
│ └── review_repo.py
│
├── models/
│ ├── user_model.py
│ ├── product_model.py
│ ├── product_base.py
│ ├── detailed_product.py
│ ├── detailed_product_types.py
│ ├── review_system.py
│ ├── catalog.py
│ └── search_engine.py
│
├── routes/
│ ├── auth.py
│ └── shop.py
│
└── templates/

---

## 👤 User Management

**User Roles:**

- Customer
- Admin

**Features:**

- Secure registration and login
- Password hashing using `werkzeug.security`
- Role-based behavior
- User profile updates and deletion

**Key Classes:**

- `User`
- `Customer`
- `Admin`

---

## 📦 Product Management

### Base Product Model

The system uses an abstract base class to define common product attributes:

**Product (Abstract)**

**Attributes:**

- `id`
- `name`
- `price`
- `image_url`
- `category`

---

### 🧩 Product Details Module

**Class Hierarchy:**

Product (Abstract)
│
▼
DetailedProduct
│
├── DetailedCosmeticsProduct
├── DetailedFoodProduct
├── DetailedClothesProduct
└── DetailedSportsProduct

**DetailedProduct Responsibilities:**

- Stock management
- Review system integration
- Full product detail generation

**Key Methods:**

- `get_stock_status()`
- `get_full_details()`

**Product-Specific Implementations:**

| Product Type | Additional Attributes        |
|--------------|------------------------------|
| Cosmetics    | brand, skin_type            |
| Food         | expiry_date                 |
| Clothes      | brand, size                 |
| Sports       | material, sport_type        |

---

## 📊 Stock Management

Each product contains a stock quantity with validation.

**Stock Status Rules:**

| Quantity | Status             |
|----------|------------------|
| 0        | Out of stock      |
| 1–5      | Limited stock     |
| >5       | In stock          |

Stock status is automatically included in product details.

---

## ⭐ Review & Rating System

Each detailed product includes an independent `ReviewSystem`.

**Features:**

- Add reviews with rating (1–5)
- Calculate average rating
- Count total reviews
- Review data is returned as part of product details

---

## 🛒 Shopping Cart

- Cart is stored in the user session
- Supports adding, incrementing, and clearing items
- Stock availability is validated before adding items

---

## 🧾 Order Management

**Order Processing:**

- Create orders from cart items
- Store order headers and order items separately
- Maintain purchase price history
- Support transactional integrity using commits and rollbacks

**Tables:**

- `orders`
- `order_items`

---

## 🔍 Search & Sorting

**Search Features:**

- Keyword-based product search
- Category-based browsing

**Sorting Options:**

- Price (ascending / descending)
- Name (A–Z / Z–A)
- Creation date

---

## 🗄️ Database Design

The database uses SQLite with enforced foreign key constraints.

**Main Tables:**

- `users`
- `products`
- `orders`
- `order_items`
- `reviews`

All relationships maintain referential integrity.

---

**Notes:**

- JSON used in `users.specific_info` and `products.details` for flexible data storage.  
- Foreign keys with `ON DELETE CASCADE` / `ON DELETE SET NULL` for data integrity.  

---

## 🧠 Design Principles

- Object-Oriented Programming: Inheritance, Polymorphism, Encapsulation  
- Repository pattern for database access  
- Modular and maintainable code  
- Validation for inputs: price ≥ 0, stock ≥ 0, rating 1–5, email/password formats  

---

## 🚀 Future Enhancements

- Payment integration  
- Admin dashboard  
- Wishlist and recommendations  
- Pagination and filtering  
- Enhanced semantic search  

---

## ✅ Conclusion

Comprehensive E-Commerce project featuring:

- Advanced product modeling  
- Integrated review system  
- Shopping cart and order management with transaction integrity  
- Dynamic search and sorting  
- Ready for frontend integration or API extension
