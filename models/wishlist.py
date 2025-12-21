from extensions import db
from models.wishlist_item import WishlistItem
from models.shopping_cart import ShoppingCart

class Wishlist:
  def __init__(self, user_id):
    self.user_id = user_id

  def add_product(self, product_id):
    exists = WishlistItem.query.filter_by(user_id=self.user_id, product_id=product_id).first()     
    if not exists:
      new_item = WishlistItem(user_id=self.user_id, product_id=product_id)
      db.session.add(new_item)
      db.session.commit()
      return True, "Product added to wishlist."
    return False, "Product is already in your wishlist."
 
  def remove_product(self, product_id):
    WishlistItem.query.filter_by(user_id=self.user_id, product_id=product_id).delete()
    db.session.commit()

  def move_to_cart(self, product_id):
    # Use ShoppingCart logic to handle stock validation
    cart = ShoppingCart(self.user_id)
    success, message = cart.add_product(product_id)
    if success:
      self.remove_product(product_id)
      return True, "Product moved to cart successfully."
    return False, message
    
  def move_all_to_cart(self):
    items = self.items
    results = []
    for item in items:
      success, message = self.move_to_cart(item.product_id)
      results.append({"product_id": item.product_id, "success": success, "message": message})
    return results

  def clear_wishlist(self):
    WishlistItem.query.filter_by(user_id=self.user_id).delete()
    db.session.commit()

  @property
  def items(self):
    return WishlistItem.query.filter_by(user_id=self.user_id).all()
    
  @property
  def items_count(self):
    return WishlistItem.query.filter_by(user_id=self.user_id).count()

  @property
  def is_empty(self):
    return self.items_count == 0