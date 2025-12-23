import random

class Catalog:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product) 

    def get_products_by_category(self, category):
        results = []
        for product in self.products:
            if product.category.lower() == category.lower():  
                results.append(product)
        return results
    
    def get_random_products_from_all_categories(self, products_per_category=5):
        all_categories = set(product.category for product in self.products)
        result = []
    
        for category in all_categories:
            all_in_category = self.get_products_by_category(category)
            if len(all_in_category) > products_per_category:
                selected = random.sample(all_in_category, products_per_category)
            else:
                selected = all_in_category[:] 
           
            result.extend(selected)
        return result
    
    def get_all_products_shuffled(self, category):
        category_products = self.get_products_by_category(category)
        random.shuffle(category_products)
        return category_products
    
    def sort_products_by_price(self, chosen, category=None):
        if category:
            products_to_sort = self.get_products_by_category(category)
        else:
            products_to_sort = self.get_random_products_from_all_categories(products_per_category=5)
        
        if chosen == 'Ascending':
            return sorted(products_to_sort, key=lambda x: x.price)  
        
        elif chosen == 'Descending':
            return sorted(products_to_sort, key=lambda x: x.price, reverse=True)
        
        elif chosen == 'A-Z':
            return sorted(products_to_sort, key=lambda x: x.name)  
        
        elif chosen == 'Z-A':
            return sorted(products_to_sort, key=lambda x: x.name, reverse=True)
        
        else:
            return products_to_sort

    
    def get_product_by_id(self, product_id):
        for product in self.products:
            if product.id == product_id:
                return product
        return None