from collections.abc import Callable

import factory
import pytest

from library.adapters.database.tables import UserTable


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserTable

    email = factory.Sequence(lambda n: f"email{n}@example.com")
    username = factory.Sequence(lambda n: f"username{n}")
    deleted_at = None


@pytest.fixture
def create_user(db) -> Callable:
    def _factory(**kwargs) -> UserTable:
        user = UserFactory(**kwargs)
        return user

    return _factory
