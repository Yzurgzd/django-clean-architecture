__all__ = [
    "FromDishka",
    "inject",
]

from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from dishka import FromDishka, make_container
from dishka.integrations.base import wrap_injection
from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.request import Request

from library.adapters.database.di import DatabaseProvider
from library.domains.di import DomainProvider

T = TypeVar("T")
P = ParamSpec("P")


def inject(func: Callable[P, T]) -> Callable[[Request, P.args, P.kwargs], T]:
    @wraps(func)
    def wrapper(request: Request, *args: P.args, **kwargs: P.kwargs) -> T:
        dishka_container = request.dishka_container
        with dishka_container() as container:
            injected_func = wrap_injection(
                func=func,
                container_getter=lambda _, p: container,
                is_async=False,
            )
            return injected_func(request, *args, **kwargs)

    return wrapper


class ContainerMiddleware(MiddlewareMixin):
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response
        self.container = make_container(
            DatabaseProvider(debug=False), DomainProvider()
        )  # TODO: make an argument

    def __call__(self, request: Request) -> HttpResponse:
        request.dishka_container = self.container

        response = self.get_response(request)

        return response
