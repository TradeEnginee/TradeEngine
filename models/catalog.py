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

    
    
    def get_random_products_from_all_categories(self, products_per_category=5):
       all_categories = set(p.category for p in self.products)
       result = []
    
       for category in all_categories:
           
           all_in_category = self.get_products_by_category(category)
        
           if all_in_category:
               count_to_select = min(products_per_category, len(all_in_category))
               selected = random.sample(all_in_category, count_to_select)
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
            products_to_sort = self.products
        
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