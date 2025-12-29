import sqlite3
import json
from werkzeug.security import generate_password_hash
from Database.db_manager import get_connection
from models.user_model import User, Customer, Admin

class UserRepository:
    
    @staticmethod
    def _map_row_to_object(row):
        if not row:
            return None
        
        u_id = row['id']
        name = row['username']
        email = row['email']
        pw = row['password_hash']
        role = row['role']
        mob = row['mobile']
        info = row['specific_info']


        if role == 'admin':
            return Admin(u_id, name, email, pw, mob, info)
        elif role == 'customer':
            return Customer(u_id, name, email, pw, mob, info)
        else:
            return User(u_id, name, email, pw, role, mob)


    @staticmethod
    def add_user(user_object):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            info_dict = {}
            
            if isinstance(user_object, Customer):
                info_dict = {
                    'address': user_object.address,
                    'loyalty_points': getattr(user_object, 'loyalty_points', 0)
                }
            elif isinstance(user_object, Admin):
                info_dict = {
                    'department': user_object.department
                }
            
            info_json = json.dumps(info_dict)

            sql = """
            INSERT INTO users (username, email, password_hash, role, mobile, specific_info)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(sql, (
                user_object.username,
                user_object.email,
                user_object.get_password_hash(), 
                user_object.role,
                user_object.mobile,
                info_json
            ))
            
            conn.commit()
            print(f"✅ User '{user_object.username}' added successfully.")
            return True
            
        except sqlite3.IntegrityError:
            print(f"⚠️ Error: User '{user_object.username}' or Email already exists.")
            return False
        except Exception as e:
            print(f"❌ Error adding user: {e}")
            return False
        finally:
            if conn:
                conn.close()


    @staticmethod
    def get_user_by_email(email):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM users WHERE email = ?"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
            return UserRepository._map_row_to_object(user)
        except Exception as e:
            print(f"❌ Error fetching user: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_user_by_username(username):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM users WHERE username = ?"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            return UserRepository._map_row_to_object(user)
        except Exception as e:
            print(f"❌ Error fetching user: {e}")
            return None
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            sql = "SELECT * FROM users WHERE id = ?"
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()
            return UserRepository._map_row_to_object(user)
        except Exception as e:
            print(f"❌ Error fetching user: {e}")
            return None
        finally:
            if conn:
                conn.close()


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