from django.core.exceptions import ValidationError


def phone_validator(phone: str):
    if phone[0] != '+' or phone[1] != '7' or len(phone) != 12:
        raise ValidationError(
            f'The entered phone phone {phone} is incorrect, it must start with +7 and have 12 characters',
            params={'phone': phone}, )


def positive_int(num: int):
    if num <= 0:
        raise ValidationError(
            f'Value {num} is less or equal zero',
            params={'value': num},
        )
