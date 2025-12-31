import sqlite3
from Database.db_manager import get_connection

class OrderRepository:
    @staticmethod
    def create_order(user_id, cart_items, total_amount, shipping_address, payment_method="Cash", status="Pending", cursor=None):
        """
        Creates an order in the database.
        Args:
            cursor: Optional database cursor. If provided, assumes caller handles commit/rollback.
        """
        conn = None
        should_close_conn = False
        
        try:
            if cursor is None:
                conn = get_connection()
                cursor = conn.cursor()
                should_close_conn = True
            
            # 1. Insert Order
            sql_order = """
            INSERT INTO orders (user_id, total_amount, shipping_address, payment_method, status)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(sql_order, (user_id, total_amount, shipping_address, payment_method, status))
            
            order_id = cursor.lastrowid
            
            # 2. Insert Order Items
            sql_item = """
            INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
            VALUES (?, ?, ?, ?)
            """
            
            for item in cart_items:
                # Handle both dict (from db cart) and object (from request) if needed
                # Current usage in checkout is objects, but this repo signature expects items list 
                # Let's standardize the input expectation. 
                # If item is dict (old way):
                p_id = item.get('product_id') if isinstance(item, dict) else item.product_id
                qty = item.get('quantity') if isinstance(item, dict) else item.quantity
                price = item.get('price') if isinstance(item, dict) else (item.unit_price if hasattr(item, 'unit_price') else 0)
                
                cursor.execute(sql_item, (order_id, p_id, qty, price))
            
            if should_close_conn:
                conn.commit()
                print(f"✅ Order #{order_id} created successfully.")
            
            return order_id
            
        except Exception as e:
            if should_close_conn and conn:
                conn.rollback()
            print(f"❌ Error creating order: {e}")
            # If we are part of a transaction (external cursor), we should re-raise the exception
            # so the caller knows to rollback too.
            if not should_close_conn:
                raise e
            return None
        finally:
            if should_close_conn and conn:
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

    @staticmethod
    def get_all_orders():
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
    
            sql = """
            SELECT o.*, u.username 
            FROM orders o 
            JOIN users u ON o.user_id = u.id 
            ORDER BY o.created_at DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows 
            
        except Exception as e:
            print(f"❌ Error fetching all orders: {e}")
            return []
        finally:
            if conn: conn.close()


    @staticmethod
    def update_order_status(order_id, new_status):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = "UPDATE orders SET status = ? WHERE id = ?"
            cursor.execute(sql, (new_status, order_id))
            conn.commit()
            
            return cursor.rowcount > 0
        except Exception as e:
            print(f"❌ Error updating order status: {e}")
            return False
        finally:
            if conn: conn.close()
