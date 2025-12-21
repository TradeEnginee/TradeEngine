from flask import Blueprint, jsonify
from Database.Repositories.product_repo import ProductRepository
from models.wishlist import Wishlist
from models.shopping_cart import ShoppingCart

wishlist_bp = Blueprint("wishlist", __name__)
wishlist = Wishlist()
cart = ShoppingCart()

@wishlist_bp.route("/wishlist/add/<int:product_id>", methods=["POST"])
def add_to_wishlist(product_id):
    product = ProductRepository.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    wishlist.add_product(product)
    return jsonify({"message": "Product added to wishlist"}), 200

@wishlist_bp.route("/wishlist", methods=["GET"])
def view_wishlist():
    products = []
    for product in wishlist.products:
        products.append({
            "id": product.id,
            "name": product.name,
            "price": product.price
        })
    return jsonify({
        "items": products,
        "items_count": wishlist.items_count
    })

@wishlist_bp.route("/wishlist/remove/<int:product_id>", methods=["DELETE"])
def remove_from_wishlist(product_id):
    wishlist.remove_product(product_id)
    return jsonify({"message": "Product removed from wishlist"}), 200

@wishlist_bp.route("/wishlist/move-to-cart/<int:product_id>", methods=["POST"])
def move_to_cart(product_id):
    wishlist.move_to_cart(product_id, cart)
    return jsonify({"message": "Product moved to cart"}), 200

@wishlist_bp.route("/wishlist/clear", methods=["DELETE"])
def clear_wishlist():
    wishlist.clear_wishlist()
    return jsonify({"message": "Wishlist cleared"}), 200