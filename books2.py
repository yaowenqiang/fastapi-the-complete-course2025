from typing import Optional

from pydantic import BaseModel, Field

import uvicorn
from fastapi import FastAPI
from pygments.lexers import func

from main import BOOKS

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
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=5)

def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    # return book
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

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
async def create_book(book_request:BookRequest):
    print(book_request.model_dump())
    # new_book = Book(**book_request.model_dump())
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


if __name__ == "__main__":
    uvicorn.run('books2:app', host="0.0.0.0", port=8001, reload=True)
