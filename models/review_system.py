class Review:
    def __init__(self, user_name, rating, comment=""):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        self.user_name = user_name
        self.rating = rating
        self.comment = comment

class ReviewSystem:
    def __init__(self):
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def get_average_rating(self):
        if not self.reviews:
            return 0.0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    def get_review_count(self):
        return len(self.reviews)