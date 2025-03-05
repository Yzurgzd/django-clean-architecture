from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol

from library.domains.entities.book import (
    Book,
    BookId,
    BookPaginationParams,
    CreateBook,
    UpdateBook,
)


class IBookStorage(Protocol):
    @abstractmethod
    def fetch_book_by_id(self, *, book_id: BookId) -> Book | None:
        raise NotImplementedError

    @abstractmethod
    def count_books(self, *, params: BookPaginationParams) -> int:
        raise NotImplementedError

    @abstractmethod
    def fetch_book_list(self, *, params: BookPaginationParams) -> Sequence[Book]:
        raise NotImplementedError

    @abstractmethod
    def create_book(self, *, book: CreateBook) -> Book:
        raise NotImplementedError

    @abstractmethod
    def delete_book_by_id(self, *, book_id: BookId) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_book_by_id(self, *, update_book: UpdateBook) -> Book:
        raise NotImplementedError

    @abstractmethod
    def exists_book_by_id(self, *, book_id: BookId) -> bool:
        raise NotImplementedError
