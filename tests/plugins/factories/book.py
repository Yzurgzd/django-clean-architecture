from collections.abc import Callable

import factory
import pytest

from library.adapters.database.tables import BookTable


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookTable

    title = factory.Faker("sentence")
    author = factory.Faker("name")
    published_date = factory.Faker("date")
    deleted_at = None


@pytest.fixture
def create_book(db) -> Callable:
    def _factory(**kwargs) -> BookTable:
        book = BookFactory(**kwargs)
        return book

    return _factory
