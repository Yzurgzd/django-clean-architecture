from http import HTTPStatus

import pytest
from dirty_equals import IsDict, IsStr
from django.test import Client

from library.adapters.database.tables import BookTable

API_URL = "/api/v1/books/create/"


@pytest.mark.parametrize(
    "json_data",
    [
        {"title": "Test book"},
        {"author": "Test author"},
        {"title": "Test book", "author": "Test author"},
    ],
)
def test_create_book_incorrect_data(client: Client, json_data):
    response = client.post(API_URL, json_data)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_book_ok_status(client: Client):
    response = client.post(
        API_URL,
        {
            "title": "Test book",
            "author": "Test author",
            "year": 2024,
        },
        content_type="application/json",
    )
    assert response.status_code == HTTPStatus.CREATED


def test_create_book_ok_format(client: Client):
    response = client.post(
        API_URL,
        {
            "title": "Test book",
            "author": "Test author",
            "year": 2024,
        },
        content_type="application/json",
    )
    assert response.json() == {
        "id": IsStr(),
        "title": "Test book",
        "author": "Test author",
        "year": 2024,
        "created_at": IsStr(),
        "updated_at": IsStr(),
    }


def test_create_book_ok_check_db(client: Client):
    response = client.post(
        API_URL,
        {
            "title": "Test book",
            "author": "Test author",
            "year": 2024,
        },
        content_type="application/json",
    )
    db_book = BookTable.objects.get(id=response.json()["id"])
    assert response.json() == IsDict(
        {
            "id": str(db_book.id),
            "title": db_book.title,
            "author": db_book.author,
            "year": db_book.year,
            "created_at": IsStr(),
            "updated_at": IsStr(),
        }
    )


def test_create_book_duplicate_conflict(client: Client):
    book_data = {
        "title": "Test book",
        "author": "Test author",
        "year": 2024,
    }
    client.post(API_URL, book_data)
    response = client.post(API_URL, book_data)
    assert response.status_code == HTTPStatus.CONFLICT
