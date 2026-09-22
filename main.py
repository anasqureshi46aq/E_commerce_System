from connection import create_connection
from datetime import date, datetime


# ============================================================
# E-COMMERCE MANAGEMENT SYSTEM
# Python + MySQL
# ============================================================


def pause():
    input("\nPress Enter to continue...")


def get_connection():
    try:
        return create_connection()
    except Exception as e:
        print("Database connection error:", e)
        return None


# ============================================================
# 1. CUSTOMER MANAGEMENT
# ============================================================

def customer_management():
    while True:
        print("\n========== CUSTOMER MANAGEMENT ==========")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Search Customer")
        print("4. Update Customer")
        print("5. Delete Customer")
        print("6. Customer Orders")
        print("7. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_customer()
        elif choice == "2":
            view_customers()
        elif choice == "3":
            search_customer()
        elif choice == "4":
            update_customer()
        elif choice == "5":
            delete_customer()
        elif choice == "6":
            customer_orders()
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


def add_customer():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        print("\n--- Add Customer ---")
        name = input("Full Name: ")
        phone = input("Phone: ")
        email = input("Email: ")
        address = input("Address: ")

        query = """
            INSERT INTO customers (full_name, phone, email, address)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, phone, email, address))
        connection.commit()

        print("Customer added successfully!")
        print("Customer ID:", cursor.lastrowid)

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def view_customers():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT customer_id, full_name, phone, email, address
            FROM customers
            ORDER BY customer_id
        """)
        rows = cursor.fetchall()

        print("\n---------------- CUSTOMERS ----------------")
        if not rows:
            print("No customers found.")
        else:
            for row in rows:
                print(
                    f"ID: {row[0]} | Name: {row[1]} | "
                    f"Phone: {row[2]} | Email: {row[3]} | Address: {row[4]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def search_customer():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        keyword = input("Enter customer name / phone / email: ")

        cursor.execute("""
            SELECT customer_id, full_name, phone, email, address
            FROM customers
            WHERE full_name LIKE %s
               OR phone LIKE %s
               OR email LIKE %s
            ORDER BY customer_id
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

        rows = cursor.fetchall()

        if not rows:
            print("No customer found.")
        else:
            for row in rows:
                print(
                    f"ID: {row[0]} | Name: {row[1]} | "
                    f"Phone: {row[2]} | Email: {row[3]} | Address: {row[4]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def update_customer():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        customer_id = input("Enter Customer ID: ")

        cursor.execute(
            "SELECT customer_id, full_name, phone, email, address FROM customers WHERE customer_id=%s",
            (customer_id,)
        )
        customer = cursor.fetchone()

        if not customer:
            print("Customer not found.")
            return

        print("\nLeave blank if you don't want to change a value.")

        name = input(f"Full Name [{customer[1]}]: ") or customer[1]
        phone = input(f"Phone [{customer[2]}]: ") or customer[2]
        email = input(f"Email [{customer[3]}]: ") or customer[3]
        address = input(f"Address [{customer[4]}]: ") or customer[4]

        cursor.execute("""
            UPDATE customers
            SET full_name=%s, phone=%s, email=%s, address=%s
            WHERE customer_id=%s
        """, (name, phone, email, address, customer_id))

        connection.commit()
        print("Customer updated successfully!")

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def delete_customer():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        customer_id = input("Enter Customer ID to delete: ")

        cursor.execute(
            "SELECT full_name FROM customers WHERE customer_id=%s",
            (customer_id,)
        )
        customer = cursor.fetchone()

        if not customer:
            print("Customer not found.")
            return

        confirm = input(f"Delete {customer[0]}? (y/n): ").lower()

        if confirm == "y":
            cursor.execute(
                "DELETE FROM customers WHERE customer_id=%s",
                (customer_id,)
            )
            connection.commit()
            print("Customer deleted successfully.")
        else:
            print("Delete cancelled.")

    except Exception as e:
        connection.rollback()
        print("Cannot delete customer:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def customer_orders():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        customer_id = input("Enter Customer ID: ")

        cursor.execute("""
            SELECT o.order_id, o.order_date, o.total_amount, o.order_status
            FROM orders o
            WHERE o.customer_id=%s
            ORDER BY o.order_id DESC
        """, (customer_id,))

        rows = cursor.fetchall()

        if not rows:
            print("No orders found for this customer.")
        else:
            for row in rows:
                print(
                    f"Order ID: {row[0]} | Date: {row[1]} | "
                    f"Amount: {row[2]} | Status: {row[3]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


# ============================================================
# 2. CATEGORY MANAGEMENT
# ============================================================

def category_management():
    while True:
        print("\n========== CATEGORY MANAGEMENT ==========")
        print("1. Add Category")
        print("2. View Categories")
        print("3. Update Category")
        print("4. Delete Category")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_category()
        elif choice == "2":
            view_categories()
        elif choice == "3":
            update_category()
        elif choice == "4":
            delete_category()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def add_category():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        name = input("Category Name: ")
        description = input("Description: ")

        cursor.execute("""
            INSERT INTO categories (category_name, description)
            VALUES (%s, %s)
        """, (name, description))

        connection.commit()
        print("Category added successfully!")
        print("Category ID:", cursor.lastrowid)

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def view_categories():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT category_id, category_name, description
            FROM categories
            ORDER BY category_id
        """)
        rows = cursor.fetchall()

        if not rows:
            print("No categories found.")
        else:
            for row in rows:
                print(f"ID: {row[0]} | {row[1]} | {row[2]}")

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def update_category():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        category_id = input("Category ID: ")

        cursor.execute(
            "SELECT category_name, description FROM categories WHERE category_id=%s",
            (category_id,)
        )
        row = cursor.fetchone()

        if not row:
            print("Category not found.")
            return

        name = input(f"Category Name [{row[0]}]: ") or row[0]
        description = input(f"Description [{row[1]}]: ") or row[1]

        cursor.execute("""
            UPDATE categories
            SET category_name=%s, description=%s
            WHERE category_id=%s
        """, (name, description, category_id))

        connection.commit()
        print("Category updated successfully.")

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def delete_category():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        category_id = input("Category ID: ")

        cursor.execute(
            "DELETE FROM categories WHERE category_id=%s",
            (category_id,)
        )
        connection.commit()
        print("Category deleted successfully.")

    except Exception as e:
        connection.rollback()
        print("Cannot delete category:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


# ============================================================
# 3. PRODUCT MANAGEMENT
# ============================================================

def product_management():
    while True:
        print("\n========== PRODUCT MANAGEMENT ==========")
        print("1. Add Product")
        print("2. View Products")
        print("3. Search Product")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Low Stock Products")
        print("7. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_product()
        elif choice == "2":
            view_products()
        elif choice == "3":
            search_product()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            low_stock_products()
        elif choice == "7":
            break
        else:
            print("Invalid choice.")


def add_product():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        print("\n--- Add Product ---")

        name = input("Product Name: ")
        category_id = input("Category ID: ")
        price = float(input("Price: "))
        stock = int(input("Initial Stock: "))
        description = input("Description: ")

        cursor.execute("""
            INSERT INTO products
            (product_name, category_id, price, stock_quantity, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, category_id, price, stock, description))

        connection.commit()

        print("Product added successfully!")
        print("Product ID:", cursor.lastrowid)

    except ValueError:
        print("Price must be a number and stock must be an integer.")
    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def view_products():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT p.product_id, p.product_name,
                   c.category_name, p.price,
                   p.stock_quantity, p.description
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            ORDER BY p.product_id
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No products found.")
        else:
            print("\n---------------- PRODUCTS ----------------")
            for row in rows:
                print(
                    f"ID: {row[0]} | Product: {row[1]} | "
                    f"Category: {row[2]} | Price: {row[3]} | "
                    f"Stock: {row[4]} | Description: {row[5]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def search_product():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        keyword = input("Enter product name/category: ")

        cursor.execute("""
            SELECT p.product_id, p.product_name,
                   c.category_name, p.price, p.stock_quantity
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.category_id
            WHERE p.product_name LIKE %s
               OR c.category_name LIKE %s
            ORDER BY p.product_id
        """, (f"%{keyword}%", f"%{keyword}%"))

        rows = cursor.fetchall()

        if not rows:
            print("No product found.")
        else:
            for row in rows:
                print(
                    f"ID: {row[0]} | {row[1]} | Category: {row[2]} | "
                    f"Price: {row[3]} | Stock: {row[4]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def update_product():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        product_id = input("Product ID: ")

        cursor.execute("""
            SELECT product_name, category_id, price,
                   stock_quantity, description
            FROM products
            WHERE product_id=%s
        """, (product_id,))

        row = cursor.fetchone()

        if not row:
            print("Product not found.")
            return

        name = input(f"Product Name [{row[0]}]: ") or row[0]
        category_id = input(f"Category ID [{row[1]}]: ") or row[1]
        price = input(f"Price [{row[2]}]: ") or row[2]
        stock = input(f"Stock [{row[3]}]: ") or row[3]
        description = input(f"Description [{row[4]}]: ") or row[4]

        cursor.execute("""
            UPDATE products
            SET product_name=%s, category_id=%s, price=%s,
                stock_quantity=%s, description=%s
            WHERE product_id=%s
        """, (name, category_id, price, stock, description, product_id))

        connection.commit()
        print("Product updated successfully.")

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def delete_product():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        product_id = input("Product ID to delete: ")

        cursor.execute(
            "DELETE FROM products WHERE product_id=%s",
            (product_id,)
        )
        connection.commit()
        print("Product deleted successfully.")

    except Exception as e:
        connection.rollback()
        print("Cannot delete product:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def low_stock_products():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        limit = int(input("Show products with stock <= "))

        cursor.execute("""
            SELECT product_id, product_name, stock_quantity, price
            FROM products
            WHERE stock_quantity <= %s
            ORDER BY stock_quantity
        """, (limit,))

        rows = cursor.fetchall()

        if not rows:
            print("No low-stock products found.")
        else:
            for row in rows:
                print(
                    f"ID: {row[0]} | {row[1]} | "
                    f"Stock: {row[2]} | Price: {row[3]}"
                )

    except ValueError:
        print("Please enter a valid number.")
    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


# ============================================================
# 4. ORDER MANAGEMENT
# ============================================================

def order_management():
    while True:
        print("\n========== ORDER MANAGEMENT ==========")
        print("1. Place New Order")
        print("2. View All Orders")
        print("3. View Order Details")
        print("4. Update Order Status")
        print("5. Cancel Order")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            place_order()
        elif choice == "2":
            view_orders()
        elif choice == "3":
            view_order_details()
        elif choice == "4":
            update_order_status()
        elif choice == "5":
            cancel_order()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


def place_order():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        customer_id = input("Customer ID: ")

        cursor.execute(
            "SELECT full_name FROM customers WHERE customer_id=%s",
            (customer_id,)
        )
        customer = cursor.fetchone()

        if not customer:
            print("Customer not found.")
            return

        product_id = input("Product ID: ")
        quantity = int(input("Quantity: "))

        cursor.execute("""
            SELECT product_name, price, stock_quantity
            FROM products
            WHERE product_id=%s
        """, (product_id,))

        product = cursor.fetchone()

        if not product:
            print("Product not found.")
            return

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return

        if product[2] < quantity:
            print("Insufficient stock.")
            return

        total_amount = float(product[1]) * quantity

        # Create order
        cursor.execute("""
            INSERT INTO orders
            (customer_id, order_date, total_amount, order_status)
            VALUES (%s, CURDATE(), %s, 'Pending')
        """, (customer_id, total_amount))

        order_id = cursor.lastrowid

        # Create order item
        cursor.execute("""
            INSERT INTO order_items
            (order_id, product_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, product_id, quantity, product[1]))

        # Reduce stock
        cursor.execute("""
            UPDATE products
            SET stock_quantity = stock_quantity - %s
            WHERE product_id=%s
        """, (quantity, product_id))

        connection.commit()

        print("\nOrder placed successfully!")
        print("Order ID:", order_id)
        print("Customer:", customer[0])
        print("Product:", product[0])
        print("Quantity:", quantity)
        print("Total Amount:", total_amount)

    except ValueError:
        connection.rollback()
        print("Quantity must be a valid integer.")
    except Exception as e:
        connection.rollback()
        print("Order failed:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def view_orders():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT o.order_id, c.full_name, o.order_date,
                   o.total_amount, o.order_status
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            ORDER BY o.order_id DESC
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No orders found.")
        else:
            for row in rows:
                print(
                    f"Order ID: {row[0]} | Customer: {row[1]} | "
                    f"Date: {row[2]} | Amount: {row[3]} | Status: {row[4]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def view_order_details():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        order_id = input("Order ID: ")

        cursor.execute("""
            SELECT o.order_id, c.full_name, o.order_date,
                   o.total_amount, o.order_status
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_id=%s
        """, (order_id,))

        order = cursor.fetchone()

        if not order:
            print("Order not found.")
            return

        print("\n--- ORDER DETAILS ---")
        print("Order ID:", order[0])
        print("Customer:", order[1])
        print("Order Date:", order[2])
        print("Total:", order[3])
        print("Status:", order[4])

        cursor.execute("""
            SELECT p.product_name, oi.quantity, oi.price,
                   (oi.quantity * oi.price) AS subtotal
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            WHERE oi.order_id=%s
        """, (order_id,))

        items = cursor.fetchall()

        print("\nItems:")
        for item in items:
            print(
                f"{item[0]} | Qty: {item[1]} | "
                f"Price: {item[2]} | Subtotal: {item[3]}"
            )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def update_order_status():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        order_id = input("Order ID: ")

        print("\n1. Pending")
        print("2. Confirmed")
        print("3. Shipped")
        print("4. Delivered")
        print("5. Cancelled")

        choice = input("Choose status: ")

        status_map = {
            "1": "Pending",
            "2": "Confirmed",
            "3": "Shipped",
            "4": "Delivered",
            "5": "Cancelled"
        }

        if choice not in status_map:
            print("Invalid status.")
            return

        cursor.execute("""
            UPDATE orders
            SET order_status=%s
            WHERE order_id=%s
        """, (status_map[choice], order_id))

        connection.commit()
        print("Order status updated successfully.")

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def cancel_order():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        order_id = input("Order ID to cancel: ")

        cursor.execute("""
            SELECT order_status
            FROM orders
            WHERE order_id=%s
        """, (order_id,))

        order = cursor.fetchone()

        if not order:
            print("Order not found.")
            return

        if order[0] == "Cancelled":
            print("Order is already cancelled.")
            return

        if order[0] == "Delivered":
            print("Delivered order cannot be cancelled.")
            return

        # Return product quantities to stock
        cursor.execute("""
            SELECT product_id, quantity
            FROM order_items
            WHERE order_id=%s
        """, (order_id,))

        items = cursor.fetchall()

        for product_id, quantity in items:
            cursor.execute("""
                UPDATE products
                SET stock_quantity = stock_quantity + %s
                WHERE product_id=%s
            """, (quantity, product_id))

        cursor.execute("""
            UPDATE orders
            SET order_status='Cancelled'
            WHERE order_id=%s
        """, (order_id,))

        connection.commit()
        print("Order cancelled and stock restored.")

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


# ============================================================
# 5. PAYMENT MANAGEMENT
# ============================================================

def payment_management():
    while True:
        print("\n========== PAYMENT MANAGEMENT ==========")
        print("1. Make Payment")
        print("2. View Payments")
        print("3. Payment History by Order")
        print("4. Update Payment Status")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            make_payment()
        elif choice == "2":
            view_payments()
        elif choice == "3":
            payment_history()
        elif choice == "4":
            update_payment_status()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def make_payment():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        order_id = input("Order ID: ")

        cursor.execute("""
            SELECT total_amount, order_status
            FROM orders
            WHERE order_id=%s
        """, (order_id,))

        order = cursor.fetchone()

        if not order:
            print("Order not found.")
            return

        if order[1] == "Cancelled":
            print("Cannot pay for a cancelled order.")
            return

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM payments
            WHERE order_id=%s AND payment_status='Paid'
        """, (order_id,))

        paid = float(cursor.fetchone()[0])
        total = float(order[0])
        balance = total - paid

        print("Order Total:", total)
        print("Already Paid:", paid)
        print("Balance:", balance)

        if balance <= 0:
            print("Order is already fully paid.")
            return

        amount = float(input("Payment Amount: "))

        if amount <= 0 or amount > balance:
            print("Invalid payment amount.")
            return

        method = input("Payment Method (Cash/Card/UPI): ")

        status = "Paid"

        cursor.execute("""
            INSERT INTO payments
            (order_id, payment_date, amount, payment_method, payment_status)
            VALUES (%s, CURDATE(), %s, %s, %s)
        """, (order_id, amount, method, status))

        connection.commit()

        print("Payment successful!")
        print("Payment ID:", cursor.lastrowid)

    except ValueError:
        connection.rollback()
        print("Amount must be a valid number.")
    except Exception as e:
        connection.rollback()
        print("Payment failed:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def view_payments():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT p.payment_id, p.order_id, c.full_name,
                   p.payment_date, p.amount,
                   p.payment_method, p.payment_status
            FROM payments p
            JOIN orders o ON p.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            ORDER BY p.payment_id DESC
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No payments found.")
        else:
            for row in rows:
                print(
                    f"Payment ID: {row[0]} | Order: {row[1]} | "
                    f"Customer: {row[2]} | Date: {row[3]} | "
                    f"Amount: {row[4]} | Method: {row[5]} | "
                    f"Status: {row[6]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def payment_history():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        order_id = input("Order ID: ")

        cursor.execute("""
            SELECT payment_id, payment_date, amount,
                   payment_method, payment_status
            FROM payments
            WHERE order_id=%s
            ORDER BY payment_id
        """, (order_id,))

        rows = cursor.fetchall()

        if not rows:
            print("No payment history found.")
        else:
            for row in rows:
                print(
                    f"Payment ID: {row[0]} | Date: {row[1]} | "
                    f"Amount: {row[2]} | Method: {row[3]} | Status: {row[4]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def update_payment_status():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        payment_id = input("Payment ID: ")

        print("1. Paid")
        print("2. Pending")
        print("3. Failed")
        print("4. Cancelled")

        choice = input("Choose status: ")

        status_map = {
            "1": "Paid",
            "2": "Pending",
            "3": "Failed",
            "4": "Cancelled"
        }

        if choice not in status_map:
            print("Invalid choice.")
            return

        cursor.execute("""
            UPDATE payments
            SET payment_status=%s
            WHERE payment_id=%s
        """, (status_map[choice], payment_id))

        connection.commit()
        print("Payment status updated.")

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


# ============================================================
# 6. INVENTORY MANAGEMENT
# ============================================================

def inventory_management():
    while True:
        print("\n========== INVENTORY MANAGEMENT ==========")
        print("1. View Inventory")
        print("2. Add Stock")
        print("3. Reduce Stock")
        print("4. Low Stock Report")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_stock()
        elif choice == "3":
            reduce_stock()
        elif choice == "4":
            low_stock_products()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def view_inventory():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT product_id, product_name,
                   stock_quantity, price
            FROM products
            ORDER BY stock_quantity
        """)

        rows = cursor.fetchall()

        if not rows:
            print("Inventory is empty.")
        else:
            print("\n------------- INVENTORY -------------")
            for row in rows:
                print(
                    f"Product ID: {row[0]} | {row[1]} | "
                    f"Stock: {row[2]} | Price: {row[3]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def add_stock():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        product_id = input("Product ID: ")
        quantity = int(input("Quantity to add: "))

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return

        cursor.execute("""
            UPDATE products
            SET stock_quantity = stock_quantity + %s
            WHERE product_id=%s
        """, (quantity, product_id))

        if cursor.rowcount == 0:
            print("Product not found.")
            return

        connection.commit()
        print("Stock added successfully.")

    except ValueError:
        connection.rollback()
        print("Quantity must be an integer.")
    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def reduce_stock():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        product_id = input("Product ID: ")
        quantity = int(input("Quantity to reduce: "))

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return

        cursor.execute("""
            SELECT stock_quantity
            FROM products
            WHERE product_id=%s
        """, (product_id,))

        row = cursor.fetchone()

        if not row:
            print("Product not found.")
            return

        if row[0] < quantity:
            print("Not enough stock.")
            return

        cursor.execute("""
            UPDATE products
            SET stock_quantity = stock_quantity - %s
            WHERE product_id=%s
        """, (quantity, product_id))

        connection.commit()
        print("Stock reduced successfully.")

    except ValueError:
        connection.rollback()
        print("Quantity must be an integer.")
    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


# ============================================================
# 7. DELIVERY MANAGEMENT
# ============================================================

def delivery_management():
    while True:
        print("\n========== DELIVERY MANAGEMENT ==========")
        print("1. Create Delivery")
        print("2. View Deliveries")
        print("3. Update Delivery Status")
        print("4. Search Delivery")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_delivery()
        elif choice == "2":
            view_deliveries()
        elif choice == "3":
            update_delivery_status()
        elif choice == "4":
            search_delivery()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def create_delivery():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        order_id = input("Order ID: ")
        address = input("Delivery Address: ")
        delivery_date = input("Expected Delivery Date (YYYY-MM-DD): ")

        cursor.execute(
            "SELECT order_id FROM orders WHERE order_id=%s",
            (order_id,)
        )

        if not cursor.fetchone():
            print("Order not found.")
            return

        cursor.execute("""
            INSERT INTO deliveries
            (order_id, delivery_address, expected_delivery_date, delivery_status)
            VALUES (%s, %s, %s, 'Pending')
        """, (order_id, address, delivery_date))

        connection.commit()

        print("Delivery created successfully!")
        print("Delivery ID:", cursor.lastrowid)

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def view_deliveries():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT d.delivery_id, d.order_id, c.full_name,
                   d.delivery_address, d.expected_delivery_date,
                   d.delivery_status
            FROM deliveries d
            JOIN orders o ON d.order_id = o.order_id
            JOIN customers c ON o.customer_id = c.customer_id
            ORDER BY d.delivery_id DESC
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No deliveries found.")
        else:
            for row in rows:
                print(
                    f"Delivery ID: {row[0]} | Order: {row[1]} | "
                    f"Customer: {row[2]} | Address: {row[3]} | "
                    f"Expected: {row[4]} | Status: {row[5]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def update_delivery_status():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        delivery_id = input("Delivery ID: ")

        print("1. Pending")
        print("2. Shipped")
        print("3. Out for Delivery")
        print("4. Delivered")
        print("5. Cancelled")

        choice = input("Choose status: ")

        status_map = {
            "1": "Pending",
            "2": "Shipped",
            "3": "Out for Delivery",
            "4": "Delivered",
            "5": "Cancelled"
        }

        if choice not in status_map:
            print("Invalid choice.")
            return

        cursor.execute("""
            UPDATE deliveries
            SET delivery_status=%s
            WHERE delivery_id=%s
        """, (status_map[choice], delivery_id))

        connection.commit()
        print("Delivery status updated.")

    except Exception as e:
        connection.rollback()
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def search_delivery():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        keyword = input("Enter Delivery ID / Order ID / status: ")

        cursor.execute("""
            SELECT delivery_id, order_id, delivery_address,
                   expected_delivery_date, delivery_status
            FROM deliveries
            WHERE CAST(delivery_id AS CHAR) LIKE %s
               OR CAST(order_id AS CHAR) LIKE %s
               OR delivery_status LIKE %s
            ORDER BY delivery_id DESC
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

        rows = cursor.fetchall()

        if not rows:
            print("No delivery found.")
        else:
            for row in rows:
                print(
                    f"Delivery ID: {row[0]} | Order: {row[1]} | "
                    f"Address: {row[2]} | Expected: {row[3]} | "
                    f"Status: {row[4]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


# ============================================================
# 8. SEARCH
# ============================================================

def search_menu():
    while True:
        print("\n========== SEARCH ==========")
        print("1. Search Customer")
        print("2. Search Product")
        print("3. Search Order")
        print("4. Search Delivery")
        print("5. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            search_customer()
        elif choice == "2":
            search_product()
        elif choice == "3":
            search_order()
        elif choice == "4":
            search_delivery()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def search_order():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        keyword = input("Enter Order ID / Customer Name / Status: ")

        cursor.execute("""
            SELECT o.order_id, c.full_name,
                   o.order_date, o.total_amount, o.order_status
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE CAST(o.order_id AS CHAR) LIKE %s
               OR c.full_name LIKE %s
               OR o.order_status LIKE %s
            ORDER BY o.order_id DESC
        """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

        rows = cursor.fetchall()

        if not rows:
            print("No order found.")
        else:
            for row in rows:
                print(
                    f"Order ID: {row[0]} | Customer: {row[1]} | "
                    f"Date: {row[2]} | Amount: {row[3]} | Status: {row[4]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


# ============================================================
# 9. REPORTS & ANALYTICS
# ============================================================

def reports_menu():
    while True:
        print("\n========== REPORTS & ANALYTICS ==========")
        print("1. Total Sales")
        print("2. Total Orders")
        print("3. Total Customers")
        print("4. Product Sales Report")
        print("5. Top Customers")
        print("6. Low Stock Report")
        print("7. Monthly Sales")
        print("8. Back to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            total_sales_report()
        elif choice == "2":
            total_orders_report()
        elif choice == "3":
            total_customers_report()
        elif choice == "4":
            product_sales_report()
        elif choice == "5":
            top_customers_report()
        elif choice == "6":
            low_stock_products()
        elif choice == "7":
            monthly_sales_report()
        elif choice == "8":
            break
        else:
            print("Invalid choice.")


def total_sales_report():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM payments
            WHERE payment_status='Paid'
        """)

        total = cursor.fetchone()[0]
        print("\nTotal Sales:", total)

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def total_orders_report():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM orders")
        print("\nTotal Orders:", cursor.fetchone()[0])

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def total_customers_report():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT COUNT(*) FROM customers")
        print("\nTotal Customers:", cursor.fetchone()[0])

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def product_sales_report():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT p.product_id, p.product_name,
                   COALESCE(SUM(oi.quantity), 0) AS units_sold,
                   COALESCE(SUM(oi.quantity * oi.price), 0) AS revenue
            FROM products p
            LEFT JOIN order_items oi
                ON p.product_id = oi.product_id
            LEFT JOIN orders o
                ON oi.order_id = o.order_id
                AND o.order_status <> 'Cancelled'
            GROUP BY p.product_id, p.product_name
            ORDER BY revenue DESC
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No product sales data.")
        else:
            for row in rows:
                print(
                    f"ID: {row[0]} | {row[1]} | "
                    f"Units Sold: {row[2]} | Revenue: {row[3]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def top_customers_report():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT c.customer_id, c.full_name,
                   COUNT(o.order_id) AS total_orders,
                   COALESCE(SUM(o.total_amount), 0) AS total_spent
            FROM customers c
            LEFT JOIN orders o
                ON c.customer_id = o.customer_id
                AND o.order_status <> 'Cancelled'
            GROUP BY c.customer_id, c.full_name
            ORDER BY total_spent DESC
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No customer data.")
        else:
            for row in rows:
                print(
                    f"Customer ID: {row[0]} | {row[1]} | "
                    f"Orders: {row[2]} | Total Spent: {row[3]}"
                )

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


def monthly_sales_report():
    connection = get_connection()
    if not connection:
        return

    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT DATE_FORMAT(payment_date, '%Y-%m') AS month,
                   SUM(amount) AS total_sales
            FROM payments
            WHERE payment_status='Paid'
            GROUP BY DATE_FORMAT(payment_date, '%Y-%m')
            ORDER BY month DESC
        """)

        rows = cursor.fetchall()

        if not rows:
            print("No sales data.")
        else:
            for row in rows:
                print(f"Month: {row[0]} | Sales: {row[1]}")

    except Exception as e:
        print("Error:", e)

    finally:
        cursor.close()
        connection.close()
        pause()


# ============================================================
# MAIN MENU
# ============================================================

def main():
    while True:
        print("\n")
        print("==============================================")
        print("       E-COMMERCE MANAGEMENT SYSTEM")
        print("==============================================")
        print("1. Customer Management")
        print("2. Product Management")
        print("3. Category Management")
        print("4. Order Management")
        print("5. Payment Management")
        print("6. Inventory Management")
        print("7. Delivery Management")
        print("8. Search")
        print("9. Reports & Analytics")
        print("10. Exit")
        print("==============================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            customer_management()

        elif choice == "2":
            product_management()

        elif choice == "3":
            category_management()

        elif choice == "4":
            order_management()

        elif choice == "5":
            payment_management()

        elif choice == "6":
            inventory_management()

        elif choice == "7":
            delivery_management()

        elif choice == "8":
            search_menu()

        elif choice == "9":
            reports_menu()

        elif choice == "10":
            print("\nThank you for using E-Commerce Management System!")
            print("Program closed.")
            break

        else:
            print("Invalid choice. Please enter 1 to 10.")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()
