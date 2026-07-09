from fastapi import FastAPI

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
    print(book_author)
    print(category)
    books_to_return = []
    for book in BOOKS:
        print(book.get('author')) 
        if (book.get('author').casefold() == book_author.casefold()) and (book.get('catetory').casefold() == category.casefold()):
            books_to_return.append(book)
    return books_to_return


