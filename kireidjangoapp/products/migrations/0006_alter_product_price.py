# Generated by Django 3.2.18 on 2023-05-22 04:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0005_auto_20230522_0047"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=0, default="", max_digits=15),
        ),
    ]
