from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Database.Repositories.product_repo import ProductRepository
from Database.Repositories.review_repo import ReviewRepository
from flask import abort
review_repo = ReviewRepository()
from Database.Repositories.order_repo import OrderRepository
import json

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

@shop_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = ProductRepository.get_product_by_id(product_id)
    if not product:
        abort(404)

    reviews = review_repo.get_reviews_by_product(product_id)

    if reviews:
        avg_rating = sum(r.rating for r in reviews) / len(reviews)
        reviews_count = len(reviews)
    else:
        avg_rating = None
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
        except:
            shipping_info = {}
            

        items = OrderRepository.get_order_details(order_id)
        
        orders_data.append({
            'id': order_id,
            'date': row['created_at'],
            'status': row['status'],
            'total': row['total_amount'],
            'payment': row['payment_method'],
            'shipping': shipping_info,
            'items': items
        })
    
    return render_template('orders.html', orders=orders_data)
