# Generated by Django 4.1.7 on 2023-05-06 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afisha_app', '0004_remove_viewer_phone_alter_viewer_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewer',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='phone'),
        ),
    ]
