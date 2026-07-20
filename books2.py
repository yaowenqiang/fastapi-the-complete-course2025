from email.quoprimime import body_check
from pydantic import BaseModel

import uvicorn
from fastapi import FastAPI, Body
from pygments.lexers import func

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id,title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: int
    title: str
    author: str
    description: str
    rating: int


BOOKS = [
    Book(1,'computer science pro', 'codingwithruby', 'a very nice book', 5),
    Book(2, 'be fast with fastapi', 'codingwithruby', 'a great book', 5),
    Book(3, 'master endpoints', 'codingwithruby', 'a awesome book', 5),
    Book(4, 'HP1', 'author 1', 'book description', 2),
    Book(5, 'HP2', 'author 2', 'book description', 3),
    Book(6, 'HP3', 'author 3', 'book description', 1),
    Book(7, 'HP4', 'author 4', 'book description', 4),
    Book(8, 'HP5', 'author 5', 'book description', 4),
]

@app.get('/books')
async def read_all_books():
    return BOOKS

# @app.post('/create-book')
# async def create_book(book_request=Body()):
#     BOOKS.append(book_request)

@app.post('/create-book')
async def create_book(book_request=BookRequest):
    new_book = Book(**book_request.dict())
    # new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)


if __name__ == "__main__":
    uvicorn.run('books2:app', host="0.0.0.0", port=8001, reload=True)
