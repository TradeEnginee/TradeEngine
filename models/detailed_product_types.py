from .detailed_product import DetailedProduct

class DetailedCosmeticsProduct(DetailedProduct):
    def __init__(self, name, price, image_url, category, brand, skin_type, stock_quantity=10):
        super().__init__(name, price, image_url, category, stock_quantity)
        self.brand = brand
        self.skin_type = skin_type

    def get_details(self):
        details = super().get_details()
        details.update({"brand": self.brand, "skin_type": self.skin_type})
        return details

class DetailedFoodProduct(DetailedProduct):
    def __init__(self, name, price, image_url, category, expiry_date, stock_quantity=10):
        super().__init__(name, price, image_url, category, stock_quantity)
        self.expiry_date = expiry_date

    def get_details(self):
        details = super().get_details()
        details["expiry_date"] = self.expiry_date
        return details

class DetailedClothesProduct(DetailedProduct):
    def __init__(self, name, price, image_url, category, brand, size, stock_quantity=10):
        super().__init__(name, price, image_url, category, stock_quantity)
        self.brand = brand
        self.size = size

    def get_details(self):
        details = super().get_details()
        details.update({"brand": self.brand, "size": self.size})
        return details

class DetailedSportsProduct(DetailedProduct):
    def __init__(self, name, price, image_url, category, material, sport_type, stock_quantity=10):
        super().__init__(name, price, image_url, category, stock_quantity)
        self.material = material
        self.sport_type = sport_type

    def get_details(self):
        details = super().get_details()
        details.update({"material": self.material, "sport_type": self.sport_type})
        return details