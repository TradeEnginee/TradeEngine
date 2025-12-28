class WishlistItem:
    def __init__(self, item_id, user, product):
        self._item_id = item_id
        self._user = user
        self._product = product

    @property
    def product(self):
        return self._product

    @property
    def user(self):
        return self._user

    def to_dict(self):
        return {
            "item_id": self._item_id,
            "product_name": self._product.name,
            "product_price": self._product.price
        }

    def __repr__(self):
        return f"<WishlistItem: {self._product.name}>"