from flask import Flask
from routes.checkout_routes import checkout_bp
from Database.db_manager import init_schema
import os

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(checkout_bp, url_prefix='/api')

if __name__ == '__main__':
    # Initialize database on startup
    if not os.path.exists('Database/TradeEngine.db'):
        init_schema()
    
    app.run(debug=True, port=3000)
