class Wishlist:
  def __init__(self):
    self.products = []

  def add_product(self, product):
    if product not in self.products:
      self.products.append(product)
 
  def remove_product(self, product_id):
    new_products = []
    for product in self.products:
      if product.id != product_id:
        new_products.append(product)

    self.products = new_products

  def move_to_cart(self, product_id, cart):
    for product in self.products:
      if product.id == product_id:
        cart.add_product(product)
        self.remove_product(product_id)
        break