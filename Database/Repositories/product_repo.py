import sqlite3
import json
from Database.db_manager import get_connection
from models.product_model import Product


ALLOWED_SORT_COLUMNS = ["price", "name", "created_at", "stock_quantity"]
ALLOWED_SORT_TYPES = ["ASC", "DESC"]

class ProductRepository:

    # =========================================================
    # Helper: Convert a Row into an Object
    # =========================================================
    @staticmethod
    def _map_row_to_object(row):
        if not row:
            return None
        return Product(
            id=row['id'],
            name=row['name'],
            price=row['price'],
            image_url=row['image_url'],
            category=row['category'],
            stock_quantity=row['stock_quantity'],
            details=row['details'],  
            created_at=row['created_at']
        )

    # =========================================================
    # Create: Add a Product (Using an Object)
    # =========================================================
    @staticmethod
    def add_product(product_object):
       
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            
            details_json = json.dumps(product_object.details) if product_object.details else "{}"

            sql = """
            INSERT INTO products (name, price, image_url, category, stock_quantity, details)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            
            cursor.execute(sql, (
                product_object.name, 
                product_object.price, 
                product_object.image_url, 
                product_object.category, 
                product_object.stock_quantity, 
                details_json
            ))

            conn.commit()
            print(f" Product '{product_object.name}' added successfully.")
            return True
            
        except Exception as e:
            print(f" Error adding Product: {e}")
            return False
        finally:
            if conn: conn.close()

    # =========================================================
    # Read: Fetch All Products (With Sorting Support)
    # =========================================================
    @staticmethod
    def get_all_products(ordered_by="created_at", sort_type="DESC"):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
    
            if ordered_by not in ALLOWED_SORT_COLUMNS: ordered_by = "created_at"
            if sort_type not in ALLOWED_SORT_TYPES: sort_type = "DESC"
            
            
            sql = f"SELECT * FROM products ORDER BY category ASC, {ordered_by} {sort_type}"
            
            cursor.execute(sql)
            rows = cursor.fetchall()
            return [ProductRepository._map_row_to_object(row) for row in rows]
            
        except Exception as e:
            print(f" Error fetching products: {e}")
            return []
        finally:
            if conn: conn.close()

    # =========================================================
    # Read: Fetch Products from a Specific Category (With Sorting Support)
    # =========================================================
    @staticmethod
    def get_products_by_category(category, ordered_by="created_at", sort_type="DESC"):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
        
            if ordered_by not in ALLOWED_SORT_COLUMNS: ordered_by = "created_at"
            if sort_type not in ALLOWED_SORT_TYPES: sort_type = "DESC"

    
            sql = f"SELECT * FROM products WHERE category = ? ORDER BY {ordered_by} {sort_type}"
            
            cursor.execute(sql, (category,))
            rows = cursor.fetchall()
            return [ProductRepository._map_row_to_object(row) for row in rows]
        except Exception as e:
            print(f" Error fetching category {category}: {e}")
            return []
        finally:
            if conn: conn.close()

    # =========================================================
    # Search: Search for a Product by Name (New)
    # =========================================================
    @staticmethod
    def search_products(query):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
        
            sql = "SELECT * FROM products WHERE name LIKE ? ORDER BY price ASC"
            cursor.execute(sql, (f'%{query}%',))
            rows = cursor.fetchall()
            return [ProductRepository._map_row_to_object(row) for row in rows]
        except Exception as e:
            print(f" Error searching for {query}: {e}")
            return []
        finally:
            if conn: conn.close()

    # =========================================================
    # Read: Fetch a Single Product by ID
    # =========================================================
    @staticmethod
    def get_product_by_id(product_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM products WHERE id = ?"
            cursor.execute(sql, (product_id,))
            row = cursor.fetchone()
            return ProductRepository._map_row_to_object(row)
        except Exception as e:
            print(f" Error fetching product {product_id}: {e}")
            return


    # =========================================================
    # Update: Edit Product Details (With Protection Against Negative Values )
    # =========================================================
    @staticmethod
    def update_product(product_id, name=None, price=None, image_url=None, category=None, stock_quantity=None, details_dict=None):
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
                if float(price) < 0:
                    print(" Update Rejected: Price cannot be negative.")
                    return False
                fields_to_update.append("price = ?")
                values.append(price)
            
            if image_url is not None:
                fields_to_update.append("image_url = ?")
                values.append(image_url)

            if category is not None:
                fields_to_update.append("category = ?")
                values.append(category)

            
            if stock_quantity is not None:
                if int(stock_quantity) < 0:
                    print(" Update Rejected: Stock cannot be negative.")
                    return False
                fields_to_update.append("stock_quantity = ?")
                values.append(stock_quantity)

            
            if details_dict is not None:
                details_json = json.dumps(details_dict)
                fields_to_update.append("details = ?")
                values.append(details_json)

            if not fields_to_update:
                return False 

            sql = f"UPDATE products SET {', '.join(fields_to_update)} WHERE id = ?"
            values.append(product_id)

            cursor.execute(sql, tuple(values))
            conn.commit()
            print(f" Product {product_id} updated successfully.")
            return True

        except Exception as e:
            print(f" Error updating product {product_id}: {e}")
            return False
        finally:
            if conn: conn.close()

    # =========================================================
    # Delete: Remove Product
    # =========================================================
    @staticmethod
    def delete_product(product_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            sql = "DELETE FROM products WHERE id = ?"
            cursor.execute(sql, (product_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f" Product {product_id} deleted.")
                return True
            else:
                print(f" Product {product_id} not found.")
                return False
                
        except Exception as e:
            print(f" Error deleting product: {e}")
            return False
        finally:
            if conn: conn.close()