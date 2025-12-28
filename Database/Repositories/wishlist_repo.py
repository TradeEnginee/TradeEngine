import sqlite3
from Database.db_manager import get_connection
from Database.Repositories.product_repo import ProductRepository
from models.wishlist import Wishlist, WishlistItem

class WishlistRepository:
    @staticmethod
    def _map_row_to_object(row, user_object):
        if not row:
            return None      
        product = ProductRepository.get_product_by_id(row['product_id'])
        
        if product:
            return WishlistItem(
                item_id=row['id'],
                user=user_object,
                product=product
            )
        return None

    @staticmethod
    def get_wishlist_by_user(user_object):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM wishlist_items WHERE user_id = ?"
            cursor.execute(sql, (user_object.id,))
            rows = cursor.fetchall()
            
            wishlist = Wishlist(user_object)
            for row in rows:
                item = WishlistRepository._map_row_to_object(row, user_object)
                if item:
                    wishlist._items.append(item)     
            return wishlist

        except Exception as e:
            print(f"❌ Error fetching wishlist: {e}")
            return None
        finally:
            if conn: conn.close()

    @staticmethod
    def add_item(user_id, product_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "INSERT INTO wishlist_items (user_id, product_id) VALUES (?, ?)"
            cursor.execute(sql, (user_id, product_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"❌ Error adding item to wishlist: {e}")
            return False
        finally:
            if conn: conn.close()

    @staticmethod
    def remove_item(user_id, product_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM wishlist_items WHERE user_id = ? AND product_id = ?"
            cursor.execute(sql, (user_id, product_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"❌ Error removing item from wishlist: {e}")
            return False
        finally:
            if conn: conn.close()

    @staticmethod
    def clear_wishlist(user_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM wishlist_items WHERE user_id = ?"
            cursor.execute(sql, (user_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Error clearing wishlist: {e}")
            return False
        finally:
            if conn: conn.close()