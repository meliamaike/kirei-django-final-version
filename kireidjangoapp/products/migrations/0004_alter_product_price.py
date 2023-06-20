# Generated by Django 3.2.18 on 2023-05-19 21:41

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(
                decimal_places=2, default=Decimal("0.00"), max_digits=15
            ),
        ),
    ]