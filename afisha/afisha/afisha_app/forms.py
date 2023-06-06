from django.forms import ChoiceField, Form, DecimalField, CharField, EmailField
from django.contrib.auth import forms as auth_forms, models as auth_models



class AddFundsForm(Form):
    money = DecimalField(
        label='Amount',
        max_digits=10,
        decimal_places=2,
    )

class RegistrationForm(auth_forms.UserCreationForm):
    first_name = CharField(max_length=40, required=True)
    last_name = CharField(max_length=40, required=True)
    email = EmailField(max_length=128, required=True)

    class Meta:
        model = auth_models.User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']