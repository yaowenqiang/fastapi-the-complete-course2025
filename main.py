from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {
        'title':'title One',
        'author':'author One',
        'category':'science',
    },
    {
        'title':'title two',
        'author':'author two',
        'category':'science',
    },
    {
        'title':'title three',
        'author':'author three',
        'category':'history',
    },
    {
        'title':'title four',
        'author':'author four',
        'category':'math',
    },
    {
        'title':'title five',
        'author':'author five',
        'category':'math',
    },
    {
        'title':'titleSix',
        'author':'authorsix',
        'category':'math',
    },
]


@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.get('/api-endpoint')
async def first_api():
    return {'message':'Hello! Eric!'}
@app.get('/books')
async def read_all_books():
    return BOOKS


@app.get('/books/mybook')
async def read_my_books():
    return {'book_title': 'my favorite book!'}

#@app.get('/books/{book_title}')
#async def read_book(book_title: str):
#    for book in BOOKS:
#        if book.get('title').casefold() == book_title.casefold():
#            return book

#@app.get('/books/{dynamic_param}')
#async def read_all_books(dynamic_param):
#    return {'dynamic_param': dynamic_param}


@app.get('/books/{book_author}')
async def read_category_by_query(book_author: str,category: str):
    books_to_return = []
    for book in BOOKS:
        if (book.get('author').casefold() == book_author.casefold()) and (book.get('category').casefold() == category.casefold()):
            books_to_return.append(book)
    return books_to_return


@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return new_book

@app.put('/books/update_book')
async def update_book(updated_book=Body()):
    print(updated_book)
    for i in range(len(BOOKS)):
        title = update_book.get('title','').casefold()
        if BOOKS[i].get('title').casefold() == title:
            BOOKS[i] = updated_book
