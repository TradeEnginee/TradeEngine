import sqlite3
from Database.db_manager import get_connection

class OrderRepository:
    @staticmethod
    def create_order(user_id, cart_items, total_amount, shipping_address, payment_method="Cash", status="Pending"):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql_order = """
            INSERT INTO orders (user_id, total_amount, shipping_address, payment_method, status)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(sql_order, (user_id, total_amount, shipping_address, payment_method, status))
            
            order_id = cursor.lastrowid
            
            sql_item = """
            INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
            VALUES (?, ?, ?, ?)
            """
            
            for item in cart_items:
                cursor.execute(sql_item, (order_id, item['product_id'], item['quantity'], item['price']))
            
            conn.commit()
            print(f"✅ Order #{order_id} created successfully.")
            return order_id
            
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Error creating order: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_user_orders(user_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC"
            cursor.execute(sql, (user_id,))
            orders = cursor.fetchall()
            return orders
        except Exception as e:
            print(f"❌ Error fetching orders: {e}")
            return []
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_order_details(order_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = """
            SELECT oi.quantity, oi.price_at_purchase, p.name, p.image_url
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
            """
            cursor.execute(sql, (order_id,))
            items = cursor.fetchall()
            return items
        except Exception as e:
            print(f"❌ Error fetching order details: {e}")
            return []
        finally:
            if conn:
                conn.close()