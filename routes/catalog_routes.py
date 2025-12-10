from flask import Flask, jsonify
from models.catalog import Catalog
from models.product_types import CosmeticsProduct, ElectronicProduct, FoodProduct, ClothesProduct, SportsProduct

app = Flask(__name__)
catalog = Catalog()

# Sample data population
catalog.add_product(CosmeticsProduct(1, "Lipstick", 20, "lipstick.jpg", "Cosmetics"))
catalog.add_product(ElectronicProduct(2, "Headphones", 50, "headphones.jpg", "Electronics"))
catalog.add_product(FoodProduct(3, "Chocolate", 10, "chocolate.jpg", "Food"))
catalog.add_product(ClothesProduct(4, "T-Shirt", 15, "tshirt.jpg", "Clothes"))
catalog.add_product(SportsProduct(5, "Football", 30, "football.jpg", "Sports"))

# Homepage endpoint (random products)
@app.route("/home")
def home():
    products = catalog.get_random_products()
    return jsonify([vars(p) for p in products])

# Products by category
@app.route("/products/<category>")
def products_by_category(category):
    products = catalog.get_products_by_category(category)
    return jsonify([vars(p) for p in products])

if __name__ == "__main__":
    app.run(debug=True)
