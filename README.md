# book_review_fastapi
RESTful API using FastAPI for a hypothetical book review system.

# Book Review System using FastAPI

#### This API  has 1 route

## 1) Book route

#### This route is reponsible for creating a book, viewing a list of books(you can filter by author or publication year) it also has nested endpoints for creating reviews for each book and viewing them as well.


# How to run locally
First clone this repo by using following command
````

git clone https://github.com/muthu-1812/book_review_fastapi.git

````
then 
````

cd src/book_review

````

Then install requirements

````

pip install requirements.txt

````

Then go this repo folder in your local computer run follwoing command
````

uvicorn main:app --reload

````

Then you can use following link to use the  API

````

http://127.0.0.1:8000/docs 

````
