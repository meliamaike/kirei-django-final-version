from django.db import models


class CategoryService(models.Model):
    THREADING = "TH"
    MANICURE = "MN"
    PEDICURE = "PD"
    FACIALS = "FC"
    BROWS = "BW"
    EYELASHES = "EL"
    LIPS = "LP"

    CATEGORY_CHOICES = [
        (THREADING, "Threading"),
        (MANICURE, "Manos"),
        (PEDICURE, "Pies"),
        (FACIALS, "Cuidado de la piel"),
        (BROWS, "Cejas"),
        (EYELASHES, "Pestañas"),
        (LIPS, "Labios"),
    ]

    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)

    def __str__(self):
        return dict(self.CATEGORY_CHOICES)[self.category]



class Service(models.Model):
    service = models.CharField(max_length=200)
    category = models.ForeignKey(CategoryService, on_delete=models.SET_NULL, null=True)
    description = models.TextField(
        verbose_name="Product Description",
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
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "Servicio: {}, Categoria{} - {} ".format(
            self.service, self.category, self.duration
        )
