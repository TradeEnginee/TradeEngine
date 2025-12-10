import random
class Catalog:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def get_products_by_category(self, category):
        results = []
        for p in self.products:
            if p.category.lower() == category.lower():
                results.append(p)
        return results

    def get_random_products(self, count=5):
     max_count = min(count, len(self.products))

     selected_products = random.sample(self.products, max_count)

     return selected_products

