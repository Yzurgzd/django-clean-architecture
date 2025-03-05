from uuid import UUID

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from library.application.exceptions import EmptyPayloadException
from library.domains.entities.user import (
    CreateUser,
    UpdateUser,
    UserId,
    UserPaginationParams,
)
from library.domains.use_cases.commands.user.create_user import CreateUserCommand
from library.domains.use_cases.commands.user.delete_user_by_id import (
    DeleteUserByIdCommand,
)
from library.domains.use_cases.commands.user.update_user_by_id import (
    UpdateUserByIdCommand,
)
from library.domains.use_cases.queries.user.fetch_user_by_id import FetchUserByIdQuery
from library.domains.use_cases.queries.user.fetch_user_list import FetchUserListQuery
from library.presentors.rest.routers.api.v1.schemas.users import (
    CreateUserSchema,
    UpdateUserSchema,
    UserPaginationParamsSchema,
    UserPaginationSchema,
    UserSchema,
)
from library.utils.dishka_integration import FromDishka, inject


@api_view(["GET"])
@inject
def fetch_users(
    request: Request,
    *,
    fetch_user_list: FromDishka[FetchUserListQuery],
) -> UserPaginationSchema:
    params = UserPaginationParamsSchema(**request.query_params)
    users = fetch_user_list.execute(
        input_dto=UserPaginationParams(limit=params.limit, offset=params.offset)
    )
    return Response(
        UserPaginationSchema.model_validate(users).model_dump(),
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@inject
def create_user(
    request: Request,
    *,
    create_user: FromDishka[CreateUserCommand],
) -> UserSchema:
    create_user_data = CreateUserSchema(**request.data)
    user = create_user.execute(
        input_dto=CreateUser(
            username=create_user_data.username,
            email=create_user_data.email,
        )
    )
    return Response(
        UserSchema.model_validate(user).model_dump(), status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
@inject
def fetch_user(
    request: Request,
    user_id: UUID,
    *,
    fetch_user_by_id: FromDishka[FetchUserByIdQuery],
) -> UserSchema:
    user = fetch_user_by_id.execute(input_dto=UserId(user_id))
    return Response(
        UserSchema.model_validate(user).model_dump(), status=status.HTTP_200_OK
    )


@api_view(["PATCH"])
@inject
def update_user_by_id(
    request: Request,
    user_id: UUID,
    *,
    update_user: FromDishka[UpdateUserByIdCommand],
) -> UserSchema:
    update_user_data = UpdateUserSchema(**request.data)
    values = update_user_data.model_dump(exclude_unset=True)
    if not values:
        raise EmptyPayloadException(message="No values to update")
    user = update_user.execute(
        input_dto=UpdateUser(
            id=UserId(user_id),
            **values,
        )
    )
    return Response(
        UserSchema.model_validate(user).model_dump(), status=status.HTTP_200_OK
    )


@api_view(["DELETE"])
@inject
def delete_user_by_id(
    request: Request,
    user_id: UUID,
    *,
    delete_user_by_id: FromDishka[DeleteUserByIdCommand],
) -> None:
    delete_user_by_id.execute(input_dto=UserId(user_id))
    return Response(status=status.HTTP_204_NO_CONTENT)
