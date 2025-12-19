import re
from werkzeug.security import generate_password_hash, check_password_hash
import json

class User:
    def __init__(self, id, username, email, password_hash, role, mobile):
        self.id = id
        self.username = username
        self.role = role
        self.mobile = mobile
        
        self.email = email 
        
        self.__password_hash = password_hash

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        if not User.validate_email_format(new_email):
            raise ValueError(f"❌ Invalid email format: '{new_email}'")
        self._email = new_email


    def is_admin(self):
        return False
    
    @staticmethod
    def validate_password_strength(plain_password):
        if not (8 <= len(plain_password) <= 24):
            return False, "Password length must be between 8 and 24 characters."
        if not re.search(r"[A-Z]", plain_password):
            return False, "Password must contain at least one uppercase letter (A-Z)."
        if not re.search(r"[a-z]", plain_password):
            return False, "Password must contain at least one lowercase letter (a-z)."
        if not re.search(r"\d", plain_password):
            return False, "Password must contain at least one number (0-9)."
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", plain_password):
            return False, "Password must contain at least one special character (!@#$%)."
        return True, "Valid"

    @staticmethod
    def validate_email_format(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(pattern, email):
            return True
        return False

    @property
    def password(self):
        raise AttributeError("❌ Password is not a readable attribute!")

    @password.setter
    def password(self, plain_password):
        is_valid, message = User.validate_password_strength(plain_password)
        if not is_valid:
            raise ValueError(f"⚠️ Weak Password: {message}")
        self.__password_hash = generate_password_hash(plain_password)

    def get_password_hash(self):
        return self.__password_hash

    def verify_password(self, plain_password):
        return check_password_hash(self.__password_hash, plain_password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "mobile": self.mobile
        }
    def __repr__(self):
        return f"<User {self.id}: {self.username} ({self.role})>"

class Customer(User):
    def __init__(self, id, username, email, password_hash, mobile, specific_info_json):
        super().__init__(id, username, email, password_hash, "customer", mobile)
        
        info = json.loads(specific_info_json) if specific_info_json else {}
        self.address = info.get('address', 'No Address')
        self.loyalty_points = info.get('loyalty_points', 0)

    def can_buy(self):
        return True
    
    def to_dict(self):
        data = super().to_dict()
        data['address'] = self.address
        data['loyalty_points'] = self.loyalty_points
        return data

class Admin(User):
    def __init__(self, id, username, email, password_hash, mobile, specific_info_json):
        super().__init__(id, username, email, password_hash, "admin", mobile)
        
        info = json.loads(specific_info_json) if specific_info_json else {}
        self.department = info.get('department', 'General')
    
    # Override
    def is_admin(self):
        return True

    def to_dict(self):
        data = super().to_dict()
        data['department'] = self.department
        return data