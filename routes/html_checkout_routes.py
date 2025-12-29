from flask import Blueprint, request, render_template_string, session
from datetime import datetime
from models.order import ShippingAddress, OrderItem
from models.payment_processor import CreditCardStrategy, CashOnDeliveryStrategy, PaymentContext
from Database.db_manager import get_connection

html_checkout_bp = Blueprint('html_checkout', __name__)


# ============================================================
# CART & USER HELPER FUNCTIONS (Replace these when cart is implemented)
# ============================================================

def get_current_user_id():
    """
    Get the current logged-in user's ID.
    
    TODO: Replace with Flask-Login integration:
        from flask_login import current_user
        return current_user.id if current_user.is_authenticated else None
    """
    # Check session first (for when user auth is implemented)
    if 'user_id' in session:
        return session['user_id']
    
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
    
    # Fallback: Use demo products from database for testing
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products LIMIT 3")
    products = cursor.fetchall()
    conn.close()
    
    # Create demo cart items (products is list of tuples: (id, name, price))
    demo_cart = []
    for product in products:
        demo_cart.append({
            'product_id': product[0],      # id
            'product_name': product[1],    # name
            'quantity': 1,                 # Default quantity
            'unit_price': product[2]       # price
        })
    
    return demo_cart


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
    if 'cart' in session:
        session.pop('cart', None)


# ============================================================
# HTML TEMPLATES
# ============================================================

SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Success</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <div class="auth-box" style="text-align: center; max-width: 600px;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
            <h2 style="color: var(--secondary-color);">Order Confirmed!</h2>
            <p style="color: var(--text-color); margin-bottom: 2rem;">
                Thank you for your purchase. Your order has been placed successfully.
            </p>
            <div style="background: var(--bg-color); padding: 1.5rem; border-radius: 12px; text-align: left; margin-bottom: 2rem;">
                <p><strong>Order ID:</strong> #{{ order_id }}</p>
                <p><strong>Total Amount:</strong> ${{ total }}</p>
                <p><strong>Payment Method:</strong> {{ method }}</p>
                <p><strong>Status:</strong> {{ status }}</p>
            </div>
            <a href="/shop" class="login-btn" style="display: inline-block; text-decoration: none;">
                <i class="fa-solid fa-bag-shopping"></i> Continue Shopping
            </a>
        </div>
    </div>
</body>
</html>
"""

ERROR_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Failed</title>
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div class="container">
        <div class="auth-box" style="text-align: center; max-width: 600px;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">❌</div>
            <h2 style="color: var(--danger-color);">Payment Failed</h2>
            <p style="margin-bottom: 2rem;">{{ error_message }}</p>
            <a href="/checkout" class="login-btn" style="display: inline-block; text-decoration: none;">
                <i class="fa-solid fa-rotate-left"></i> Try Again
            </a>
        </div>
    </div>
</body>
</html>
"""


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
            return render_template_string(ERROR_TEMPLATE, 
                error_message="Please login to complete your order.")
        
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
            return render_template_string(ERROR_TEMPLATE, 
                error_message="Your cart is empty. Please add items before checkout.")
        
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
            return render_template_string(ERROR_TEMPLATE, error_message=payment_result.message)
        
        # 5. Save order to database
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO orders (user_id, shipping_address, payment_method, total_amount, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            shipping.to_json(),
            payment_method,
            total_price,
            'confirmed',
            datetime.now().isoformat()
        ))
        
        order_id = cursor.lastrowid
        
        # 6. Insert order items
        for item in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
                VALUES (?, ?, ?, ?)
            """, (order_id, item.product_id, item.quantity, item.unit_price))
        
        conn.commit()
        conn.close()
        
        # 7. Clear the cart after successful order
        clear_cart()
        
        # 8. Return success page
        return render_template_string(
            SUCCESS_TEMPLATE,
            order_id=order_id,
            total=f"{total_price:.2f}",
            method="Cash on Delivery" if payment_method == 'cod' else "Credit Card",
            status="Confirmed"
        )
        
    except Exception as e:
        return render_template_string(ERROR_TEMPLATE, error_message=str(e))
