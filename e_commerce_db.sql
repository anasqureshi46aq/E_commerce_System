create database e_commerce_db;
use e_commerce_db;

-- =====================================================
-- 1. CUSTOMERS
-- =====================================================

CREATE TABLE customers (
    customer_id INT NOT NULL AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    email VARCHAR(100),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id)
);


-- =====================================================
-- 2. CATEGORIES
-- =====================================================

CREATE TABLE categories (
    category_id INT NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255),
    PRIMARY KEY (category_id)
);


-- =====================================================
-- 3. PRODUCTS
-- =====================================================

CREATE TABLE products (
    product_id INT NOT NULL AUTO_INCREMENT,
    product_name VARCHAR(150) NOT NULL,
    category_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    description VARCHAR(255),

    PRIMARY KEY (product_id),

    FOREIGN KEY (category_id)
        REFERENCES categories(category_id)
);


-- =====================================================
-- 4. ORDERS
-- =====================================================

CREATE TABLE orders (
    order_id INT NOT NULL AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
    order_status VARCHAR(30) NOT NULL DEFAULT 'Pending',

    PRIMARY KEY (order_id),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- =====================================================
-- 5. ORDER ITEMS
-- =====================================================

CREATE TABLE order_items (
    order_item_id INT NOT NULL AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,

    PRIMARY KEY (order_item_id),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);


-- =====================================================
-- 6. PAYMENTS
-- =====================================================

CREATE TABLE payments (
    payment_id INT NOT NULL AUTO_INCREMENT,
    order_id INT NOT NULL,
    payment_date DATE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(30),
    payment_status VARCHAR(30) NOT NULL DEFAULT 'Paid',

    PRIMARY KEY (payment_id),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- =====================================================
-- 7. DELIVERIES
-- =====================================================

CREATE TABLE deliveries (
    delivery_id INT NOT NULL AUTO_INCREMENT,
    order_id INT NOT NULL,
    delivery_address VARCHAR(255) NOT NULL,
    expected_delivery_date DATE,
    delivery_status VARCHAR(30) NOT NULL DEFAULT 'Pending',

    PRIMARY KEY (delivery_id),

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- =====================================================
-- CHECK TABLES
-- =====================================================

SHOW TABLES;