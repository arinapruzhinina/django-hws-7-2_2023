from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from afisha_app.models import BaseMixin
from django.utils.translation import gettext_lazy as _


class Ticket(BaseMixin):
    row = models.IntegerField(_('row'), blank=True, null=True, validators=[MaxValueValidator(11), MinValueValidator(1)])
    seat_num = models.IntegerField(_('seat number'), blank=True, null=True,
                                   validators=[MaxValueValidator(20), MinValueValidator(1)])
    viewer = models.ForeignKey('Viewer', on_delete=models.CASCADE, null=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.event}, {self.id}'

    class Meta:
        db_table = 'tickets'
        app_label = "afisha_app"
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['id']

    def validate_ticket(self):
        try:
            ticket_amount = Ticket.objects.all().filter(row=self.row, seat_num=self.seat_num, event__id=self.event.id)
        except ObjectDoesNotExist:
            return False

        for amount in ticket_amount:
            if (amount.row == self.row and amount.seat_num == self.seat_num):
                return False
        return True

    def validate_seat_performance(self):
        return self.row and self.seat_num

    def validate_ticket_concert(self):
        return self.row != None or self.seat_num != None

    def clean(self):
        super().clean()
        if self.event.type == 'concert':
            if self.validate_ticket_concert():
                raise ValidationError(
                    'There are no seats at this concert. Leave the row and seat num fields blank',
                    params={'row': self.row, 'seat_num': self.seat_num},
                )
        if self.event.type == 'performance':
            if not self.validate_ticket():
                raise ValidationError(
                    'This seat are already taken',
                    params={'row': self.row, 'seat_num': self.seat_num},
                )
            if not self.validate_seat_performance():
                raise ValidationError(
                    'Both "row" and "seat number" fields must be presente',
                    params={'row': self.row, 'seat_num': self.seat_num}
                )
        age = self.viewer.age()
        if age < self.event.age_minimum:
            raise ValidationError(
                'Viewer is not old enough to attend this event',
                params={'age': age, 'min_age': self.event.age_minimum},
            )
