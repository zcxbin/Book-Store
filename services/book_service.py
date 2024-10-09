from sqlalchemy.orm import Session
from exceptions import raise_error
from models import Category as CategoryModel
from models.book import Book as BookModel
from models.author import Author as AuthorModel



def get_book_service():
    try:
        yield BookService()
    finally:
        pass


class BookService:
    def get_books_by_author_name(self, db: Session, author_name: str):
        print(author_name)
        author_model = db.query(AuthorModel).filter(
            AuthorModel.author_name == author_name).first()

        if not author_model:
            raise_error(101)

        return db.query(BookModel).filter(BookModel.author_id == author_model.id).all()

    def get_books_by_category_name(self, db: Session, category_name: str):
        category_model = db.query(CategoryModel).filter(
            CategoryModel.type_name == category_name).first()

        if not category_model:
            raise_error(201)

        return db.query(BookModel).filter(BookModel.category_id == category_model.id).all()
