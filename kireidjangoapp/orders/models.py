from django.db import models
from customers.models import Customer
from my_payments.models import CartPayment, AppointmentPayment


class ProductOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(CartPayment, on_delete=models.CASCADE)


class AppointmentOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(AppointmentPayment, on_delete=models.CASCADE)
