import pytest

from library.adapters.database.storages.book import BookStorage
from library.adapters.database.storages.user import UserStorage
from library.domains.interfaces.storages.book import IBookStorage
from library.domains.interfaces.storages.user import IUserStorage


@pytest.fixture
def book_storage() -> IBookStorage:
    return BookStorage()


@pytest.fixture
def user_storage() -> IUserStorage:
    return UserStorage()
