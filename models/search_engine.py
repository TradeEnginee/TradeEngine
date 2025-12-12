class SearchEngine:
    def __init__(self, catalog):
        self.catalog = catalog
    
    def _split_into_keywords(self, query):
        
        if not query:
            return []
        return query.lower().strip().split()
    
    def _matches_product(self, product, keywords):
       
        search_text = f"{product.name} {product.category} {getattr(product, 'brand', '')} {getattr(product, 'material', '')}"
        search_text = search_text.lower()
        
        for keyword in keywords:
            if keyword in search_text:
                return True
        return False
    
    def search_products(self, query):
       
        keywords = self._split_into_keywords(query)
        
        if not keywords:
            return []
        
        results = []
        for product in self.catalog.products:
            if self._matches_product(product, keywords):
                results.append(product)
        
        return results
    
    def search_with_suggestions(self, query):
        
        keywords = self._split_into_keywords(query)
        
        if not keywords:
            return []
        
        scored_results = []
        
        for product in self.catalog.products:
            search_text = f"{product.name} {product.category} {getattr(product, 'brand', '')}"
            search_text = search_text.lower()
            
            match_count = 0
            for keyword in keywords:
                if keyword in search_text:
                    match_count += 1
            
            if match_count > 0:
                scored_results.append({
                    'product': product,
                    'match_score': match_count,
                    'matched_keywords': [k for k in keywords if k in search_text]
                })
        
        scored_results.sort(key=lambda x: x['match_score'], reverse=True)
        
        return [item['product'] for item in scored_results]