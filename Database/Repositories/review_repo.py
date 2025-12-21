import sqlite3
from Database.db_manager import get_connection

class ReviewRepository:
    
    @staticmethod
    def add_review(user_id, product_id, rating, comment=""):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            if not (1 <= rating <= 5):
                print("⚠️ Rating must be between 1 and 5.")
                return False

            sql = """
            INSERT INTO reviews (user_id, product_id, rating, comment)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(sql, (user_id, product_id, rating, comment))
            conn.commit()
            print(f"✅ Review added for product {product_id}.")
            return True
            
        except Exception as e:
            print(f"❌ Error adding review: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_product_reviews(product_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = """
            SELECT r.rating, r.comment, r.created_at, u.username 
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.product_id = ?
            ORDER BY r.created_at DESC
            """
            cursor.execute(sql, (product_id,))
            reviews = cursor.fetchall()
            return reviews
        except Exception as e:
            print(f"❌ Error fetching reviews: {e}")
            return []
        finally:
            if conn:
                conn.close()