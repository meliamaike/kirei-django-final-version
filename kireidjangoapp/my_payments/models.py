from django.db import models
from django.urls import reverse
from orders.models import Order

from payments.models import BasePayment, PurchasedItem

class MyPayment(BasePayment):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


    def get_failure_url(self):
        """
        Return the URL where users will be redirected after a failed attempt to complete a payment.
        """
        return reverse('my_payments:payment_failed', args=[self.id])

    def get_success_url(self):
        """
        Return the URL where users will be redirected after a successful payment.
        """
        return reverse('my_payments:payment_success', args=[self.id])

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
                currency='USD'
            )
            items.append(purchased_item)
        return items


    



    

