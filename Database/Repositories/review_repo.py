import sqlite3
from Database.db_manager import get_connection
from models.review_model import Review

class ReviewRepository:

    @staticmethod
    def _map_row_to_object(row):
        if not row:
            return None
        
        return Review(
            review_id=row["id"],
            user_id=row["user_id"],
            product_id=row["product_id"],
            rating=row["rating"],
            comment=row["comment"],
            created_at=row["created_at"],
            username=row.get("username")  
        )

    # =========================
    # Add Review
    # =========================
    @staticmethod
    def add_review(review: Review):
        conn = None
        try:
            if not (1 <= review.rating <= 5):
                print("⚠️ Rating must be between 1 and 5.")
                return False

            conn = get_connection()
            cursor = conn.cursor()

            sql = """
            INSERT INTO reviews (user_id, product_id, rating, comment)
            VALUES (?, ?, ?, ?)
            """

            cursor.execute(sql, (
                review.user_id,
                review.product_id,
                review.rating,
                review.comment
            ))

            conn.commit()
            print(f"✅ Review added for product {review.product_id}.")
            return True

        except Exception as e:
            print(f"❌ Error adding review: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # =========================
    # Get Reviews For Product
    # =========================
    @staticmethod
    def get_reviews_by_product(product_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            sql = """
            SELECT r.*, u.username
            FROM reviews r
            JOIN users u ON r.user_id = u.id
            WHERE r.product_id = ?
            ORDER BY r.created_at DESC
            """

            cursor.execute(sql, (product_id,))
            rows = cursor.fetchall()

            return [ReviewRepository._map_row_to_object(row) for row in rows]

        except Exception as e:
            print(f"❌ Error fetching reviews: {e}")
            return []
        finally:
            if conn:
                conn.close()

    # =========================
    # Delete Review
    # =========================
    @staticmethod
    def delete_review(review_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            sql = "DELETE FROM reviews WHERE id = ?"
            cursor.execute(sql, (review_id,))
            conn.commit()

            if cursor.rowcount > 0:
                print(f"🗑️ Review {review_id} deleted successfully.")
                return True
            else:
                print("⚠️ Review not found.")
                return False

        except Exception as e:
            print(f"❌ Error deleting review: {e}")
            return False
        finally:
            if conn:
                conn.close()
