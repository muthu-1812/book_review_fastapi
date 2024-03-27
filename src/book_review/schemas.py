from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class BookBase(BaseModel):
    title: str
    author: str
    publication_year: int = Field(le=datetime.now().year,
                                  description="Year value should not be in future")


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    updated_on: datetime
    created_on: datetime

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    ratings: float = Field(ge=0.0, le=5.0, description="Providing a rating between 0-5")
    review: str = Field(min_length=10, description="Min review length 50 characters", )
    review_author: str
    reviewer_email: EmailStr


class BookOut(Book):
    reviews: list[ReviewBase]


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    updated_on: datetime
    created_on: datetime

    class Config:
        orm_mode = True
