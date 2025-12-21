from extensions import db
from .cart_item import CartItem
from models.detailed_product import DetailedProduct

class ShoppingCart:
  def __init__(self, user_id):
    self.user_id = user_id
  
  def add_product(self, product_id):
    # Fetch the product from the database to check stock
    product = DetailedProduct.query.get(product_id)
    if not product or product.stock_quantity <= 0:
      return False, "Product is currently out of stock."

    # Check if the product is already in the user's cart
    item = CartItem.query.filter_by(user_id=self.user_id, product_id=product_id).first()
    if item:
      # Check if there is enough stock for an additional unit
      if item.quantity < product.stock_quantity:
        item.increase_quantity()
        product.stock_quantity -= 1 # Deduct from inventory
      else:
        return False, f"Maximum stock reached ({product.stock_quantity} available)."
    else:
      # Create a new cart item and deduct 1 from inventory
      new_item = CartItem(user_id=self.user_id, product_id=product_id, _quantity=1)
      product.stock_quantity -= 1
      db.session.add(new_item)

    db.session.commit()
    return True, "Product successfully added to your cart."

  def remove_product(self, product_id):
    item = CartItem.query.filter_by(user_id=self.user_id, product_id=product_id).first()
    if item:
      product = DetailedProduct.query.get(product_id)
      # Restore the stock quantity
      product.stock_quantity += item.quantity 
      db.session.delete(item)
      db.session.commit()

  def decrease_or_remove(self, product_id):
    item = CartItem.query.filter_by(user_id=self.user_id, product_id=product_id).first()
    if item:
      product = DetailedProduct.query.get(product_id)
      if item.quantity > 1:
        item.decrease_quantity()
        product.stock_quantity += 1 # Restore 1 unit to stock
      else:
        db.session.delete(item)
        product.stock_quantity += 1 # Restore the last unit to stock
      db.session.commit()
    
  def clear_cart(self):
    user_items = CartItem.query.filter_by(user_id=self.user_id).all()
    for item in user_items:
      product = DetailedProduct.query.get(item.product_id)
      if product:
        product.stock_quantity += item.quantity

    CartItem.query.filter_by(user_id=self.user_id).delete()
    db.session.commit()
    
  @property
  def items_count(self):
    return CartItem.query.filter_by(user_id=self.user_id).count()

  @property
  def total_quantity(self):
    user_items = CartItem.query.filter_by(user_id=self.user_id).all()
    total = 0
    for item in user_items:
      total += item.quantity
    return total

  @property
  def is_empty(self):
    return self.items_count == 0

  def calculate_subtotal(self):
    user_items = CartItem.query.filter_by(user_id=self.user_id).all()
    subtotal = 0
    for item in user_items:
      subtotal += item.item_total_price()
    return subtotal