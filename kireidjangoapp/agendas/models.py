import datetime
from django.db import models
from professionals.models import Professional

"""
Un profesional tiene una Agenda por dia, es decir, tiene MUCHAS AGENDAS.
"""


class Agenda(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    day = models.DateField()
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
    available = models.BooleanField(default=True)
