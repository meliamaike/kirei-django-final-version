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

    
    def get_time_slots(self):
        start_time = datetime.strptime(self.start_time, '%H:%M').time()
        end_time = datetime.strptime(self.end_time, '%H:%M').time()
        start_datetime = timezone.make_aware(datetime.combine(datetime.today(), start_time))
        end_datetime = timezone.make_aware(datetime.combine(datetime.today(), end_time))

        print("start_datetime", start_datetime)
        print("end_datetime", end_datetime)
        slot_duration = timedelta(minutes=30)
        appointment_slots = []

        for dt in rrule.rrule(rrule.DAILY, dtstart=start_datetime, until=end_datetime):
            while start_datetime < dt:
                start_datetime += slot_duration
            while start_datetime + slot_duration <= end_datetime:
                slot_end_datetime = start_datetime + slot_duration
                slot = AppointmentSlot(
                    agenda=self,
                    start_time=start_datetime.time(),
                    end_time=slot_end_datetime.time(),
                    booked=False
                )
                slot.save()

                print("SLOR CREADO SE SUPONEE: ", slot)
                appointment_slots.append(slot)
                start_datetime = slot_end_datetime

        return appointment_slots

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
