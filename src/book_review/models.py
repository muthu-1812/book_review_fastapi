from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Text
from sqlalchemy.orm import relationship

from src.book_review.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    author = Column(String, nullable=False)
    publication_year = Column(Integer)
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    reviews = relationship("Review", back_populates="review_of")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    ratings = Column(Float, nullable=False)
    review = Column(Text, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    review_author = Column(String, nullable=False)
    reviewer_email = Column(String, nullable=True)
    created_on = Column(DateTime, default=datetime.now)
    updated_on = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    review_of = relationship("Book", back_populates="reviews")
