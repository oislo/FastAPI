from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from enum import Enum
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    descriptions: Optional[str] = Field(title="Description of the book", min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            "example": {
                "id": "l1ed74ba-dc19-4622-93fc-3bc5b05bd995",
                "title": "Kur qau Nicja",
                "author": "Irvin D. Yalom",
                "descriptions": "A nice description of the book",
                "rating": "75"
            }
        }


BOOKS = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Books number {exception.books_to_return} ??"}
    )


@app.get("/")
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)
    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[ i - 1])
            i += 1
        return new_books
    return BOOKS


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()


@app.put("/{book_id}")
async def book_id_book(book_id: UUID, book: Book):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    raise raise_item_cannot_be_found_exception()


@app.post("/")
async def create_book(book: Book):
    BOOKS.append(book)
    return book



@app.delete("/{book_id}")
async def delete_book(book_id: UUID):
    counter = 0
    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f"Book with ID {book_id} was deleted!"
    raise raise_item_cannot_be_found_exception()


def create_books_no_api():
    book_1 = Book(id='53408a4a-1321-4070-9936-937e220257b4',
            title="Title 1",
            author="Author 1",
            descriptions="Desc 1",
            rating=60)
    book_2 = Book(id='d44d95e9-8f4c-4c73-ac3a-e03a14b58464',
            title="Title 2",
            author="Author 2",
            descriptions="Desc 2",
            rating=70)
    book_3 = Book(id='da0281e6-6501-488d-ab02-15749427e74a',
            title="Title 3",
            author="Author 3",
            descriptions="Desc 3",
            rating=80)
    book_4 = Book(id='e1ed74ba-dc19-4622-93fc-3bc5b05bd995',
            title="Title 4",
            author="Author 4",
            descriptions="Desc 4",
            rating=50)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404, detail="Book not found", headers={"X_Header-Error": "Nothing to be seen at the UUID"})