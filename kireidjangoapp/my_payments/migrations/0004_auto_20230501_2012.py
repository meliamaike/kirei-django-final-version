# Generated by Django 3.2.18 on 2023-05-01 23:12

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("my_payments", "0003_cartpayment_cart_total"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appointmentpayment",
            name="area_code",
        ),
        migrations.RemoveField(
            model_name="appointmentpayment",
            name="document_number",
        ),
    ]
