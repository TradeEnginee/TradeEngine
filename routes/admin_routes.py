from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from Database.Repositories.product_repo import ProductRepository # 👈 استيراد الريبو
from models.product_model import Product # 👈 ضيف دي عشان نكريت أوبجيكت جديد

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
# ... (نفس الـ imports)

# ================================
# 1. إضافة منتج (معدلة)
# ================================
@admin_bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock_quantity'])
        category = request.form['category'] # ده هيجيب اللي اختاره أو اللي كتبه جديد
        image_url = request.form['image_url']
        
        # --- تجميع الـ Details الديناميكية ---
        keys = request.form.getlist('detail_key[]')   # قائمة المفاتيح (Color, Brand...)
        values = request.form.getlist('detail_val[]') # قائمة القيم (Red, Dell...)
        
        # دمجهم في قاموس واحد
        details_dict = {}
        for k, v in zip(keys, values):
            if k.strip(): # لو المفتاح مش فاضي
                details_dict[k.strip()] = v.strip()
        
        # إنشاء المنتج
        new_product = Product(None, name, price, image_url, category, stock, details_dict)
        
        if ProductRepository.add_product(new_product):
            flash("Product added successfully! 🎉", "success")
            return redirect(url_for('admin.manage_products'))
        else:
            flash("Error adding product.", "error")
            
    # GET: هات التصنيفات الموجودة عشان تظهر في القائمة
    existing_categories = ProductRepository.get_all_categories()
    return render_template('admin/add_edit_product.html', product=None, categories=existing_categories)


# ================================
# 2. تعديل منتج (معدلة)
# ================================
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
        
        # --- تجميع الـ Details الديناميكية ---
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