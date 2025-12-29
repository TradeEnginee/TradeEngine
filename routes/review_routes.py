from flask import Blueprint, request, redirect, url_for, flash, session
from Database.Repositories.review_repo import ReviewRepository
from models.review_model import Review

review_bp = Blueprint('review', __name__)


@review_bp.route('/products/<int:product_id>/reviews', methods=['POST'])
def add_review(product_id):
    if 'user_id' not in session:
        flash("Please login to add a review.", "error")
        return redirect(url_for('auth.login'))

    user_id = session.get('user_id')
    username = session.get('username')

    rating = request.form.get('rating')
    comment = request.form.get('comment', '').strip()

    try:
        rating = int(rating)
    except (TypeError, ValueError):
        flash("Rating must be a number between 1 and 5.", "error")
        return redirect(url_for('shop.product_detail', product_id=product_id))

    review = Review(
        review_id=None,
        user_id=user_id,
        product_id=product_id,
        rating=rating,
        comment=comment,
        created_at=None,
        username=username
    )

    success = ReviewRepository.add_review(review)

    if success:
        flash("Your review has been added.", "success")
    else:
        flash("Could not add review. Please try again.", "error")

    return redirect(url_for('shop.product_detail', product_id=product_id))
