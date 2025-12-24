# checkout_routes.py 

from flask import Blueprint, request, jsonify
import json
from datetime import datetime
from models.order import Order, ShippingAddress, OrderItem
from models.payment_processor import PaymentProcessor, CreditCardStrategy, CashOnDeliveryStrategy, PaymentContext
from Database.Repositories.order_repo import OrderRepository
from Database.db_manager import get_connection

checkout_bp = Blueprint('checkout', __name__)

# Payment strategy factory
def get_payment_strategy(method: str, details: dict = None):
    if method == 'credit_card':
        return CreditCardStrategy(
            card_number=details.get('card_number', ''),
            expiry=details.get('expiry', ''),
            cvv=details.get('cvv', '')
        )
    elif method == 'cod':
        return CashOnDeliveryStrategy()
    else:
        raise ValueError(f"Unknown payment method: {method}")


@checkout_bp.route('/checkout', methods=['POST'])
def create_order():
    """Create a new order with shipping info and process payment"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['user_id', 'items', 'shipping', 'payment_method']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Build ShippingAddress from request data
    shipping_data = data['shipping']
    shipping = ShippingAddress(
        full_name=shipping_data.get('full_name', ''),
        address_line1=shipping_data.get('address_line1', ''),
        address_line2=shipping_data.get('address_line2', ''),
        city=shipping_data.get('city', ''),
        state=shipping_data.get('state', ''), # Added state handling
        postal_code=shipping_data.get('postal_code', ''),
        country=shipping_data.get('country', ''),
        phone=shipping_data.get('phone', '')
    )
    
    # Build OrderItems from request data
    items = []
    total_price = 0.0
    for item_data in data['items']:
        item = OrderItem(
            product_id=item_data['product_id'],
            product_name=item_data['product_name'],
            quantity=item_data['quantity'],
            unit_price=item_data['unit_price']
        )
        items.append(item)
        total_price += item.quantity * item.unit_price
    
    # Process payment using Strategy Pattern
    payment_method = data['payment_method']
    payment_details = data.get('payment_details', {})
    
    try:
        strategy = get_payment_strategy(payment_method, payment_details)
        # Use PaymentContext appropriately
        processor = PaymentContext(strategy)
        # process_payment requires amount and payment_data
        payment_result = processor.process_payment(total_price, payment_details)
        
        if not payment_result.success: # PaymentResult object, not dict
            return jsonify({'error': 'Payment failed', 'details': payment_result.message}), 400
            
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    # Save order to database
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Insert order with JSON shipping address
        # Corrected column name: total_price -> total_amount to match schema
        cursor.execute("""
            INSERT INTO orders (user_id, shipping_address, payment_method, total_amount, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data['user_id'],
            shipping.to_json(),  # Store as JSON string
            payment_method,
            total_price,
            'confirmed' if payment_result.success else 'pending',
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
        
        # Create response dictionary from PaymentResult
        payment_response = {
            'success': payment_result.success,
            'transaction_id': payment_result.transaction_id,
            'message': payment_result.message,
            'data': payment_result.data
        }

        return jsonify({
            'success': True,
            'order_id': order_id,
            'total': total_price,
            'status': 'confirmed',
            'payment': payment_response
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        conn.close()


@checkout_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Retrieve an order by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, user_id, shipping_address, payment_method, total_amount, status, created_at
            FROM orders WHERE id = ?
        """, (order_id,))
        
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Order not found'}), 404
        
        # Deserialize shipping address from JSON
        shipping = ShippingAddress.from_json(row['shipping_address'])
        
        # Get order items
        cursor.execute("""
            SELECT product_id, quantity, price_at_purchase
            FROM order_items WHERE order_id = ?
        """, (order_id,))
        
        items = [
            {
                'product_id': item['product_id'],
                'quantity': item['quantity'],
                'unit_price': item['price_at_purchase']
            }
            for item in cursor.fetchall()
        ]
        
        return jsonify({
            'order_id': row['id'],
            'user_id': row['user_id'],
            'shipping': {
                'full_name': shipping.full_name,
                'address_line1': shipping.address_line1,
                'address_line2': shipping.address_line2,
                'city': shipping.city,
                'postal_code': shipping.postal_code,
                'country': shipping.country,
                'phone': shipping.phone
            },
            'payment_method': row['payment_method'],
            'total': row['total_amount'],
            'status': row['status'],
            'items': items,
            'created_at': row['created_at']
        }), 200
        
    finally:
        conn.close()


@checkout_bp.route('/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """Get all orders for a user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, shipping_address, payment_method, total_amount, status, created_at
            FROM orders WHERE user_id = ? ORDER BY created_at DESC
        """, (user_id,))
        
        orders = []
        for row in cursor.fetchall():
            shipping = ShippingAddress.from_json(row['shipping_address'])
            orders.append({
                'order_id': row['id'],
                'shipping_city': shipping.city,
                'payment_method': row['payment_method'],
                'total': row['total_amount'],
                'status': row['status'],
                'created_at': row['created_at']
            })
        
        return jsonify({'orders': orders}), 200
        
    finally:
        conn.close()
