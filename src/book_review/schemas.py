from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class BookBase(BaseModel):
    title: str = Field(min_length=2, max_length=256, description="Title of the book.")
    author: str = Field(min_length=2, max_length=256, description="Author of the book")
    publication_year: int = Field(gt=0, le=datetime.now().year,
                                  description="Year value should not be in future or less than zero")


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    updated_on: datetime
    created_on: datetime

    class Config:
        from_attribute = True


class ReviewBase(BaseModel):
    ratings: float = Field(ge=0.0, le=5.0, decimal_places=2, description="Providing a rating between 0-5")
    review: str = Field(min_length=10, description="Provide a review(min length:10 characters)")
    review_author: str = Field(min_length=3, description="Provide your name")
    reviewer_email: EmailStr = Field(description="Provide email id to send a notification")


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    updated_on: datetime
    created_on: datetime

    class Config:
        from_attribute = True


class BookOut(Book):
    reviews: list[ReviewBase]
