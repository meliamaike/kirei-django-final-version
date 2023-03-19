import datetime
from django.db import models
from django.forms import ValidationError
from services.models import Service
from professionals.models import Professional
from shoppingcarts.models import ShoppingCart

# from agendas.models import Agenda
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
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    appointment_slot = models.OneToOneField(
        AppointmentSlot, on_delete=models.CASCADE, related_name="appointment"
    )

    @property
    def start_time(self):
        return self.appointment_slot.start_time

    @property
    def end_time(self):
        return self.appointment_slot.end_time
