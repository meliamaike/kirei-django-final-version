import datetime
from django.db import models
from professionals.models import Professional
from appointments.models import AppointmentSlot
from datetime import datetime, timedelta
from django.utils import timezone
from dateutil import rrule

"""
Un profesional tiene una Agenda por dia, es decir, tiene MUCHAS AGENDAS.
"""


class Agenda(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    start_time = models.CharField(
        max_length=5,
        choices=[
            ("8:00", "8:00 AM"),
            ("8:30", "8:30 AM"),
            ("9:00", "9:00 AM"),
            ("9:30", "9:30 AM"),
            ("10:00", "10:00 AM"),
            ("10:30", "10:30 AM"),
            ("11:00", "11:00 AM"),
            ("11:30", "11:30 AM"),
            ("12:00", "12:00 PM"),
            ("12:30", "12:30 PM"),
            ("13:00", "13:00 PM"),
            ("13:30", "13:30 PM"),
            ("14:00", "14:00 PM"),
            ("14:30", "14:30 PM"),
            ("15:00", "15:00 PM"),
            ("15:30", "15:30 PM"),
            ("16:00", "16:00 PM"),
            ("16:30", "16:30 PM"),
            ("17:00", "17:00 PM"),
            ("17:30", "17:30 PM"),
            ("18:00", "18:00 PM"),
            ("18:30", "18:30 PM"),
            ("19:00", "19:00 PM"),
            ("19:30", "19:30 PM"),
        ],
    )
    end_time = models.CharField(
        max_length=5,
        choices=[
            ("8:30", "8:30 AM"),
            ("9:00", "9:00 AM"),
            ("9:30", "9:30 AM"),
            ("10:00", "10:00 AM"),
            ("10:30", "10:30 AM"),
            ("11:00", "11:00 AM"),
            ("11:30", "11:30 AM"),
            ("12:00", "12:00 PM"),
            ("12:30", "12:30 PM"),
            ("13:00", "13:00 PM"),
            ("13:30", "13:30 PM"),
            ("14:00", "14:00 PM"),
            ("14:30", "14:30 PM"),
            ("15:00", "15:00 PM"),
            ("15:30", "15:30 PM"),
            ("16:00", "16:00 PM"),
            ("16:30", "16:30 PM"),
            ("17:00", "17:00 PM"),
            ("17:30", "17:30 PM"),
            ("18:00", "18:00 PM"),
            ("18:30", "18:30 PM"),
            ("19:00", "19:00 PM"),
            ("19:30", "19:30 PM"),
            ("20:00", "20:00 PM"),
        ],
    )

    def get_time_slots(self, date_slot, agenda):
        start_time, end_time = self.get_start_and_end_time(date_slot, agenda)

        if start_time is None or end_time is None:
            return []

        start_datetime = timezone.make_aware(datetime.combine(date_slot, start_time))
        end_datetime = timezone.make_aware(datetime.combine(date_slot, end_time))
        slot_duration = timedelta(minutes=30)
        appointment_slots = []

        # Loop through each time slot on this day
        while start_datetime < end_datetime:
            slot_end_datetime = start_datetime + slot_duration
            slot = AppointmentSlot(
                agenda=self,
                start_time=start_datetime.time(),
                end_time=slot_end_datetime.time(),
                booked=False,
            )
            slot.save()

            appointment_slots.append(slot)

            start_datetime += slot_duration

        return appointment_slots

    def get_start_and_end_time(self, date_slot, agenda):
        start_time = datetime.strptime(self.start_time, "%H:%M").time()
        end_time = datetime.strptime(self.end_time, "%H:%M").time()

        modifications = AgendaModifications.objects.filter(
            date=date_slot,
            agenda=agenda,
        )

        if modifications.filter(available=True).exists():
            modification = modifications.first()
            start_time = datetime.strptime(modification.start_time, "%H:%M").time()
            end_time = datetime.strptime(modification.end_time, "%H:%M").time()
        elif modifications.filter(available=False).exists():
            return None, None

        return start_time, end_time


class AgendaModifications(models.Model):
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.CharField(
        blank=True,
        null=True,
        max_length=5,
        choices=[
            ("8:00", "8:00 AM"),
            ("8:30", "8:30 AM"),
            ("9:00", "9:00 AM"),
            ("9:30", "9:30 AM"),
            ("10:00", "10:00 AM"),
            ("10:30", "10:30 AM"),
            ("11:00", "11:00 AM"),
            ("11:30", "11:30 AM"),
            ("12:00", "12:00 PM"),
            ("12:30", "12:30 PM"),
            ("13:00", "13:00 PM"),
            ("13:30", "13:30 PM"),
            ("14:00", "14:00 PM"),
            ("14:30", "14:30 PM"),
            ("15:00", "15:00 PM"),
            ("15:30", "15:30 PM"),
            ("16:00", "16:00 PM"),
            ("16:30", "16:30 PM"),
            ("17:00", "17:00 PM"),
            ("17:30", "17:30 PM"),
            ("18:00", "18:00 PM"),
            ("18:30", "18:30 PM"),
            ("19:00", "19:00 PM"),
            ("19:30", "19:30 PM"),
        ],
    )
    end_time = models.CharField(
        blank=True,
        null=True,
        max_length=5,
        choices=[
            ("8:30", "8:30 AM"),
            ("9:00", "9:00 AM"),
            ("9:30", "9:30 AM"),
            ("10:00", "10:00 AM"),
            ("10:30", "10:30 AM"),
            ("11:00", "11:00 AM"),
            ("11:30", "11:30 AM"),
            ("12:00", "12:00 PM"),
            ("12:30", "12:30 PM"),
            ("13:00", "13:00 PM"),
            ("13:30", "13:30 PM"),
            ("14:00", "14:00 PM"),
            ("14:30", "14:30 PM"),
            ("15:00", "15:00 PM"),
            ("15:30", "15:30 PM"),
            ("16:00", "16:00 PM"),
            ("16:30", "16:30 PM"),
            ("17:00", "17:00 PM"),
            ("17:30", "17:30 PM"),
            ("18:00", "18:00 PM"),
            ("18:30", "18:30 PM"),
            ("19:00", "19:00 PM"),
            ("19:30", "19:30 PM"),
            ("20:00", "20:00 PM"),
        ],
    )
    available = models.BooleanField(default=True)
