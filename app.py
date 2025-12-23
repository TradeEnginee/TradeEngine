from flask import Flask
from Database.db_manager import init_schema
from routes.auth_routes import auth_bp
from routes.product_route import shop_bp


app = Flask(__name__)

app.secret_key = "TradeEngine_Secret_Key_2025" 


init_schema()


app.register_blueprint(auth_bp)
app.register_blueprint(shop_bp)



if __name__ == '__main__':
    print("🚀 TradeEngine is running on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)