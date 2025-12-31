from flask import Blueprint, render_template, session, request, redirect, url_for, flash, abort
from Database.Repositories.product_repo import ProductRepository
from Database.Repositories.review_repo import ReviewRepository
from Database.Repositories.order_repo import OrderRepository
from models.review_model import Review
import json

review_repo = ReviewRepository()

shop_bp = Blueprint('shop', __name__)

# ==========================================
# Home Page (Product Display)
# ==========================================
@shop_bp.route('/')
def home():
    username = session.get('username', 'Guest')
    
    search_query = request.args.get('search')
    sort_by = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'DESC')
    
    products = []

    if search_query:
        products = ProductRepository.search_products(search_query)
        categorized_products = {'Search Results': products} if products else {}
    else:
        products = ProductRepository.get_all_products(ordered_by=sort_by, sort_type=order)
        categorized_products = {}
        for product in products:
            cat = product.category
            if cat not in categorized_products:
                categorized_products[cat] = []
            categorized_products[cat].append(product)

    return render_template(
        'index.html',
        user=username,
        categorized_products=categorized_products,
        current_sort=sort_by,
        current_order=order
    )

# ==========================================
# Add Review
# ==========================================
@shop_bp.route('/product/<int:product_id>/add_review', methods=['POST'])
def add_review(product_id):
    if 'user_id' not in session:
        flash("Please login to add a review.", "error")
        return redirect(url_for('auth.login'))
    
    try:
        rating = int(request.form['rating'])
        comment = request.form.get('comment', '').strip()
        
        if not (1 <= rating <= 5):
            flash("Rating must be between 1 and 5.", "error")
            return redirect(url_for('shop.product_detail', product_id=product_id))
        
        new_review = Review(
            review_id=None,
            user_id=session['user_id'],
            product_id=product_id,
            rating=rating,
            comment=comment
        )
        
        success = ReviewRepository.add_review(new_review)
        if success:
            flash("Review added successfully!", "success")
        else:
            flash("Failed to add review.", "error")
    except Exception as e:
        flash(f"Error: {e}", "error")
    
    return redirect(url_for('shop.product_detail', product_id=product_id))

# ==========================================
# Add to Cart (SESSION cart – تفضّلي سايبه كما هو)
# ==========================================
@shop_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' not in session:
        flash("Please login to add items to cart.", "error")
        return redirect(url_for('auth.login'))

    quantity = int(request.args.get('quantity', 1))
    product = ProductRepository.get_product_by_id(product_id)
    
    if product and product.is_in_stock():
        if quantity > product.stock_quantity:
            flash(f"Only {product.stock_quantity} items available in stock.", "error")
            return redirect(request.referrer or url_for('shop.home'))
        
        if 'cart' not in session:
            session['cart'] = {}
        
        cart = session['cart']
        str_id = str(product_id)

        if str_id in cart:
            new_quantity = cart[str_id]['quantity'] + quantity

            if new_quantity > product.stock_quantity:
                flash(f"Cannot add more. Only {product.stock_quantity} items available.", "error")
                return redirect(request.referrer or url_for('shop.home'))
            
            cart[str_id]['quantity'] = new_quantity
            flash(f"Updated {product.name} quantity in cart!", "success")
        else:
            item_data = product.to_dict()
            item_data['quantity'] = quantity
            cart[str_id] = item_data
            flash(f"{product.name} added to cart!", "success")

        session['cart'] = cart
        session.modified = True
    else:
        flash("Product out of stock or not found.", "error")

    return redirect(request.referrer or url_for('shop.home'))

# ==========================================
# Product Detail Page
# ==========================================
@shop_bp.route('/product/<int:product_id>', endpoint='product_detail')
def product_detail_view(product_id):
    product = ProductRepository.get_product_by_id(product_id)
    if not product:
        abort(404)

    reviews = review_repo.get_reviews_by_product(product_id)

    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        reviews_count = len(reviews)
    else:
        avg_rating = 0
        reviews_count = 0

    return render_template(
        'product_detail.html',
        product=product,
        reviews=reviews,
        avg_rating=avg_rating,
        reviews_count=reviews_count
    )

# ==========================================
# My Orders Page
# ==========================================
@shop_bp.route('/my-orders')
def my_orders():
    if 'user_id' not in session:
        flash("Please login to view your orders.", "warning")
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    raw_orders = OrderRepository.get_user_orders(user_id)
    
    orders_data = []
    
    for row in raw_orders:
        order_id = row['id']
        
        try:
            shipping_info = json.loads(row['shipping_address'])
        except Exception:
            shipping_info = {}
        
        items = OrderRepository.get_order_details(order_id)
        
        orders_data.append({
            'id': order_id,
            'date': row['created_at'],
            'status': row['status'],
            'total': row['total_amount'],
            'payment': row['payment_method'],
            'shipping': shipping_info,
            'products': items
        })
    
    return render_template('orders.html', orders=orders_data)


