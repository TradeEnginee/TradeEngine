from flask import Blueprint, request, render_template_string
from datetime import datetime
from models.order import ShippingAddress, OrderItem
from models.payment_processor import CreditCardStrategy, CashOnDeliveryStrategy, PaymentContext
from Database.db_manager import get_connection

html_checkout_bp = Blueprint('html_checkout', __name__)

# Success page template
SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Success</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <div class="card" style="text-align: center; max-width: 600px; margin: 4rem auto; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
            <h1 style="color: var(--success-color); margin-bottom: 1rem;">Order Confirmed!</h1>
            <p style="color: var(--text-secondary); margin-bottom: 2rem;">
                Thank you for your purchase. Your order has been placed successfully.
            </p>
            <div style="background: #f1f5f9; padding: 1.5rem; border-radius: 8px; text-align: left; margin-bottom: 2rem;">
                <p><strong>Order ID:</strong> #{{ order_id }}</p>
                <p><strong>Total Amount:</strong> ${{ total }}</p>
                <p><strong>Payment Method:</strong> {{ method }}</p>
                <p><strong>Status:</strong> {{ status }}</p>
            </div>
            <a href="/checkout" style="display: inline-block; padding: 1rem 2rem; background: var(--primary-color); color: white; text-decoration: none; border-radius: var(--radius); font-weight: 600;">
                Place Another Order
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
</head>
<body>
    <div class="container">
        <div class="card" style="text-align: center; max-width: 600px; margin: 4rem auto; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">❌</div>
            <h1 style="color: var(--error-color); margin-bottom: 1rem;">Payment Failed</h1>
            <p style="margin-bottom: 2rem;">{{ error_message }}</p>
            <a href="/checkout" style="display: inline-block; padding: 1rem 2rem; background: var(--primary-color); color: white; text-decoration: none; border-radius: var(--radius); font-weight: 600;">
                Try Again
            </a>
        </div>
    </div>
</body>
</html>
"""

@html_checkout_bp.route('/submit_checkout', methods=['POST'])
def submit_checkout():
    """Handle HTML form submission for checkout"""
    try:
        # Get form data
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
        
        # Fetch actual products from database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, price FROM products")
        products = cursor.fetchall()
        
        items = []
        total_price = 0
        for p in products:
            qty = 1 if p[0] == 1 else 2
            item = OrderItem(product_id=p[0], product_name=p[1], quantity=qty, unit_price=p[2])
            items.append(item)
            total_price += item.quantity * item.unit_price
        
        # Get payment method
        payment_method = request.form.get('payment_method', 'cod')
        
        # Process payment
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
        
        # Save to database
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO orders (user_id, shipping_address, payment_method, total_amount, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            1,  # Hardcoded user_id
            shipping.to_json(),
            payment_method,
            total_price,
            'confirmed',
            datetime.now().isoformat()
        ))
        
        order_id = cursor.lastrowid
        
        # Insert order items
        for item in items:
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase)
                VALUES (?, ?, ?, ?)
            """, (order_id, item.product_id, item.quantity, item.unit_price))
        
        conn.commit()
        conn.close()
        
        # Return success page
        return render_template_string(
            SUCCESS_TEMPLATE,
            order_id=order_id,
            total=f"{total_price:.2f}",
            method="Cash on Delivery" if payment_method == 'cod' else "Credit Card",
            status="Confirmed"
        )
        
    except Exception as e:
        return render_template_string(ERROR_TEMPLATE, error_message=str(e))
