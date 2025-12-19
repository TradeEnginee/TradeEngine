# routes/checkout_routes.py
from flask import Blueprint, request, jsonify
from order import Order, OrderItem, ShippingAddress, OrderStatus
from payment_processor import PaymentContext, PaymentResult
from datetime import datetime

checkout_bp = Blueprint('checkout', __name__, url_prefix='/api/checkout')

# In-memory storage (replace with database)
orders_db = {}
order_counter = 1


def validate_shipping_address(data: dict) -> tuple[bool, str, ShippingAddress]:
    """Validate and create ShippingAddress from request data"""
    required_fields = ["full_name", "address_line1", "city", "state", "postal_code", "country", "phone"]
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}", None
    
    # Validate phone number (basic)
    phone = str(data["phone"]).replace("-", "").replace(" ", "")
    if not phone.isdigit() or len(phone) < 10:
        return False, "Invalid phone number", None
    
    # Validate postal code (basic)
    if len(str(data["postal_code"])) < 3:
        return False, "Invalid postal code", None
    
    address = ShippingAddress(
        full_name=data["full_name"],
        address_line1=data["address_line1"],
        address_line2=data.get("address_line2", ""),
        city=data["city"],
        state=data["state"],
        postal_code=data["postal_code"],
        country=data["country"],
        phone=data["phone"]
    )
    
    return True, "Valid", address


@checkout_bp.route('/shipping', methods=['POST'])
def save_shipping_info():
    """Save shipping information for the order"""
    global order_counter
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Validate shipping address
    is_valid, message, shipping_address = validate_shipping_address(data.get("shipping_address", {}))
    if not is_valid:
        return jsonify({"error": message}), 400
    
    # Validate cart items
    cart_items = data.get("cart_items", [])
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400
    
    # Create order items
    order_items = []
    for item in cart_items:
        order_items.append(OrderItem(
            product_id=item["product_id"],
            product_name=item["product_name"],
            quantity=item["quantity"],
            unit_price=item["unit_price"]
        ))
    
    # Create order
    order = Order(
        id=order_counter,
        user_id=data.get("user_id", 0),
        items=order_items,
        shipping_address=shipping_address,
        status=OrderStatus.PENDING
    )
    
    orders_db[order_counter] = order
    order_counter += 1
    
    return jsonify({
        "message": "Shipping information saved",
        "order_id": order.id,
        "order_summary": order.to_dict()
    }), 201


@checkout_bp.route('/payment-methods', methods=['GET'])
def get_payment_methods():
    """Get available payment methods"""
    methods = [
        {
            "id": "credit_card",
            "name": "Credit Card",
            "description": "Pay securely with Visa, Mastercard, or American Express",
            "icon": "credit-card"
        },
        {
            "id": "paypal",
            "name": "PayPal",
            "description": "Pay with your PayPal account",
            "icon": "paypal"
        },
        {
            "id": "cod",
            "name": "Cash on Delivery",
            "description": "Pay when your order arrives",
            "icon": "banknote"
        }
    ]
    return jsonify({"payment_methods": methods}), 200


@checkout_bp.route('/process-payment', methods=['POST'])
def process_payment():
    """Process payment for an order using Strategy Pattern"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    order_id = data.get("order_id")
    payment_method = data.get("payment_method")
    payment_data = data.get("payment_data", {})
    
    # Validate order exists
    if order_id not in orders_db:
        return jsonify({"error": "Order not found"}), 404
    
    order = orders_db[order_id]
    
    # Check order status
    if order.status != OrderStatus.PENDING:
        return jsonify({"error": "Order has already been processed"}), 400
    
    # Validate payment method
    if payment_method not in PaymentContext.get_available_methods():
        return jsonify({
            "error": f"Invalid payment method. Available: {PaymentContext.get_available_methods()}"
        }), 400
    
    # Use Strategy Pattern to process payment
    payment_context = PaymentContext()
    payment_context.set_strategy(payment_method)
    
    result: PaymentResult = payment_context.process_payment(order.total, payment_data)
    
    if result.success:
        # Update order
        order.payment_method = payment_method
        order.transaction_id = result.transaction_id
        order.status = OrderStatus.PAID if payment_method != "cod" else OrderStatus.PROCESSING
        order.updated_at = datetime.utcnow()
        
        return jsonify({
            "success": True,
            "message": result.message,
            "transaction_id": result.transaction_id,
            "order": order.to_dict()
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": result.message
        }), 400


@checkout_bp.route('/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details"""
    if order_id not in orders_db:
        return jsonify({"error": "Order not found"}), 404
    
    return jsonify({"order": orders_db[order_id].to_dict()}), 200


@checkout_bp.route('/validate-address', methods=['POST'])
def validate_address():
    """Validate shipping address without creating order"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    is_valid, message, _ = validate_shipping_address(data)
    
    return jsonify({
        "valid": is_valid,
        "message": message
    }), 200 if is_valid else 400
