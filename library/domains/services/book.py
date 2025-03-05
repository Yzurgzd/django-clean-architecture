from library.application.exceptions import EntityNotFoundException
from library.domains.entities.book import (
    Book,
    BookId,
    BookPagination,
    BookPaginationParams,
    CreateBook,
    UpdateBook,
)
from library.domains.interfaces.storages.book import IBookStorage


class BookService:
    __book_storage: IBookStorage

    def __init__(self, book_storage: IBookStorage) -> None:
        self.__book_storage = book_storage

    def fetch_book_by_id(self, *, book_id: BookId) -> Book:
        book = self.__book_storage.fetch_book_by_id(book_id=book_id)
        if book is None:
            raise EntityNotFoundException(entity=Book, entity_id=book_id)
        return book

    def fetch_book_list(self, *, params: BookPaginationParams) -> BookPagination:
        total = self.__book_storage.count_books(params=params)
        items = self.__book_storage.fetch_book_list(params=params)
        return BookPagination(total=total, items=items)

    def create_book(self, *, book: CreateBook) -> Book:
        return self.__book_storage.create_book(book=book)

    def delete_book_by_id(self, *, book_id: BookId) -> None:
        if not self.__book_storage.exists_book_by_id(book_id=book_id):
            raise EntityNotFoundException(entity=Book, entity_id=book_id)
        self.__book_storage.delete_book_by_id(book_id=book_id)

    def update_book_by_id(self, *, update_book: UpdateBook) -> Book:
        if not self.__book_storage.exists_book_by_id(book_id=update_book.id):
            raise EntityNotFoundException(entity=Book, entity_id=update_book.id)
        return self.__book_storage.update_book_by_id(update_book=update_book)
