# Generated by Django 4.1.6 on 2023-03-05 00:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("appointments", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="date",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
