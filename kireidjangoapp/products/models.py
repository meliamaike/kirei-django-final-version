from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(
        verbose_name="Descripcion del producto",
        blank=True,
        default="",
        help_text="Ingrese una breve descripción del producto.",
    )
    price = models.FloatField()
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to="products/static/images"
    )  # modificar ruta de guardado de imagen

    category = models.CharField(max_length=255, default="")
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def is_in_stock(self):
        return self.stock > 0
    
    def get_type(self):
        return 'Product'
