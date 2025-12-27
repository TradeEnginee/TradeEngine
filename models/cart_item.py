class CartItem:

    def __init__(self, item_id, user, product, quantity=1):
        self._item_id = item_id
        self._user = user
        self._product = product
        self.quantity = quantity

    @property
    def product(self):
        return self._product

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Quantity must be an integer and at least 1")
        self._quantity = value

    def increase(self):
        self.quantity += 1

    def decrease(self):
        self.quantity -= 1

    @property
    def item_total_price(self):
        return self._product.price * self.quantity

    def to_dict(self):
        return {
            "item_id": self._item_id,
            "user_id": self._user.id,
            "product_name": self._product.name,
            "quantity": self.quantity,
            "item_total_price": self.item_total_price
        }

    def __repr__(self):
        return f"<CartItem ID {self._item_id}: {self._product.name} (Qty: {self.quantity})>"