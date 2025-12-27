from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Database.Repositories.cart_repo import CartRepository
from Database.Repositories.user_repo import UserRepository

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart')
def view_cart():
    if 'user_id' not in session:
        flash("Please login to view your cart.", "error")
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    user = UserRepository.get_user_by_id(user_id)
    cart = CartRepository.get_cart_by_user(user)
    return render_template('cart.html', cart=cart)

@cart_bp.route('/cart/add/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash("Please login to add items to cart.", "error")
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    
    if CartRepository.add_or_update_item(user_id, product_id, 1):
        flash("Product added to cart!", "success")
    else:
        flash("Could not add product. Please try again.", "error")
        
    return redirect(request.referrer or url_for('cart.view_cart'))

@cart_bp.route('/cart/remove/<int:product_id>')
def remove_from_cart(product_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    if CartRepository.remove_item(user_id, product_id):
        flash("Item removed from cart.", "success")
    else:
        flash("Failed to remove item.", "error")
    return redirect(url_for('cart.view_cart'))

@cart_bp.route('/cart/clear')
def clear_cart():
    user_id = session.get('user_id')
    if user_id and CartRepository.clear_cart(user_id):
        flash("Cart cleared.", "success")
    return redirect(url_for('cart.view_cart'))