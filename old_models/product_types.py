from .product_base import Product

class CosmeticsProduct(Product):
    def __init__(self, name, price, image_url, category, brand, skin_type):
        super().__init__(name, price, image_url, category)
        self.brand = brand
        self.skin_type = skin_type
    
    def get_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image_url": self.image_url,
            "category": self.category,
            "brand": self.brand,
            "skin_type": self.skin_type
        }

class ElectronicProduct(Product):
    def __init__(self, name, price, image_url, category, brand, warranty_years):
        super().__init__(name, price, image_url, category)
        self.brand = brand
        self.warranty_years = warranty_years
    
    def get_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image_url": self.image_url,
            "category": self.category,
            "brand": self.brand,
            "warranty_years": self.warranty_years
        }

class FoodProduct(Product):
    def __init__(self, name, price, image_url, category, expiry_date):
        super().__init__(name, price, image_url, category)
        self.expiry_date = expiry_date
    
    def get_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image_url": self.image_url,
            "category": self.category,
            "expiry_date": self.expiry_date
        }

class ClothesProduct(Product):
    def __init__(self, name, price, image_url, category, brand, size):
        super().__init__(name, price, image_url, category)
        self.brand = brand
        self.size = size
    
    def get_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image_url": self.image_url,
            "category": self.category,
            "brand": self.brand,
            "size": self.size
        }

class SportsProduct(Product):
    def __init__(self, name, price, image_url, category, material, sport_type):
        super().__init__(name, price, image_url, category)
        self.material = material
        self.sport_type = sport_type
    
    def get_details(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "image_url": self.image_url,
            "category": self.category,
            "material": self.material,
            "sport_type": self.sport_type
        }