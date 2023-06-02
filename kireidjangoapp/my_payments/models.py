from django.db import models
from django.urls import reverse

# from orders.models import Order
from products.models import Product
from payments.models import BasePayment, PurchasedItem
from appointments.models import Appointment
from decimal import Decimal


class AppointmentPayment(BasePayment):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True)
    payment_method = models.CharField(max_length=30)
    id_mercado_pago = models.CharField(max_length=30, null=True)
    total = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )

    def get_failure_url(self):
        """
        Return the URL where users will be redirected after a failed attempt to complete a payment.
        """
        return reverse("my_payments:payment_failed", args=[self.id])

    def get_success_url(self):
        """
        Return the URL where users will be redirected after a successful payment.
        """
        return reverse("my_payments:payment_success", args=[self.id])

    def get_purchased_items(self):
        """
        Return an iterable of purchased items.
        """
        items = []
        for item in self.order.shopping_cart.items.all():
            purchased_item = PurchasedItem(
                name=item.product.name,
                quantity=item.quantity,
                price=item.product.price,
                currency="ARS",
            )
            items.append(purchased_item)
        return items


class CartPayment(BasePayment):
    cart_products = models.ManyToManyField(Product, through="ProductPayment")
    payment_method = models.CharField(max_length=30)
    id_mercado_pago = models.CharField(max_length=30, null=True)
    cart_total = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )


class ProductPayment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_payment = models.ForeignKey(CartPayment, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )
