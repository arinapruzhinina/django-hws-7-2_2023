# Generated by Django 4.1.7 on 2023-05-05 20:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afisha_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='row',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(11), django.core.validators.MinValueValidator(0)], verbose_name='row'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seat_num',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)], verbose_name='seat number'),
        ),
    ]