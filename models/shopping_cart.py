from .cart_item import CartItem

class ShoppingCart:
  def __init__(self):
    self.items = []
  
  def add_product(self, product):
    for item in self.items:
      if item.product.id == product.id:
        item.increase_quantity()
        return
    self.items.append(CartItem(product))

  def remove_product(self, product_id):
    new_items = []
    for item in self.items:
      if item.product.id != product_id:
        new_items.append(item)
    self.items = new_items

  def decrease_or_remove(self, product_id):
    for item in self.items:
      if item.product.id == product_id:
        if item.quantity > 1:
          item.decrease_quantity()
        else:
          self.remove_product(product_id)
        break
    
  def clear_cart(self):
    self.items.clear()

  @property
  def items_count(self):
    return len(self.items)

  @property
  def total_quantity(self):
    total = 0
    for item in self.items:
        total += item.quantity
    return total

  @property
  def is_empty(self):
    return len(self.items) == 0

  def calculate_subtotal(self):
    subtotal = 0
    for item in self.items:
      subtotal += item.item_total_price()
    return subtotal