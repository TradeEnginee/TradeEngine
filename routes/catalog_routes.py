import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, request
from models.catalog import Catalog
from models.product_types import CosmeticsProduct, ElectronicProduct, FoodProduct, ClothesProduct, SportsProduct
from models.search_engine import SearchEngine

app = Flask(__name__)
catalog = Catalog()

# 🔧 Sample data :
catalog.add_product(CosmeticsProduct("Lipstick", 20, "lipstick.jpg", "Cosmetics", "Maybelline", "Oily"))
catalog.add_product(ElectronicProduct("Headphones", 50, "headphones.jpg", "Electronics", "Sony", 2))
catalog.add_product(FoodProduct("Chocolate", 10, "chocolate.jpg", "Food", "2024-12-31"))
catalog.add_product(ClothesProduct("T-Shirt", 15, "tshirt.jpg", "Clothes", "Nike", "M"))
catalog.add_product(SportsProduct("Football", 30, "football.jpg", "Sports", "Rubber", "Football"))

# Homepage endpoint
@app.route("/home")
def home():
    products = catalog.get_random_products_from_all_categories(5)
    return jsonify([p.get_details() for p in products])

# Category page
@app.route("/category/<category_name>")
def category_page(category_name):
    products = catalog.get_all_products_shuffled(category_name)
    return jsonify([p.get_details() for p in products])

@app.route("/search")
def search():
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({"error": "Please provide a search query"}), 400
    
    search_engine = SearchEngine(catalog)
    
    results = search_engine.search_with_suggestions(query)
    
    if not results:
        return jsonify({
            "message": "No products found",
            "query": query,
            "suggestions": ["Try different keywords", "Check spelling"]
        })
    
    return jsonify({
        "query": query,
        "count": len(results),
        "results": [p.get_details() for p in results]
    })


# Sort endpoint
@app.route("/sort/<category_name>/<sort_type>")
def sort_products(category_name, sort_type):
    sort_map = {
        "asc": "Ascending",
        "desc": "Descending", 
        "a-z": "A-Z",
        "z-a": "Z-A"
    }
    
    chosen = sort_map.get(sort_type, "Ascending")  
    products = catalog.sort_products_by_price(chosen, category=category_name)
    return jsonify([p.get_details() for p in products])

if __name__ == "__main__":
    app.run(debug=True)