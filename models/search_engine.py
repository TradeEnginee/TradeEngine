from models.catalog import Catalog
class SearchEngine:
    def __init__(self, catalog):
        self.catalog = catalog
    
    def _split_into_keywords(self, query):
        
        if not query:
            return self.get_random_products_from_all_categories()
        return query.lower().strip().split()
    
    def search_products(self, query):
       
        keywords = self._split_into_keywords(query)
        
        results = []
        for product in keywords:
            for product_item in self.catalog.products:
             for value in product_item.values():
               if product.lower() == value.lower():
                results.append(product_item)
                break
        
        return results
    
    def search_with_suggestions(self, query):
        
        keywords = self._split_into_keywords(query)
        
        
        result_list = []
        for product_item in self.catalog.products:
        
            match_count = 0
            
            for product in keywords:
             for value in product_item.values():
               
               if product.lower() == value.lower():
                match_count +=1
            scored_results = {
                "product": product_item,
                "match_score": match_count
            }
            result_list.append(scored_results)

        
        
        result_list.sort(key=lambda x: x['match_score'], reverse=True)
        
        return [item['product'] for item in result_list if item['match_score'] > 0]
