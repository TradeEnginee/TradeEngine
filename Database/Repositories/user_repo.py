import sqlite3
import json
from werkzeug.security import generate_password_hash
# Import the connection function from the db_manager file in the same directory
from Database.db_manager import get_connection

class UserRepository:
    
    # Add New User
    @staticmethod
    def add_user(username, email, password, role="customer", mobile="", specific_info={}):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # 1. Hash the password (Security best practice)
            hashed_pw = generate_password_hash(password)

            # 2. Convert specific info to JSON string (to store in the TEXT column)
            info_json = json.dumps(specific_info)

            # 3. SQL Insert Statement (Using ? placeholders for security)
            sql = """
            INSERT INTO users (username, email, password_hash, role, mobile, specific_info)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(sql, (username, email, hashed_pw, role, mobile, info_json))
            conn.commit()
            print(f"✅ User '{username}' added successfully.")
            return True
            
        except sqlite3.IntegrityError:
            # Handles duplicate Username or Email errors
            print(f"⚠️ Error: User '{username}' or Email '{email}' already exists.")
            return False
        except Exception as e:
            print(f"❌ Error adding user: {e}")
            return False
        finally:
            if conn:
                conn.close()

    # Get User Details Using their Email
    @staticmethod
    def get_user_by_email(email):
        # Function used during Login to fetch user details by email.
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM users WHERE email = ?"
            cursor.execute(sql, (email,))
            user = cursor.fetchone() # Fetch the first matching record
            return user
        except Exception as e:
            print(f"❌ Error fetching user: {e}")
            return None
        finally:
            if conn:
                conn.close()

    # Get User Details Using their Username
    @staticmethod
    def get_user_by_username(username):
        # Function used during Login to fetch user details by email.
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM users WHERE username = ?"
            cursor.execute(sql, (username,))
            user = cursor.fetchone() # Fetch the first matching record
            return user
        except Exception as e:
            print(f"❌ Error fetching user: {e}")
            return None
        finally:
            if conn:
                conn.close()

    # Updating User Details
    @staticmethod
    def update_user(user_id, username=None, email=None, password=None, mobile=None, specific_info=None):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            fields_to_update = []
            values = []

            if username is not None:
                fields_to_update.append("username = ?")
                values.append(username)

            if email is not None:
                fields_to_update.append("email = ?")
                values.append(email)

            if password is not None:
                hashed_pw = generate_password_hash(password)
                fields_to_update.append("password_hash = ?")
                values.append(hashed_pw)

            if mobile is not None:
                fields_to_update.append("mobile = ?")
                values.append(mobile)

            if specific_info is not None:
                info_json = json.dumps(specific_info)
                fields_to_update.append("specific_info = ?")
                values.append(info_json)

            if not fields_to_update:
                return False

            sql = f"UPDATE users SET {', '.join(fields_to_update)} WHERE id = ?"
            values.append(user_id)

            cursor.execute(sql, tuple(values))
            conn.commit()
            print(f"✅ User {user_id} updated successfully.")
            return True

        except sqlite3.IntegrityError:
            print(f"⚠️ Error: Username or Email already exists.")
            return False
        except Exception as e:
            print(f"❌ Error updating user {user_id}: {e}")
            return False
        finally:
            if conn:
                conn.close()
    

    # Deleting User
    @staticmethod
    def delete_user(user_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = "DELETE FROM users WHERE id = ?"
            cursor.execute(sql, (user_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"🗑️ User {user_id} deleted successfully.")
                return True
            else:
                print(f"⚠️ User {user_id} not found.")
                return False
                
        except Exception as e:
            print(f"❌ Error deleting user {user_id}: {e}")
            return False
        finally:
            if conn:
                conn.close()