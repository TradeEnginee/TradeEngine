from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from Database.Repositories.product_repo import ProductRepository
from models.product_model import Product
from Database.Repositories.user_repo import UserRepository
from Database.Repositories.order_repo import OrderRepository
import json

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please login first!", "warning")
        return redirect(url_for('auth.login'))
    
    if session.get('role') != 'admin':
        flash("Access Denied! Admins only.", "error")
        return redirect(url_for('shop.home'))

    products = ProductRepository.get_all_products()
    stats = {
        'products': len(products),
        'users': 1,
        'orders': 0
    }
    
    return render_template('admin/dashboard.html', stats=stats)


@admin_bp.route('/products')
def manage_products():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    products = ProductRepository.get_all_products()
    return render_template('admin/products.html', products=products)


@admin_bp.route('/products/delete/<int:product_id>')
def delete_product(product_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    if ProductRepository.delete_product(product_id):
        flash("Product deleted successfully! 🗑️", "success")
    else:
        flash("Error deleting product.", "error")
        
    return redirect(url_for('admin.manage_products'))

@admin_bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock_quantity'])
        category = request.form['category']
        image_url = request.form['image_url']
        
        keys = request.form.getlist('detail_key[]')
        values = request.form.getlist('detail_val[]')
        
        details_dict = {}
        for k, v in zip(keys, values):
            if k.strip():
                details_dict[k.strip()] = v.strip()
        
        new_product = Product(None, name, price, image_url, category, stock, details_dict)
        
        if ProductRepository.add_product(new_product):
            flash("Product added successfully! 🎉", "success")
            return redirect(url_for('admin.manage_products'))
        else:
            flash("Error adding product.", "error")
            
    existing_categories = ProductRepository.get_all_categories()
    return render_template('admin/add_edit_product.html', product=None, categories=existing_categories)



@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    product = ProductRepository.get_product_by_id(product_id)
    if not product:
        return redirect(url_for('admin.manage_products'))

    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock_quantity'])
        category = request.form['category']
        image_url = request.form['image_url']
        
        keys = request.form.getlist('detail_key[]')
        values = request.form.getlist('detail_val[]')
        
        details_dict = {}
        for k, v in zip(keys, values):
            if k.strip():
                details_dict[k.strip()] = v.strip()

        success = ProductRepository.update_product(
            product_id, name=name, price=price, stock_quantity=stock, 
            category=category, image_url=image_url, details_dict=details_dict
        )
        
        if success:
            flash("Product updated successfully! ✅", "success")
            return redirect(url_for('admin.manage_products'))
            
    existing_categories = ProductRepository.get_all_categories()
    return render_template('admin/add_edit_product.html', product=product, categories=existing_categories)




@admin_bp.route('/users')
def manage_users():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    users = UserRepository.get_all_users()
    return render_template('admin/users.html', users=users)



@admin_bp.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    if user_id == session['user_id']:
        flash("You cannot delete your own account!", "error")
        return redirect(url_for('admin.manage_users'))

    if UserRepository.delete_user(user_id):
        flash("User deleted successfully.", "success")
    else:
        flash("Error deleting user.", "error")
        
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/users/<int:user_id>')
def user_details(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    user = UserRepository.get_user_by_id(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('admin.manage_users'))

    raw_orders = OrderRepository.get_user_orders(user_id)
    
    orders_data = []
    for row in raw_orders:
        try:
            shipping = json.loads(row['shipping_address'])
        except:
            shipping = {}
            
        orders_data.append({
            'id': row['id'],
            'total': row['total_amount'],
            'status': row['status'],
            'date': row['created_at'],
            'payment': row['payment_method'],
            'city': shipping.get('city', 'Unknown')
        })

    return render_template('admin/user_details.html', user=user, orders=orders_data)

@admin_bp.route('/orders')
def manage_orders():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    raw_orders = OrderRepository.get_all_orders()
    
    orders_data = []
    for row in raw_orders:
        orders_data.append({
            'id': row['id'],
            'username': row['username'],
            'date': row['created_at'],
            'total': row['total_amount'],
            'payment': row['payment_method'],
            'status': row['status']
        })

    return render_template('admin/orders.html', orders=orders_data)



@admin_bp.route('/orders/update-status/<int:order_id>', methods=['POST'])
def update_order_status(order_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
    
    new_status = request.form.get('status')
    
    if OrderRepository.update_order_status(order_id, new_status):
        flash(f"Order #{order_id} status updated to {new_status}.", "success")
    else:
        flash("Failed to update status.", "error")
        
    return redirect(url_for('admin.manage_orders'))
