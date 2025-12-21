from flask import Blueprint, request, jsonify
from Database.Repositories.product_repo import ProductRepository
from models.shopping_cart import ShoppingCart

cart_bp = Blueprint("cart", __name__)
cart = ShoppingCart()

@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = ProductRepository.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    cart.add_product(product)
    return jsonify({"message": "Product added to cart"}), 200

@cart_bp.route("/cart", methods=["GET"])
def view_cart():
    items = []
    for item in cart.items:
        items.append({
            "id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "total": item.item_total_price()
        })
    return jsonify({
        "items": items,
        "subtotal": cart.calculate_subtotal()
    })

@cart_bp.route("/cart/clear", methods=["DELETE"])
def clear_cart_route():
    cart.clear_cart()
    return jsonify({"message": "Cart cleared"}), 200