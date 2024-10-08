import traceback
from datetime import datetime

from sqlalchemy.orm import Session
from exceptions import raise_error
from models import Review as ReviewModel
from schemas.review import ReviewCreate


def get_review_service():
    try:
        yield ReviewService()
    finally:
        pass


class ReviewService:
    def create_review(self, review: ReviewCreate, db: Session, user_id: int, book_id: int):
        try:
            new_review = ReviewModel(
                user_id=user_id,
                book_id=book_id,
                rating=review.rating,
                comment=review.comment,
                created_at=datetime.now(),
            )
            db.add(new_review)
            db.commit()
            db.refresh(new_review)
            return new_review
        except Exception as e:
            print(traceback.print_exc())
