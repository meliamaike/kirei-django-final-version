from django.db import models
from my_payments.models import MyPayment


class Invoice(models.Model):
    payment = models.OneToOneField(MyPayment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to="invoices/")  # cambiarlo luego
