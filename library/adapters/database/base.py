import uuid

from django.db import models


class BaseTable(models.Model):
    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["id"],
                name="uq__%(class)s__id",
            ),
        ]
        indexes = [
            models.Index(
                fields=["created_at"],
                name="ix__%(class)s__created_at",
            ),
        ]

class TimestampedMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True

class IdentifiableMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
