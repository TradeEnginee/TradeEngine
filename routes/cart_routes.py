from flask import Blueprint, request, jsonify
from Database.Repositories.product_repo import ProductRepository
from models.shopping_cart import ShoppingCart
from models.cart_item import CartItem

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart", methods=["GET"])
@login_required
def view_cart():
    cart = ShoppingCart(current_user.id)
    items = []
    for item in CartItem.query.filter_by(user_id=current_user.id).all():
        items.append({
            "id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "total": item.item_total_price()
        })
        
    return jsonify({
        "items": items,
        "subtotal": cart.calculate_subtotal(),
        "total_quantity": cart.total_quantity
    }), 200

@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    cart = ShoppingCart(current_user.id)
    success, message = cart.add_product(product_id)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400

@cart_bp.route("/cart/clear", methods=["DELETE"])
@login_required
def clear_cart_route():
    cart = ShoppingCart(current_user.id)
    cart.clear_cart()
    return jsonify({"message": "Cart cleared successfully"}), 200