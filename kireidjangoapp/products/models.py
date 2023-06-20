from django.db import models
from decimal import Decimal


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("cuidado-facial", "Cuidado de la Piel"),
        ("maquillaje", "Maquillaje"),
        ("cuidado-corporal", "Cuidado Corporal"),
        ("perfumes", "Perfumes"),
        ("labios", "Labios"),
        ("cejas", "Cejas"),
        ("ojos", "Ojos"),
        ("nails", "Nails"),
        ("accesorios", "Accesorios"),
        ("baño-y-ducha", "Baño y Ducha"),
        ("exfoliantes", "Exfoliantes"),
        ("hidratantes", "Hidratantes"),
        ("aceites", "Aceites"),
        ("protectores-solares", "Protectores Solares"),
        ("manos", "Manos"),
        ("pies", "Pies"),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(
        verbose_name="Descripcion del producto",
        default="",
        help_text="Ingrese una breve descripción del producto.",
    )
    price = models.DecimalField(max_digits=15, decimal_places=0, default="")
    stock = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="products/images")
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, default="")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0

    def get_type(self):
        return "Product"
