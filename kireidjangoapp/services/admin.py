from django.contrib import admin
from services.models import Service, CategoryService


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_per_page = 15


@admin.register(CategoryService)
class CategoryServiceAdmin(admin.ModelAdmin):
    list_per_page = 15
