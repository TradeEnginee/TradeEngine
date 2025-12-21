from extensions import db

class CartItem(db.Model):
  __tablename__ = 'cart_items' 
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
  _quantity = db.Column('quantity', db.Integer, db.CheckConstraint('quantity > 0'), default=1)
  product = db.relationship("Product")

  def __init__(self, user_id, product_id, quantity=1):
    self.user_id = user_id
    self.product_id = product_id
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
    