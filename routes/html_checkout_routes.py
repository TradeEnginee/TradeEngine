from flask import Blueprint, request, render_template_string, session
from datetime import datetime
from models.order import ShippingAddress, OrderItem
from models.payment_processor import CreditCardStrategy, CashOnDeliveryStrategy, PaymentContext
from Database.db_manager import get_connection
from Database.Repositories import cart_repo, user_repo, product_repo
html_checkout_bp = Blueprint('html_checkout', __name__)


# ============================================================
# CART & USER HELPER FUNCTIONS (Replace these when cart is implemented)
# ============================================================

def get_current_user_id():
    """
    Get the current logged-in user's ID.
    Preferred: session['user_id'] (set by auth_routes)
    Fallback: Guest ID 1 (for testing if not logged in)
    """
    if 'user_id' in session:
        return session['user_id']
    
    # Optional: You can check Flask-Login's current_user too, 
    # but since auth_routes sets session, we prioritize that for now.
    from flask_login import current_user
    if current_user.is_authenticated:
        return current_user.id
        
    # Default to guest user (ID: 1) for testing
    return 1


def get_cart_items():
    """
    Get the current user's cart items.
    
    TODO: Replace with actual cart implementation:
        - Session-based cart: return session.get('cart', [])
        - Database cart: query cart_items table for user_id
        - API-based cart: fetch from cart service
    
    Returns:
        list: List of dicts with keys: product_id, product_name, quantity, unit_price
    """
    # Check if cart exists in session
    if 'cart' in session and len(session['cart']) > 0:
        return session['cart']
    

    
    # Fetch from database using the CartRepository
    user_obj = user_repo.UserRepository.get_user_by_id(get_current_user_id())
    if not user_obj:
        return []
        
    cart_obj = cart_repo.CartRepository.get_cart_by_user(user_obj)
    if not cart_obj or cart_obj.is_empty:
        return []

    # Map ShoppingCart items to the list of dicts format expected by checkout logic
    db_cart = []
    for item in cart_obj.items:
        db_cart.append({
            'product_id': item.product.id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'unit_price': item.product.price
        })
    
    return db_cart



def calculate_cart_total(cart_items):
    """Calculate total price from cart items."""
    return sum(item['quantity'] * item['unit_price'] for item in cart_items)


def clear_cart():
    """
    Clear the user's cart after successful order.
    
    TODO: Implement based on your cart storage:
        - Session: session.pop('cart', None)
        - Database: DELETE FROM cart_items WHERE user_id = ?
    """
    cart_repo.clear_cart(get_current_user_id())
    if 'cart' in session:
        session.pop('cart', None)


# ============================================================
# HTML TEMPLATES
# ============================================================


# ============================================================
# CHECKOUT ROUTE
# ============================================================

@html_checkout_bp.route('/submit_checkout', methods=['POST'])
def submit_checkout():
    """Handle HTML form submission for checkout"""
    try:
        # 1. Get current user
        user_id = get_current_user_id()
        if user_id is None:
            flash("Please login to complete your order.", "error")
            return redirect(url_for('auth.login'))
        
        # 2. Build shipping address from form
        shipping = ShippingAddress(
            full_name=request.form.get('full_name', ''),
            address_line1=request.form.get('address_line1', ''),
            address_line2=request.form.get('address_line2', ''),
            city=request.form.get('city', ''),
            state=request.form.get('state', ''),
            postal_code=request.form.get('postal_code', ''),
            country=request.form.get('country', ''),
            phone=request.form.get('phone', '')
        )
        
        # 3. Get cart items and calculate total
        cart_items = get_cart_items()
        if not cart_items:
            flash("Your cart is empty. Please add items before checkout.", "error")
            return redirect(url_for('shop.home'))
        
        total_price = calculate_cart_total(cart_items)
        
        # Convert cart items to OrderItem objects
        items = [
            OrderItem(
                product_id=item['product_id'],
                product_name=item['product_name'],
                quantity=item['quantity'],
                unit_price=item['unit_price']
            )
            for item in cart_items
        ]
        
        # 4. Process payment using Strategy Pattern
        payment_method = request.form.get('payment_method', 'cod')
        
        if payment_method == 'credit_card':
            strategy = CreditCardStrategy()
            payment_details = {
                'card_number': request.form.get('card_number', ''),
                'expiry_month': request.form.get('expiry_month', ''),
                'expiry_year': request.form.get('expiry_year', ''),
                'cvv': request.form.get('cvv', ''),
                'cardholder_name': request.form.get('cardholder_name', '')
            }
        else:
            strategy = CashOnDeliveryStrategy()
            payment_details = {}
        
        processor = PaymentContext(strategy)
        payment_result = processor.process_payment(total_price, payment_details)
        
        if not payment_result.success:
            flash(payment_result.message, "error")
            return redirect(url_for('checkout_page'))
        
        # 5. Save order (using Repository with Shared Transaction)
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            from Database.Repositories.order_repo import OrderRepository
            
            # Create Order (OrderRepo now handles order & items)
            order_id = OrderRepository.create_order(
                user_id=user_id,
                cart_items=items, # items is List[OrderItem]
                total_amount=total_price,
                shipping_address=shipping.to_json(),
                payment_method=payment_method,
                status='confirmed',
                cursor=cursor # Pass cursor to keep transaction open
            )
            
            if not order_id:
                raise Exception("Failed to create order in database.")
                
            # 6. Reduce inventory stock (using same cursor)
            for item in items:
                # Reduce inventory stock
                product_repo.ProductRepository.reduce_stock(item.product_id, item.quantity, cursor=cursor)
        
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
        
        # 7. Clear the cart after successful order
        clear_cart()
        
        # 8. Return success page
        return render_template(
            'order_success.html',
            order_id=order_id,
            total=f"{total_price:.2f}",
            method="Cash on Delivery" if payment_method == 'cod' else "Credit Card",
            status="Confirmed"
        )
        
    except Exception as e:
        flash(f"An unexpected error occurred: {str(e)}", "error")
        return redirect(url_for('checkout_page'))
