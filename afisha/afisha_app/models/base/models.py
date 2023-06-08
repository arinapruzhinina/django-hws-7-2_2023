from uuid import uuid4

from django.db import models


class BaseMixin(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=False, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=False, verbose_name='Дата обновления')

    class Meta:
        abstract = True
