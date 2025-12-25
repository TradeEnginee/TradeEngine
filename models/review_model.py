from datetime import datetime

class Review:
    def __init__(self, review_id, user_id, product_id, rating, comment="", created_at=None, username=None):
        self.id = review_id
        self.user_id = user_id
        self.product_id = product_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at or datetime.now()
        self.username = username
