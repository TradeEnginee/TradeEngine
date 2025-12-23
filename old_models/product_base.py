from abc import ABC, abstractmethod

class Product(ABC):
    next_id = 1
    
    def __init__(self, name, price, image_url, category):

        self._id = Product.next_id
        Product.next_id += 1
        
        self._name = name      
        self._price = price      
        self._image_url = image_url
        self._category = category
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @property
    def image_url(self):
        return self._image_url
    
    @property
    def category(self):
        return self._category
    
    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Name must be a non-empty string")
        self._name = value
    
    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number")
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value
    
    @category.setter 
    def category(self, value):
        allowed_categories = ["Cosmetics", "Electronics", "Food", "Clothes", "Sports"]
        if value not in allowed_categories:
            raise ValueError(f"Category must be one of: {allowed_categories}")
        self._category = value
    
    @abstractmethod
    def get_details(self):
        pass
    def __repr__(self):
        return str(self.get_details())

    def __getitem__(self, key):
        return self.get_details()[key]
    