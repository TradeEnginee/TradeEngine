from flask import Flask
from Database.db_manager import init_schema
from routes.auth_routes import auth_bp
from routes.product_route import shop_bp
from routes.admin_routes import admin_bp
from routes.cart_routes import cart_bp
from routes.wishlist_routes import wishlist_bp
from routes.review_routes import review_bp
from routes.checkout_routes import checkout_bp
from routes.html_checkout_routes import html_checkout_bp


app = Flask(__name__)

app.secret_key = "TradeEngine_Secret_Key_2025" 


init_schema()


app.register_blueprint(auth_bp)
app.register_blueprint(shop_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(wishlist_bp)
app.register_blueprint(review_bp)
app.register_blueprint(checkout_bp, url_prefix='/api')
app.register_blueprint(html_checkout_bp)

# ============================================================
# FLASK LOGIN SETUP (Minimal Fix for Crash)
# ============================================================
from flask_login import LoginManager
from Database.Repositories.user_repo import UserRepository

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    """Reload user object from user_id stored in session"""
    return UserRepository.get_user_by_id(int(user_id))


@app.route('/checkout')
def checkout_page():
    """Serve the dynamic HTML checkout page"""
    try:
        from routes.html_checkout_routes import get_cart_items, calculate_cart_total
        from flask import render_template
        
        # Now fetches real items from database via the refactored helper
        cart_items = get_cart_items()
        total = calculate_cart_total(cart_items)
        
        # Correctly maps the product_id/name keys from the helper
        items = [
            {
                'id': item['product_id'],
                'name': item['product_name'],
                'price': item['unit_price'],
                'quantity': item['quantity']
            }
            for item in cart_items
        ]
            
        return render_template('checkout.html', items=items, total=total)
    except Exception as e:
        return f"Error loading checkout: {str(e)}", 500


if __name__ == '__main__':
    print("🚀 TradeEngine is running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)