# Generated by Django 4.1.6 on 2023-03-21 03:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("appointments", "0004_remove_appointment_shopping_cart"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appointment",
            name="appointment_slot",
        ),
        migrations.AddField(
            model_name="appointment",
            name="appointment_slot",
            field=models.ManyToManyField(
                related_name="appointment", to="appointments.appointmentslot"
            ),
        ),
    ]