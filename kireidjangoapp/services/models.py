from django.db import models


class CategoryService(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.category


class Service(models.Model):
    service = models.CharField(max_length=200)
    category = models.ForeignKey(CategoryService, on_delete=models.SET_NULL, null=True)
    description = models.TextField(
        verbose_name="Descripción del producto",
        blank=True,
        default="",
        help_text="Ingrese una breve descripción del servicio.",
    )
    duration = models.IntegerField(
        choices=[
            (30, "30 min"),
            (60, "60 min"),
            (90, "90 min"),
            (120, "120 min"),
            (150, "150 min"),
            (180, "180 min"),
        ]
    )
    price = models.DecimalField(max_digits=15, decimal_places=0)

    def __str__(self):
        return "{} - {} - {} mins ".format(self.category, self.service, self.duration)

    def get_type(self):
        return "Service"

