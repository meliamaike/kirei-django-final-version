from django.contrib import admin
from professionals.models import Professional


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_per_page = 15
