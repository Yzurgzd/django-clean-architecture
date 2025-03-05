import importlib

from django.apps import AppConfig


class DatabaseConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "library.adapters.database"

    def ready(self) -> None:
        importlib.import_module("library.adapters.database.tables")
