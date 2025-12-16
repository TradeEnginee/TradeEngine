-- Enable Foreign Key support (Crucial for SQLite data integrity)
PRAGMA foreign_keys = ON;

-- ============================================
-- 1. Users Table
-- ============================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'customer')) NOT NULL DEFAULT 'customer',
    mobile TEXT,
    -- The "JSON" column: stores customer address OR admin position as JSON
    specific_info TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 2. Products Table
-- ============================================
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    image_url TEXT,
    category TEXT NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    -- The "JSON" column: stores variable details like size, expiry date, etc., as JSON
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 3. Orders Table (Invoice Header)
-- ============================================
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_amount REAL NOT NULL,
    shipping_address TEXT NOT NULL,
    payment_method TEXT NOT NULL,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- ON DELETE CASCADE: If user is deleted, delete their orders too
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- ============================================
-- 4. Order Items Table (Invoice Contents)
-- ============================================
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    price_at_purchase REAL NOT NULL, -- The price at the moment of purchase (to freeze it)
    FOREIGN KEY (order_id) REFERENCES orders (id) ON DELETE CASCADE,
    -- ON DELETE SET NULL: If product is deleted, keep the order record but set product_id to NULL
    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE SET NULL
);

-- ============================================
-- 5. Reviews Table
-- ============================================
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5) NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
);