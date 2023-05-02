from django.urls import path
from . import views
from agendas.views import create_agenda, edit_agenda

app_name = "staff"

urlpatterns = [
    path(
        "staff/statistic_dashboard",
        views.staff_statistic_dashboard,
        name="staff_statistic_dashboard",
    ),
    path(
        "staff/appointments_dashboard",
        views.staff_appointments_dashboard,
        name="staff_appointments_dashboard",
    ),
    path(
        "staff/customers_dashboard",
        views.staff_customers_dashboard,
        name="staff_customers_dashboard",
    ),
    path(
        "staff/main_dashboard", views.staff_main_dashboard, name="staff_main_dashboard"
    ),
    path("staff/login/", views.staff_login, name="staff_login"),
    path("staff/logout/", views.staff_logout, name="staff_logout"),
    path(
        "staff/appointments_dashboard/cancel/",
        views.staff_cancel_appointment,
        name="staff_cancel_appointment",
    ),
]
