# Generated by Django 4.1.7 on 2023-05-16 10:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afisha_app', '0007_viewer_phone_alter_ticket_seat_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='address'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='price'),
        ),
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
        migrations.AlterField(
            model_name='viewer',
            name='money',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
