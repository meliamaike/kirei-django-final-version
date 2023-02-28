from django.db import models
from shoppingcarts.models import ShoppingCart
from customers.models import Customer
from products.models import Product


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shopping_cart = models.OneToOneField(ShoppingCart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_total = models.DecimalField(max_digits=6, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_amount = self.shopping_cart.total_amount
        super().save(*args, **kwargs)
