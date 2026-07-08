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


