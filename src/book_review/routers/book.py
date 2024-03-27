from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import status

from src.book_review import schemas, crud
from src.book_review.database import get_db

router = APIRouter(
    prefix="/books",
    tags=['Books']
)


@router.post("/", response_model=schemas.BookCreate, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    :param book: Book data provided to create the book
    :param db: Db connection
    :return: BookId of newly created book
    """
    try:
        book = crud.create_book(db, book)
        return book

    except IntegrityError as e:
        raise HTTPException(status_code=409, detail="Integrity Error: {}".format(str(e)))


@router.get("/", response_model=list[schemas.Book])
def get_books(author: Annotated[str | None, Query(max_length=50)] = None,
              year: int | None = None,
              skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    :param author: Optional parameter to filter books by author
    :param year:  Optional parameter to filter books by year of publication
    :param skip:  Optional parameter for pagination
    :param limit: Optional parameter for pagination
    :return: List of books
    """

    books = crud.get_books(db, publication_year=year, author_name=author, skip=skip, limit=limit)
    return books


@router.get("/{book_id}", response_model=schemas.BookOut)
def read_book_by_id(book_id: int, db: Session = Depends(get_db)):
    """
        Read book by ID.
        Parameters:
            book_id (int): The ID of the book to read.
        Returns:
            dict: A dictionary with book details and reviews of one book.
        """
    book = crud.get_book_by_id(db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


def send_mock_email(email_id: str, message=""):
    """Dummy email simulation function
    writing to a text file for now"""
    with open("mock_email.txt", mode="a") as email_file:
        content = f"Sending email to {email_id} the following message: {message}\n"
        email_file.write(content)


@router.post("/{book_id}/reviews/", response_model=schemas.ReviewCreate)
def create_review_for_book(book_id: int, review: schemas.ReviewCreate, background_tasks: BackgroundTasks,
                           db: Session = Depends(get_db)):
    """
    Endpoint to add reviews to a book and send email notification to the reviewer

    :param book_id:Book id for which review is to be added
    :param review:Review body with rating and the review
    :param background_tasks:Used for sending email to reviewer
    :param db:Db connection
    :return:
    """
    book = crud.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    review = crud.create_review(db=db, review=review, book_id=book_id)
    email_id = review.reviewer_email
    if email_id:
        background_tasks.add_task(send_mock_email, email_id,
                                  message=f"Hi {review.review_author} thanks for reviewing the book {book.title}")

    return review


@router.get("/{book_id}/reviews/", response_model=list[schemas.Review])
def read_reviews_by_book(book_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint to fetch all reviews for a particular book

    :param book_id:Book id for which reviews are to be fetched
    :param skip: Optional parameter for pagination offset
    :param limit:Optional parameter for pagination limit
    :param db:Default parameter for db connection
    :return: List of reviews for a book
    """

    book = crud.get_book_by_id(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    reviews = crud.get_reviews(db, book_id=book_id, skip=skip, limit=limit)
    return reviews
