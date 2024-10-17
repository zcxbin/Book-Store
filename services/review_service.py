import traceback
from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm import Session
from exceptions import raise_error
from models import Review as ReviewModel
from schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate, ReviewUpdateResponse


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
            db.rollback()
            print(traceback.print_exc())

    def get_reviews_by_books_id(self, db: Session, book_id: int) -> ReviewResponse:
        try:
            return db.query(ReviewModel).filter(ReviewModel.book_id == book_id).all()
        except Exception as e:
            print(traceback.print_exc())

    def update_review(self, db: Session, review: ReviewUpdate, user_id: int, book_id: int):
        update_review = db.query(ReviewModel).filter(and_(
            ReviewModel.user_id == user_id,
            ReviewModel.book_id == book_id
        )).first()
        update_review.rating = review.rating
        update_review.comment = review.comment
        update_review.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.commit()
        db.refresh(update_review)
        return ReviewUpdateResponse(
            rating=review.rating,
            comment=review.comment,
            created_at=update_review.created_at
        )

    def delete_review(self, db: Session, user_id: int, book_id: int):
        review_to_delete = db.query(ReviewModel).filter(and_(
            ReviewModel.user_id == user_id,
            ReviewModel.book_id == book_id
        )).first()

        if review_to_delete:
            db.delete(review_to_delete)
            db.commit()
        else:
            print("Review không tồn tại")

