from .cart_item import CartItem

class ShoppingCart:
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
    def is_empty(self):
        return len(self._items) == 0

    @property
    def items_count(self):
        return len(self._items)

    @property
    def total_quantity(self):
        total = 0
        for item in self._items:
            total += item.quantity
        return total

    @property
    def subtotal(self):
        total = 0
        for item in self._items:
            total += item.item_total_price
        return total

    def _check_stock_availability(self, product, requested_quantity):
        if not product.is_in_stock():
            return False, f"Sorry, {product.name} is out of stock."

        if product.stock_quantity < requested_quantity:
            return False, f"Only {product.stock_quantity} units of {product.name} available."

        return True, "Stock available."

    def get_item_by_product(self, product):
        for item in self._items:
            if item.product.id == product.id:
                return item
        return None

    def add_product(self, product, quantity=1):
        item = self.get_item_by_product(product)
        requested_total = (item.quantity + quantity) if item else quantity
        is_available, message = self._check_stock_availability(product, requested_total)
        if not is_available:
            return False, message

        if item:
            item.quantity += quantity
        else:
            new_item = CartItem(None, self._user, product, quantity) 
            self._items.append(new_item)
        return True, "Product added to cart."

    def update_quantity(self, product, new_quantity):
        item = self.get_item_by_product(product)
        if not item:
            return False, "Item not found in cart."
        is_available, message = self._check_stock_availability(product, new_quantity)
        if not is_available:
            return False, message

        try:
            item.quantity = new_quantity
            return True, "Quantity updated successfully."
        except ValueError as e:
            return False, str(e)

    def decrease_or_remove(self, product):
        item = self.get_item_by_product(product)
        if not item:
            return False, "Item not found."

        if item.quantity > 1:
            item.decrease()
        else:
            self.remove_product(product)

        return True, "Cart updated."
    
    def remove_product(self, product):
        item = self.get_item_by_product(product)
        if not item:
            return False, "Item not found."

        self._items.remove(item)
        return True, "Item removed from cart."

    def clear_cart(self):
        self._items = []

    def to_dict(self):
        items_list = []
        for item in self._items:
            items_list.append(item.to_dict())

        return {
            "user": self._user.username,
            "items": items_list,
            "items_count": self.items_count,
            "total_quantity": self.total_quantity,
            "subtotal": self.subtotal
        }
    
    def __repr__(self):
        return f"<ShoppingCart of {self._user.username}: {self.items_count} items, Subtotal: ${self.subtotal:,.2f}>"