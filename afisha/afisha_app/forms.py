from django.forms import ChoiceField, Form, DecimalField, CharField, EmailField, ModelForm, DateField, IntegerField
from django.contrib.auth import forms as auth_forms
from django.core.validators import MinValueValidator, RegexValidator

from django.contrib.auth import get_user_model
from afisha_app.models.event.models import Event

User = get_user_model()


class AddFundsForm(Form):
    money = DecimalField(
        label='Add money',
        max_digits=10,
        decimal_places=2,
    )


class RegistrationForm(auth_forms.UserCreationForm):
    first_name = CharField(max_length=40, required=True)
    last_name = CharField(max_length=40, required=True)
    email = EmailField(max_length=128, required=True)
    date_of_birth = DateField(required=True, label="Date of birth", input_formats=['%Y-%m-%d'], help_text="Format: YYYY-MM-DD")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'password1', 'password2']


class EventForm(ModelForm):
    tickets_amount = IntegerField(validators=[MinValueValidator(1, message="Количество билетов должно быть больше 0")])
    price = DecimalField(validators=[MinValueValidator(0, message="Цена должна быть больше или равна 0")])

    class Meta:
        model = Event
        fields = ['name', 'description', 'address', 'age_minimum', 'date', 'start_time', 'tickets_amount', 'type',
                  'price']
