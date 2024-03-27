from typing import Type

from sqlalchemy.orm import Session
from src.book_review import models, schemas
from src.book_review.models import Book


def get_book_by_id(db: Session, book_id: int) -> Type[Book] | None:
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_by_name(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()


def get_books(db: Session, author_name: str | None, publication_year: int | None, skip: int = 0, limit: int = 100):
    query = db.query(models.Book)

    if author_name:
        query = query.filter(models.Book.author.ilike(f"%{author_name}%"))

    # Ideally I should provide year range
    elif publication_year:
        query = query.filter(models.Book.publication_year == publication_year)

    return query.offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_reviews(db: Session, book_id: int, skip: int = 0, limit: int = 100):
    return (db.query(models.Review).filter(models.Review.book_id == book_id)
            .offset(skip).limit(limit).all())


def create_review(db: Session, review: schemas.ReviewCreate, book_id: int):
    db_item = models.Review(**review.dict(), book_id=book_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
