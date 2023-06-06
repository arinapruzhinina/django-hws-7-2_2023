from typing import Collection, Optional
from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.conf.global_settings import AUTH_USER_MODEL
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator
from datetime import date



class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)

    class Meta:
        abstract = True

class CreatedMixin(models.Model):
    created = models.DateTimeField(_('created'), default=datetime.now, blank=True, null=False)

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(_('modified'), default=datetime.now, blank=True, null=False)

    class Meta:
        abstract = True


def positive_int(num: int):
    if num <= 0:
        raise ValidationError(
            f'Value {num} is less or equal zero',
            params={'value': num},
        )
    
event_types = (
    ('concert', _('conсert')),
    ('performance', _('performance')),
)




class Event(UUIDMixin, CreatedMixin, ModifiedMixin):
    price =  models.DecimalField(
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
    address = models.CharField(_('address'),max_length=100, blank=True, null=True)
    age_minimum = models.IntegerField(_('age limit'), blank=True, null=True, validators=[positive_int])
    date = models.DateField(_('date'), blank=True, null=True)
    start_time = models.TimeField(_('start time'), blank=True, null=True)
    tickets_amount = models.IntegerField(_('ticket amount'), blank=True, null=True, validators=[positive_int])
    type = models.CharField(_('type'), max_length=40, choices=event_types, blank=False, null=False)

    def __str__(self):

        return f'{self.name}, {self.type}'

    class Meta:
        db_table = '"afisha"."event"'
        verbose_name = _('event')
        verbose_name_plural = _('events')

    

class Ticket(UUIDMixin, CreatedMixin, ModifiedMixin):
    price =  models.DecimalField(
        verbose_name=_('price'),
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=False,
        null=False, 
        validators=[MinValueValidator(0)]
    )
    row = models.IntegerField(_('row'), blank=True, null=True, validators=[MaxValueValidator(11), MinValueValidator(1)])
    seat_num = models.IntegerField(_('seat number'),blank=True, null=True, validators=[MaxValueValidator(20), MinValueValidator(1)])
    users = models.ForeignKey('Viewer', on_delete=models.CASCADE, null=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return f'{self.event}, {self.id}'
    
    class Meta:
        db_table = '"afisha"."ticket"'
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')
    
    

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
        if self.event.type == 'performance' :
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
        age = self.users.age()
        if age < self.event.age_minimum:
            raise ValidationError(
                    'Viewer is not old enough to attend this event', 
                    params={'age': age, 'min_age': self.event.age_minimum},
                )
        

class EventTicket(UUIDMixin, CreatedMixin):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    class Meta:
        db_table = '"afisha"."event_ticket"'
        unique_together = (('event', 'ticket'),)

def phone_validator(phone: str):
        if phone[0] != '+' or phone[1] != '7' or len(phone) != 12:
            raise ValidationError(
            f'The entered phone phone {phone} is incorrect, it must start with +7 and have 12 characters', 
            params={'phone': phone},)
        
class Viewer(CreatedMixin, ModifiedMixin, models.Model):

    
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    money = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0, 
        validators=[MinValueValidator(0)]
    )
    # name = models.CharField(_('name'), max_length=40, blank=False, null=True)
    # surname = models.CharField(_('surname'), max_length=40, blank=False, null=True)
    date_of_birth = models.DateField(_('date of birth'),blank=False, null=True )
    phone = models.CharField(_('phone'), max_length=12, blank=True, null=True, validators=[phone_validator])
    email = models.CharField(_('email'), max_length=64, blank=True, null=True, validators=[EmailValidator()])
    tickets = models.ManyToManyField(Ticket, through='ViewerTicket')
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    class Meta:
        db_table = '"afisha"."viewer"'
        verbose_name = _('viewer')
        verbose_name_plural = _('viewers')
    
    def clean(self):
        super().clean()
        now = date.today()
        if self.date_of_birth > now:
            raise ValidationError(
                    'Your date of birth is not correct. Try one more time.', 
                    params={'date_of_birth': self.date_of_birth},
                )
        
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    
   
class ViewerTicket(UUIDMixin, CreatedMixin):
    viewer = models.ForeignKey(Viewer, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    class Meta:
        db_table = '"afisha"."viewer_ticket"'
        unique_together = (('viewer', 'ticket'),)