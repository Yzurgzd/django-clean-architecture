from django.db.models import CharField, IntegerField

from library.adapters.database.base import (
    BaseTable,
    IdentifiableMixin,
    TimestampedMixin,
)


class BookTable(BaseTable, TimestampedMixin, IdentifiableMixin):
    title = CharField(max_length=255)
    year = IntegerField()
    author = CharField(max_length=255)

    class Meta:
        db_table = "book"

    def __str__(self) -> str:
        return self.title


class UserTable(BaseTable, TimestampedMixin, IdentifiableMixin):
    username = CharField(max_length=255, unique=True)
    email = CharField(max_length=255, unique=True)

    class Meta:
        db_table = "user"

    def __str__(self) -> str:
        return self.username
