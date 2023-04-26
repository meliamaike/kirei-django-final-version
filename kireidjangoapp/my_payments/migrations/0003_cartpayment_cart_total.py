# Generated by Django 4.1.6 on 2023-04-17 05:01

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("my_payments", "0002_alter_appointmentpayment_total"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartpayment",
            name="cart_total",
            field=models.DecimalField(
                decimal_places=2, default=Decimal("0.00"), max_digits=8
            ),
        ),
    ]