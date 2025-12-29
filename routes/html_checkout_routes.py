from Database.Repositories.cart_repo import CartRepository
from flask import Blueprint, request, render_template_string, session, flash, redirect, url_for, render_template
from datetime import datetime
from models.order import ShippingAddress, OrderItem
from models.payment_processor import CreditCardStrategy, CashOnDeliveryStrategy, PaymentContext
from Database.db_manager import get_connection
from Database.Repositories import cart_repo, user_repo, product_repo
html_checkout_bp = Blueprint('html_checkout', __name__)


@html_checkout_bp.route('/submit_checkout', methods=['POST'])
def submit_checkout():
    """Handle HTML form submission for checkout"""
    try:
        # 1. Get current user
        if 'user_id' not in session:
            flash("Please login to complete your order.", "error")
            return redirect(url_for('auth.login'))
        
        user_id = session['user_id']
        
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
        
        # 3. Get cart items and calculate total using CartRepository
        user_obj = user_repo.UserRepository.get_user_by_id(user_id)
        cart = CartRepository.get_cart_by_user(user_obj)
        
        if not cart or cart.is_empty:
            flash("Your cart is empty. Please add items before checkout.", "error")
            return redirect(url_for('shop.home'))
        
        # Use the Cart object's total directly
        total_price = cart.subtotal
        
        # Convert ShoppingCart items to OrderItem objects
        items = [
            OrderItem(
                product_id=item.product.id,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=item.product.price
            )
            for item in cart.items
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
        CartRepository.clear_cart(user_id)
        if 'cart' in session:
            session.pop('cart', None)
        
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
