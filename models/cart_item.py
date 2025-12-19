class CartItem:
  def __init__(self, product, quantity=1):
    self.product = product
    self._quantity = quantity

  @property
  def quantity(self):
    return self._quantity

  def increase_quantity(self):
    self._quantity += 1

  def decrease_quantity(self):
    if self._quantity > 1:
      self._quantity -= 1

  def item_total_price(self):
    return self.product.price * self._quantity
    