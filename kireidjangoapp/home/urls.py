from django.urls import path, include

from . import views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("services/", views.services_index, name="services"),
    path("nosotros/", views.kirei_info, name="kirei_info"),
    path("faq/", views.faq, name="faq"),
]
