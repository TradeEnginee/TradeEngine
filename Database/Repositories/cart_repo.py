import sqlite3
from Database.db_manager import get_connection
from models.shopping_cart import ShoppingCart
from models.cart_item import CartItem
from Database.Repositories.product_repo import ProductRepository

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
            
            # 1. Check Product Stock
            product = ProductRepository.get_product_by_id(product_id)
            if not product:
                print("❌ Product not found.")
                return False
                
            # 2. Check Existing Cart Quantity
            check_sql = "SELECT quantity FROM cart_items WHERE user_id = ? AND product_id = ?"
            cursor.execute(check_sql, (user_id, product_id))
            existing = cursor.fetchone()
            
            # Calculate Projected Total
            current_cart_qty = existing['quantity'] if existing else 0
            new_total_qty = current_cart_qty + quantity
            
            # 3. Validate Stock
            if new_total_qty > product.stock_quantity:
                print(f"❌ Insufficient stock. Requested: {new_total_qty}, Available: {product.stock_quantity}")
                return False

            # 4. Proceed to Update or Insert
            if existing:
                return CartRepository.update_quantity(user_id, product_id, new_total_qty)
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