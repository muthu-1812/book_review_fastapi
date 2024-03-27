from fastapi.testclient import TestClient
from src.book_review.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello World"


def test_add_book_invalid_year():
    book_payload = {
        "title": "secret seven 2",
        "author": "Enid Blyton",
        "publication_year": 5000
    }
    response = client.post("/books", json=book_payload)
    assert response.status_code == 422


def test_add_book_already_created():
    book_payload = {"title": "secret seven",
                    "author": "Enid Blyton",
                    "publication_year": 1000
                    }
    response = client.post("/books", json=book_payload)
    assert response.status_code == 409


def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200


def test_get_books_filter_by_author():
    response = client.get("/books/?author=string")
    assert response.status_code == 200


def test_get_books_filter_by_year():
    response = client.get("/books/?year=123")
    assert response.status_code == 200


def test_book_by_valid_id():
    response = client.get("/books/1")
    assert response.status_code == 200


def test_book_by_invalid_id():
    response = client.get("books/1000")
    assert response.status_code == 404


def test_add_valid_review():
    review = {
        "ratings": 5,
        "review": "stringstri",
        "review_author": "string"
    }
    response = client.post("books/1/reviews", json=review)

    assert response.status_code == 200


def test_add_review_less_characters_in_description():
    review = {
        "ratings": 5,
        "review": "stringi",
        "review_author": "string"
    }
    response = client.post("books/1/reviews", json=review)
    assert response.status_code == 422


def test_get_all_reviews_for_one_book():
    response = client.get("books/1/reviews")
    assert response.status_code == 200
