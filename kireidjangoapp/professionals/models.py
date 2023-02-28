from django.db import models
from services.models import Service


class Professional(models.Model):
    professional = models.CharField(max_length=255)
    services = models.ManyToManyField(Service)
    start_date = models.DateField()

    def __str__(self):
        return self.professional
