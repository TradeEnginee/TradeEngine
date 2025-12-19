import json

class User:
    def __init__(self, id, username, email, password_hash, role, mobile):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.mobile = mobile

    def get_id(self):
        return str(self.id)
    
    def is_admin(self):
        return False

class Customer(User):
    def __init__(self, id, username, email, password_hash, role, mobile, specific_info_json):
        super().__init__(id, username, email, password_hash, role, mobile)
        
        info = json.loads(specific_info_json) if specific_info_json else {}
        self.address = info.get('address', 'No Address')

    def can_buy(self):
        return True

class Admin(User):
    def __init__(self, id, username, email, password_hash, role, mobile, specific_info_json):
        super().__init__(id, username, email, password_hash, role, mobile)
        
        info = json.loads(specific_info_json) if specific_info_json else {}
        self.department = info.get('department', 'General')

    # Override
    def is_admin(self):
        return True