from typing import Optional

from pydantic import BaseModel, Field

import uvicorn
from fastapi import FastAPI, Path, Query
from pygments.lexers import func

from main import BOOKS

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id,title, author, description, rating, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None, gt=0)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    publish_date: int = Field(gt=1999, lt=2031)


class Config:
    schema_extra = {
        'example': {
            'title': 'A new book',
            'author': 'jacky',
            'description': 'a new description of a book',
            'rating': 5,
            'publish_date': 2029
        }
    }

class BookIdRequest(BaseModel):
    id: int = Field(gt=0)


def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    # return book
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book

BOOKS = [
    Book(1,'computer science pro', 'codingwithruby', 'a very nice book', 5, 2000),
    Book(2, 'be fast with fastapi', 'codingwithruby', 'a great book', 5, 2001),
    Book(3, 'master endpoints', 'codingwithruby', 'a awesome book', 5,2022),
    Book(4, 'HP1', 'author 1', 'book description', 2,2023),
    Book(5, 'HP2', 'author 2', 'book description', 3,2024),
    Book(6, 'HP3', 'author 3', 'book description', 1,2025),
    Book(7, 'HP4', 'author 4', 'book description', 4, 2026),
    Book(8, 'HP5', 'author 5', 'book description', 4, 2027),
]

@app.get('/books')
async def read_all_books():
    return BOOKS

@app.get('/books/publish')
async def read_book_by_publish_date(publish_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.publish_date == publish_date:
            books_to_return.append(book)

    return books_to_return

@app.get('/books/{book_id}')
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

# @app.post('/create-book')
# async def create_book(book_request=Body()):
#     BOOKS.append(book_request)

@app.get('/books/')
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return

@app.post('/create-book')
async def create_book(book_request:BookRequest):
    print(book_request.model_dump())
    # new_book = Book(**book_request.model_dump())
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

@app.put('/books/update-book')
async def update_book(book:BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            break

@app.delete('/books/{book_id}')
async def delete_book(book_id:int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break


if __name__ == "__main__":
    uvicorn.run('books2:app', host="0.0.0.0", port=8001, reload=True)
