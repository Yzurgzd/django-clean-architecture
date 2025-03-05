from django.urls import path

from library.presentors.rest.routers.api.v1.endpoints.books import (
    create_book,
    delete_book_by_id,
    fetch_book,
    fetch_books,
    update_book_by_id,
)
from library.presentors.rest.routers.api.v1.endpoints.users import (
    create_user,
    delete_user_by_id,
    fetch_user,
    fetch_users,
    update_user_by_id,
)

urlpatterns = [
    path("books/", fetch_books),
    path("books/create/", create_book),
    path("books/<uuid:book_id>/", fetch_book),
    path("books/update/<uuid:book_id>/", update_book_by_id),
    path("books/delete/<uuid:book_id>/", delete_book_by_id),
    path("users/", fetch_users),
    path("users/create/", create_user),
    path("users/<uuid:user_id>/", fetch_user),
    path("users/update/<uuid:user_id>/", update_user_by_id),
    path("users/delete/<uuid:user_id>/", delete_user_by_id),
]
