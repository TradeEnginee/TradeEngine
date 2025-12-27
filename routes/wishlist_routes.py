from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Database.Repositories.wishlist_repo import WishlistRepository
from Database.Repositories.cart_repo import CartRepository
from Database.Repositories.user_repo import UserRepository

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/wishlist')
def view_wishlist():
    if 'user_id' not in session:
        flash("Please login to view your wishlist.", "error")
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    user = UserRepository.get_user_by_id(user_id)
    wishlist = WishlistRepository.get_wishlist_by_user(user)
    return render_template('wishlist.html', wishlist=wishlist)

@wishlist_bp.route('/wishlist/add/<int:product_id>')
def add_to_wishlist(product_id):
    if 'user_id' not in session:
        flash("Please login to add items to wishlist.", "error")
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')    
    if WishlistRepository.add_item(user_id, product_id):
        flash("Product added to wishlist!", "success")
    else:
        flash("Product is already in your wishlist.", "info")       
    return redirect(request.referrer or url_for('wishlist.view_wishlist'))

@wishlist_bp.route('/wishlist/remove/<int:product_id>')
def remove_from_wishlist(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    if WishlistRepository.remove_item(user_id, product_id):
        flash("Item removed from wishlist.", "success")
    else:
        flash("Error removing item.", "error")
    return redirect(url_for('wishlist.view_wishlist'))

@wishlist_bp.route('/wishlist/move-to-cart/<int:product_id>')
def move_to_cart(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    if CartRepository.add_or_update_item(user_id, product_id, 1):
        WishlistRepository.remove_item(user_id, product_id)
        flash("Item moved to your shopping cart!", "success")
    else:
        flash("Failed to move item to cart.", "error")
    return redirect(url_for('wishlist.view_wishlist'))