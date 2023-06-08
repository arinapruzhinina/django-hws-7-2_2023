from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from afisha_app.models.validation import phone_validator


class Viewer(AbstractUser):
    """Overriding the User model with the email field as primary"""

    username = models.CharField(
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "unique": _("A user with that username already exists."),
        }, verbose_name="Username",
        unique=True,
    )

    money = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)],
                                verbose_name="Деньги")
    date_of_birth = models.DateField(_('date of birth'), blank=False, null=True)
    phone = models.CharField(_('phone'), max_length=12, blank=True, null=True, validators=[phone_validator])
    email = models.CharField(_('email'), max_length=64, blank=True, null=True, validators=[EmailValidator()])

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    class Meta:
        db_table = 'viewers'
        app_label = "afisha_app"
        verbose_name = 'Viewer'
        verbose_name_plural = 'Viewers'
