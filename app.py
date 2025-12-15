from flask import Flask
from extensions import db, login_manager
from routes.auth_routes import auth_bp
from models.user_model import User, Customer, Admin

try:
    from models.product_base import Product
    from models.product_types import CosmeticsProduct, ElectronicProduct, FoodProduct, ClothesProduct, SportsProduct
except ImportError:
    pass
except Exception:
    pass

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key_123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trade_engine.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database Tables Created Successfully!")
    app.run(debug=True)

@app.route('/')
def home():
    return redirect(url_for('auth.login'))