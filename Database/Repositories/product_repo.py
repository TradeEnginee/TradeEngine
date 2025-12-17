import sqlite3
from ..db_manager import get_connection
import json
allowed_columns = ["price", "name", "created_at", "stock_quantity"]
sort_types = ["ASC", "DESC"]

class ProductRepository:

    @staticmethod
    def add_product(name, price, image_url, category, stock_quantity, details):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            details_json = json.dumps(details)

            sql = """
            INSERT INTO PRODUCTS (name, price, image_url, category, stock_quantity, details)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql, (name, price, image_url, category, stock_quantity, details_json))

            conn.commit()
            print(f"✅ Product '{name}' added successfully.")
            return True
        except Exception as e:
            print(f"❌ Error adding Product: {e}")
            return False
        finally:
            if conn:
                conn.close()


    @staticmethod
    def get_all_products(ordered_by, sort_type):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = f"SELECT * FROM products ORDER BY {ordered_by} {sort_type}" if ordered_by in allowed_columns and sort_type in sort_types else "SELECT * FROM products ORDER BY created_at DESC"
            cursor.execute(sql)
            products = cursor.fetchall()
            return products
        except Exception as e:
            print(f"❌ Error fetching products: {e}")
            return []
        finally:
            if conn:
                conn.close()

    # Get Product by Category
    @staticmethod
    def get_products_by_category(category, ordered_by, sort_type):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = f"SELECT * FROM products WHERE category = ? ORDER BY {ordered_by} {sort_type}" if ordered_by in allowed_columns and sort_type in sort_types else "SELECT * FROM products WHERE category = ? ORDER BY created_at DESC"
            cursor.execute(sql, (category,))
            products = cursor.fetchall()
            return products
        except Exception as e:
            print(f"❌ Error fetching category {category}: {e}")
            return []
        finally:
            if conn:
                conn.close()
    @staticmethod
    def get_product_by_id(product_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM products WHERE id = ?"
            cursor.execute(sql, (product_id,))
            product = cursor.fetchone()
            return product
        except Exception as e:
            print(f"❌ Error fetching product {product_id}: {e}")
            return None
        finally:
            if conn:
                conn.close()

    # Update Product
    @staticmethod
    def update_product(product_id, name=None, price=None, image_url=None, category=None, stock_quantity=None, details=None):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            fields_to_update = []
            values = []

            if name is not None:
                fields_to_update.append("name = ?")
                values.append(name)
            
            if price is not None:
                fields_to_update.append("price = ?")
                values.append(price)
            
            if image_url is not None:
                fields_to_update.append("image_url = ?")
                values.append(image_url)

            if category is not None:
                fields_to_update.append("category = ?")
                values.append(category)

            if stock_quantity is not None:
                fields_to_update.append("stock_quantity = ?")
                values.append(stock_quantity)

            if details is not None:
                details_json = json.dumps(details)
                fields_to_update.append("details = ?")
                values.append(details_json)

            if not fields_to_update:
                print("⚠️ No fields to update.")
                return False

            sql = f"UPDATE products SET {', '.join(fields_to_update)} WHERE id = ?"
            
            values.append(product_id)

            cursor.execute(sql, tuple(values))
            conn.commit()
            print(f"✅ Product {product_id} updated successfully.")
            return True

        except Exception as e:
            print(f"❌ Error updating product {product_id}: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete_product(product_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = "DELETE FROM products WHERE id = ?"
            cursor.execute(sql, (product_id,))
            conn.commit()
            print(f"🗑️ Product {product_id} deleted.")
            return True
        except Exception as e:
            print(f"❌ Error deleting product: {e}")
            return False
        finally:
            if conn:
                conn.close()