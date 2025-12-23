import json

class Product:
    def __init__(self, id, name, price, image_url, category, stock_quantity, details, created_at=None):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.category = category
        self.created_at = created_at
        
        
        self.price = price 
        self.stock_quantity = stock_quantity
        
       
        if isinstance(details, str) and details.strip():
            try:
                self.details = json.loads(details)
            except json.JSONDecodeError:
                self.details = {}
        elif isinstance(details, dict):
            self.details = details
        else:
            self.details = {}

    # ==========================
    # Properties & Validation
    # ==========================

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        try:
            val = float(value)
            if val < 0:
                raise ValueError("Price cannot be negative.")
            self._price = val
        except ValueError:
            raise ValueError("Price must be a valid number.")

    @property
    def stock_quantity(self):
        return self._stock_quantity

    @stock_quantity.setter
    def stock_quantity(self, value):
        try:
            val = int(value)
            if val < 0:
                raise ValueError("Stock quantity cannot be negative.")
            self._stock_quantity = val
        except ValueError:
            raise ValueError("Stock quantity must be an integer.")

    # ==========================
    # Logic Methods
    # ==========================

    def is_in_stock(self):
        return self._stock_quantity > 0

    def reduce_stock(self, amount=1):
        if amount > self._stock_quantity:
            return False 
        self.stock_quantity -= amount 
        return True

    def get_display_price(self):
        return f"${self._price:,.2f}"

    # ==========================
    #  Serialization 
    # ==========================
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self._price,
            "image_url": self.image_url,
            "category": self.category,
            "stock_quantity": self._stock_quantity,
            "details": self.details,
            "created_at": self.created_at
        }

    def __repr__(self):
        return f"<Product {self.id}: {self.name} (${self._price})>"