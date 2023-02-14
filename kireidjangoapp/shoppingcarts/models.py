from django.db import models
from products.models import Product


class ShoppingCart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_amount = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_amount = 0
        for product in self.cart_products.all():
            self.total_amount += product.quantity * product.product.price
        super().save(*args, **kwargs)


# Para tener un control de la cantidad
class ShoppingCartProduct(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
