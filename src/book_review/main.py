
from fastapi import FastAPI

from src.book_review import models
from src.book_review.database import engine
from src.book_review.routers import book

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(book.router)


@app.get("/")
def hello():
    return "Book Review System"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
