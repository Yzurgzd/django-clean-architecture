from dishka import BaseScope, Component, Provider, Scope, provide

from library.adapters.database.storages.book import BookStorage
from library.domains.interfaces.storages.book import IBookStorage


class DatabaseProvider(Provider):
    def __init__(
        self,
        debug: bool,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ) -> None:
        self.debug = debug
        super().__init__(scope=scope, component=component)

    @provide(scope=Scope.REQUEST)
    def book_storage(self) -> IBookStorage:
        return BookStorage()
