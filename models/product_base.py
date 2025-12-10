class Product:
    def __init__(self, id, name, price, image_url, category):
        self.id = id
        self.name = name
        self.price = price
        self.image_url = image_url
        self.category = category

    def get_specifications(self):
        return {}
