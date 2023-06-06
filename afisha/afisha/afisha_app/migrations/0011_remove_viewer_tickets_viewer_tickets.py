# Generated by Django 4.1.7 on 2023-06-06 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('afisha_app', '0010_rename_viewer_ticket_viewer1_viewer_tickets'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viewer',
            name='tickets',
        ),
        migrations.AddField(
            model_name='viewer',
            name='tickets',
            field=models.ManyToManyField(through='afisha_app.ViewerTicket', to='afisha_app.ticket'),
        ),
    ]