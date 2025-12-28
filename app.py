from flask import Flask, render_template
from routes.checkout_routes import checkout_bp
from routes.html_checkout_routes import html_checkout_bp
from Database.db_manager import init_schema, get_connection
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'dev-secret-key'

CORS(app)

# Register Blueprints
app.register_blueprint(checkout_bp, url_prefix='/api')
app.register_blueprint(html_checkout_bp)

@app.route('/')
def home():
    # Default to checkout page for payment testing
    return checkout_page()

@app.route('/checkout')
def checkout_page():
    """Serve the dynamic HTML checkout page"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Fetching all products as a simulated "cart" for now
        cursor.execute("SELECT id, name, price FROM products")
        products = cursor.fetchall()
        conn.close()
        
        items = []
        total = 0
        for p in products:
            item = {'id': p[0], 'name': p[1], 'price': p[2], 'quantity': 1 if p[0] == 1 else 2}
            items.append(item)
            total += item['price'] * item['quantity']
            
        return render_template('checkout.html', items=items, total=total)
    except Exception as e:
        return f"Error loading checkout: {str(e)}", 500

if __name__ == '__main__':
    # Initialize database on startup if it doesn't exist
    if not os.path.exists('Database/TradeEngine.db'):
        init_schema()
    
    app.run(debug=True, port=3000)
