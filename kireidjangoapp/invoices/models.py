from django.db import models
from payments.models import Payment


class Invoice(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to="invoices/")  # cambiarlo luego
