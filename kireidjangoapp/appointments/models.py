import datetime
from django.db import models
from django.forms import ValidationError
from services.models import Service
from professionals.models import Professional
from shoppingcarts.models import ShoppingCart
from customers.models import Customer
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

"""
Los horarios disponibles de la Agenda del día y si estan disponibles o no.
"""


class AppointmentSlot(models.Model):
    agenda = models.ForeignKey("agendas.Agenda", on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    booked = models.BooleanField(default=False)


class Appointment(models.Model):
    # shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    appointment_slot = models.ManyToManyField(
        AppointmentSlot, related_name="appointment"
    )

    @property
    def start_time(self):
        start_times = [slot.start_time for slot in self.appointment_slot.all()]
        return min(start_times) if start_times else None

    @property
    def end_time(self):
        end_times = [slot.end_time for slot in self.appointment_slot.all()]
        return max(end_times) if end_times else None
