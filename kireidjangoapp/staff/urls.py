from django.urls import path
from . import views
from agendas.views import create_agenda, edit_agenda

app_name = "staff"

urlpatterns = [
    path("staff/", views.staff_dashboard, name="staff_dashboard"),
    path("staff/login/", views.staff_login, name="staff_login"),
    path("staff/logout/", views.staff_logout, name="staff_logout"),
]
