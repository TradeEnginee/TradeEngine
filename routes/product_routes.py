from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Database.Repositories.product_repo import ProductRepository
from Database.Repositories.review_repo import ReviewRepository
from models.review_model import Review

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
# Product Detail Page
# ==========================================
@shop_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    product = ProductRepository.get_product_by_id(product_id)
    
    if not product:
        flash("Product not found.", "error")
        return redirect(url_for('shop.home'))
    
    reviews = ReviewRepository.get_reviews_by_product(product_id)
    
    average_rating = 0
    if reviews:
        total_rating = sum([review.rating for review in reviews])
        average_rating = round(total_rating / len(reviews), 1)
    
    return render_template(
        'product_detail.html',
        product=product,
        reviews=reviews,
        average_rating=average_rating,
        reviews_count=len(reviews)
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
        
    
        if ReviewRepository.add_review(new_review):
            flash("Review added successfully!", "success")
        else:
            flash("Failed to add review.", "error")
            
    except Exception as e:
        flash(f"Error: {e}", "error")
    
    return redirect(url_for('shop.product_detail', product_id=product_id))

# ==========================================
# Add to Cart (Updated with Quantity Support)
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
# Empty Cart (For Testing)
# ==========================================
@shop_bp.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    flash("Cart cleared.", "info")
    return redirect(url_for('shop.home'))