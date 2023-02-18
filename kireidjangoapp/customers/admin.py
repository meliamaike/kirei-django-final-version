from django.contrib import admin
from customers.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_per_page = 15
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    list_filter = (
        "email",
        "first_name",
        "last_name",
    )
