from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Database.Repositories.product_repo import ProductRepository

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
# Add to Cart (The Bridge)**

# ==========================================
@shop_bp.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    
    if 'user_id' not in session:
        flash("Please login to add items to cart.", "error")
        return redirect(url_for('auth.login'))

    
    product = ProductRepository.get_product_by_id(product_id)
    
    if product and product.is_in_stock():
        
        if 'cart' not in session:
            session['cart'] = {}
        
        cart = session['cart']
        str_id = str(product_id) 

        
        if str_id in cart:
            cart[str_id]['quantity'] += 1
            flash(f"Added another {product.name} to cart!", "success")
        else:
           
            item_data = product.to_dict()
            item_data['quantity'] = 1 
            cart[str_id] = item_data
            flash(f"{product.name} added to cart!", "success")

       
        session['cart'] = cart
        session.modified = True 
        
    else:
        flash("Product out of stock or not found.", "error")

    
    return redirect(request.referrer or url_for('shop.home'))

# ==========================================
# Empty Cart (For Testing)
# ==========================================
@shop_bp.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash("Cart cleared.", "info")
    return redirect(url_for('shop.home'))