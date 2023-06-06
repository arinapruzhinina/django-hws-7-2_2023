# Generated by Django 4.1.7 on 2023-05-15 10:37

import afisha_app.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afisha_app', '0006_remove_viewer_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewer',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True, validators=[afisha_app.models.phone_validator], verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seat_num',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(1)], verbose_name='seat phone'),
        ),
    ]