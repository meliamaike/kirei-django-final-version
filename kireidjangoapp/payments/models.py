from django.db import models
from products.models import Product
from services.models import Service
from customers.models import Customer
from orders.models import Order
from .utils import encrypt, decrypt


"""
    Modelo "Pago": Este modelo tendría campos como monto, fecha, 
    forma de pago, y reserva de la cita asociada.
"""


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    transaction_number = models.BinaryField()
    payment_method = models.CharField(
        max_length=255,
        choices=[
            ("credit_card", "Tarjeta de crédito"),
            ("debit_card", "Tarjeta de débito"),
            ("cash", "Efectivo"),
            ("bank_transfer", "Transferencia bancaria"),
            ("mercado_pago", "Mercado Pago"),
            ("other", "Otro"),
        ],
    )
    status = models.CharField(
        max_length=255,
        choices=[
            ("pending", "Pendiente"),
            ("success", "Exitosa"),
            ("failed", "Fallida"),
            ("refunded", "Reembolsada"),
            ("cancelled", "Cancelada"),
        ],
    )

    @property
    def transaction_number(self):
        return decrypt(self.encrypted_transaction_number)

    @transaction_number.setter
    def transaction_number(self, value):
        self.encrypted_transaction_number = encrypt(value)
