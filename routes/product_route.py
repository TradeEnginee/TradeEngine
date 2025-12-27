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