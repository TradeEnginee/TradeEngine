from .wishlist_item import WishlistItem

class Wishlist:
    def __init__(self, user):
        self._user = user
        self._items = []

    @property
    def user(self):
        return self._user

    @property
    def items(self):
        return list(self._items)

    @property
    def items_count(self):
        return len(self._items)

    @property
    def is_empty(self):
        return len(self._items) == 0

    def is_product_in_wishlist(self, product):
        for item in self._items:
            if item.product.id == product.id:
                return True
        return False

    def add_product(self, product):
        if self.is_product_in_wishlist(product):
            return False, f"{product.name} is already in your wishlist."
        
        new_item = WishlistItem(None, self._user, product)
        self._items.append(new_item)
        return True, f"{product.name} added to wishlist successfully."

    def remove_product(self, product):
        for item in self._items:
            if item.product.id == product.id:
                self._items.remove(item)
                return True, f"{product.name} removed from wishlist."
        return False, "Product not found in wishlist."

    def move_to_cart(self, product, shopping_cart):
        if not self.is_product_in_wishlist(product):
            return False, "Product not found in wishlist."
        success, message = shopping_cart.add_product(product, quantity=1)
        
        if success:
            self.remove_product(product)
            return True, f"Moved {product.name} to cart."
        
        return False, message

    def move_all_to_cart(self, shopping_cart):
        results = []
        for item in list(self._items):
            success, message = self.move_to_cart(item.product, shopping_cart)
            results.append({
                "product_id": item.product.id,
                "success": success,
                "message": message
            })
        return results

    def clear_wishlist(self):
        self._items = []
        return True, "Wishlist cleared successfully."

    def to_dict(self):
        return {
            "user": self._user.username,
            "items": [item.to_dict() for item in self._items],
            "items_count": self.items_count
        }

    def __repr__(self):
        return f"<Wishlist of {self._user.username}: {self.items_count} items>"