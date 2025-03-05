import pytest
from django.test import Client


@pytest.fixture
def client(db) -> Client:
    return Client()
