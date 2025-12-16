from .product_base import Product
from .review_system import ReviewSystem

class DetailedProduct(Product):
    def __init__(self, name, price, image_url, category, stock_quantity=10):
        super().__init__(name, price, image_url, category)
        if not isinstance(stock_quantity, int) or stock_quantity < 0:
            raise ValueError("Stock must be non-negative integer")
        self._stock_quantity = stock_quantity
        self._reviews = ReviewSystem()

    @property
    def stock_quantity(self):
        return self._stock_quantity

    @property
    def reviews(self):
        return self._reviews

    def get_stock_status(self):
        if self._stock_quantity == 0:
            return "Out of stock"
        elif self._stock_quantity <= 5:
            return f"Only {self._stock_quantity} left in stock!"
        return "In stock"

    def get_full_details(self):
        base = self.get_details()
        base["stock_status"] = self.get_stock_status()
        base["average_rating"] = self._reviews.get_average_rating()
        base["review_count"] = self._reviews.get_review_count()
        return base