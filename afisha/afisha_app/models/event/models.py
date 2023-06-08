from django.core.validators import MinValueValidator
from django.db import models

from afisha_app.models import BaseMixin
from django.utils.translation import gettext_lazy as _

from afisha_app.models.validation import positive_int


class Event(BaseMixin):
    price = models.DecimalField(
        verbose_name=_('price'),
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=False,
        null=False,
        validators=[MinValueValidator(0)]
    )
    name = models.CharField(_('name'), max_length=40)
    description = models.TextField(_('description'), blank=True, null=True)
    address = models.CharField(_('address'), max_length=100, blank=True, null=True)
    age_minimum = models.IntegerField(_('age limit'), blank=True, null=True, validators=[positive_int])
    date = models.DateField(_('date'), blank=True, null=True)
    start_time = models.TimeField(_('start time'), blank=True, null=True)
    tickets_amount = models.IntegerField(_('ticket amount'), blank=True, null=True, validators=[positive_int])
    viewer = models.ForeignKey('Viewer', on_delete=models.CASCADE, null=True)

    event_types = (
        ('concert', _('conсert')),
        ('performance', _('performance')),
    )

    type = models.CharField(_('type'), max_length=40, choices=event_types, blank=False, null=False)

    def __str__(self):
        return f'{self.name}, {self.type}'

    class Meta:
        db_table = 'events'
        app_label = "afisha_app"
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
