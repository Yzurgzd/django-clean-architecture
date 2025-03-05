from uuid import UUID

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from library.application.exceptions import EmptyPayloadException
from library.domains.entities.book import (
    BookId,
    BookPaginationParams,
    CreateBook,
    UpdateBook,
)
from library.domains.use_cases.commands.book.create_book import CreateBookCommand
from library.domains.use_cases.commands.book.delete_book_by_id import (
    DeleteBookByIdCommand,
)
from library.domains.use_cases.commands.book.update_book_by_id import (
    UpdateBookByIdCommand,
)
from library.domains.use_cases.queries.book.fetch_book_by_id import FetchBookByIdQuery
from library.domains.use_cases.queries.book.fetch_book_list import FetchBookListQuery
from library.presentors.rest.routers.api.v1.schemas.books import (
    BookPaginationParamsSchema,
    BookPaginationSchema,
    BookSchema,
    CreateBookSchema,
    UpdateBookSchema,
)
from library.utils.dishka_integration import FromDishka, inject


@api_view(["GET"])
@inject
def fetch_books(
    request: Request,
    *,
    fetch_book_list: FromDishka[FetchBookListQuery],
) -> BookPaginationSchema:
    params = BookPaginationParamsSchema(**request.query_params)
    book = fetch_book_list.execute(
        input_dto=BookPaginationParams(limit=params.limit, offset=params.offset)
    )
    return Response(
        BookPaginationSchema.model_validate(book).model_dump(),
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@inject
def create_book(
    request: Request,
    *,
    create_book: FromDishka[CreateBookCommand],
) -> BookSchema:
    create_book_data = CreateBookSchema(**request.data)
    book = create_book.execute(
        input_dto=CreateBook(
            title=create_book_data.title,
            year=create_book_data.year,
            author=create_book_data.author,
        )
    )
    return Response(
        BookSchema.model_validate(book).model_dump(), status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
@inject
def fetch_book(
    request: Request,
    book_id: UUID,
    *,
    fetch_book_by_id: FromDishka[FetchBookByIdQuery],
) -> BookSchema:
    book = fetch_book_by_id.execute(input_dto=BookId(book_id))
    return Response(
        BookSchema.model_validate(book).model_dump(), status=status.HTTP_200_OK
    )


@api_view(["PATCH"])
@inject
def update_book_by_id(
    request: Request,
    book_id: UUID,
    *,
    update_book: FromDishka[UpdateBookByIdCommand],
) -> BookSchema:
    update_book_data = UpdateBookSchema(**request.data)
    values = update_book_data.model_dump(exclude_unset=True)
    if not values:
        raise EmptyPayloadException(message="No values to update")
    book = update_book.execute(
        input_dto=UpdateBook(
            id=BookId(book_id),
            **values,
        )
    )
    return Response(
        BookSchema.model_validate(book).model_dump(), status=status.HTTP_200_OK
    )


@api_view(["DELETE"])
@inject
def delete_book_by_id(
    request: Request,
    book_id: UUID,
    *,
    delete_book_by_id: FromDishka[DeleteBookByIdCommand],
) -> None:
    delete_book_by_id.execute(input_dto=BookId(book_id))
    return Response(status=status.HTTP_204_NO_CONTENT)
