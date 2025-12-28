import sqlite3
from Database.db_manager import get_connection
from models.shopping_cart import ShoppingCart
from models.cart_item import CartItem
from Repositories.product_repo import ProductRepository

class CartRepository:
    @staticmethod
    def _map_row_to_object(row, user_object):
        if not row:
            return None      
        product = ProductRepository.get_product_by_id(row['product_id'])
        
        if product:
            return CartItem(
                item_id=row['id'],
                user=user_object,
                product=product,
                quantity=row['quantity']
            )
        return None

    @staticmethod
    def get_cart_by_user(user_object):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM cart_items WHERE user_id = ?"
            cursor.execute(sql, (user_object.id,))
            rows = cursor.fetchall()
            cart = ShoppingCart(user_object)
            for row in rows:
                item = CartRepository._map_row_to_object(row, user_object)
                if item:
                    cart._items.append(item)     
            return cart

        except Exception as e:
            print(f"❌ Error fetching cart: {e}")
            return None
        finally:
            if conn: conn.close()

    @staticmethod
    def update_quantity(user_id, product_id, new_quantity):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "UPDATE cart_items SET quantity = ? WHERE user_id = ? AND product_id = ?"
            cursor.execute(sql, (new_quantity, user_id, product_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"❌ Error updating quantity: {e}")
            return False
        finally:
            if conn: conn.close()

    @staticmethod
    def add_or_update_item(user_id, product_id, quantity):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            check_sql = "SELECT quantity FROM cart_items WHERE user_id = ? AND product_id = ?"
            cursor.execute(check_sql, (user_id, product_id))
            existing = cursor.fetchone()

            if existing:
                new_qty = existing['quantity'] + quantity
                return CartRepository.update_quantity(user_id, product_id, new_qty)
            else:
                insert_sql = "INSERT INTO cart_items (user_id, product_id, quantity) VALUES (?, ?, ?)"
                cursor.execute(insert_sql, (user_id, product_id, quantity))
                conn.commit()
                return True
        except Exception as e:
            print(f"❌ Error adding item: {e}")
            return False
        finally:
            if conn: conn.close()

    @staticmethod
    def remove_item(user_id, product_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM cart_items WHERE user_id = ? AND product_id = ?"
            cursor.execute(sql, (user_id, product_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error removing item: {e}")
            return False
        finally:
            if conn: conn.close()

    @staticmethod
    def clear_cart(user_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM cart_items WHERE user_id = ?"
            cursor.execute(sql, (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error clearing cart: {e}")
            return False
        finally:
            if conn: conn.close()