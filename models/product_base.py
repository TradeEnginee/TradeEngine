from abc import ABC, abstractmethod

class Product(ABC):
    next_id = 1
    def __init__(self, name, price, image_url, category):
       allowed_categories = ["Cosmetics", "Electronics", "Food", "Clothes", "Sports"]
       if category not in allowed_categories:
              raise ValueError(f"Category '{category}' is not allowed. Choose from {allowed_categories}.")  
       self.id = Product.next_id
       Product.next_id += 1
       self.name = name
       self.price = price
       self.image_url = image_url
       self.category = category
    @abstractmethod
    def get_details(self):
           pass