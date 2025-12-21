from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models.wishlist import Wishlist

wishlist_bp = Blueprint("wishlist", __name__)

@wishlist_bp.route("/wishlist", methods=["GET"])
@login_required
def view_wishlist():
    wishlist = Wishlist(current_user.id)
    products = []
    for item in wishlist.items:
        products.append({
            "id": item.product.id,
            "name": item.product.name,
            "price": item.product.price,
            "image": item.product.image_url
        })
        
    return jsonify({
        "items": products,
        "items_count": wishlist.items_count
    }), 200

@wishlist_bp.route("/wishlist/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_wishlist(product_id):
    wishlist = Wishlist(current_user.id)
    success, message = wishlist.add_product(product_id)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 200

@wishlist_bp.route("/wishlist/remove/<int:product_id>", methods=["DELETE"])
@login_required
def remove_from_wishlist(product_id):
    wishlist = Wishlist(current_user.id)
    wishlist.remove_product(product_id)
    return jsonify({"message": "Product removed from wishlist"}), 200

@wishlist_bp.route("/wishlist/move-to-cart/<int:product_id>", methods=["POST"])
@login_required
def move_to_cart(product_id):
    wishlist = Wishlist(current_user.id)
    # The wishlist model handles the ShoppingCart and Stock check internally
    success, message = wishlist.move_to_cart(product_id)
    if success:
        return jsonify({"message": message}), 200
    else:
        # Returns an error if the item is Out of Stock
        return jsonify({"error": message}), 400

@wishlist_bp.route("/wishlist/move-all", methods=["POST"])
@login_required
def move_all_to_cart():
    wishlist = Wishlist(current_user.id)
    results = wishlist.move_all_to_cart()
    return jsonify({
        "message": "Bulk move processed",
        "details": results
    }), 200

@wishlist_bp.route("/wishlist/clear", methods=["DELETE"])
@login_required
def clear_wishlist():
    wishlist = Wishlist(current_user.id)
    wishlist.clear_wishlist()
    return jsonify({"message": "Wishlist cleared"}), 200