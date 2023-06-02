from django.urls import path
from . import views
from agendas.views import create_agenda, edit_agenda
from django.contrib.auth import views as auth_views


app_name = "staff"

urlpatterns = [
    path(
        "staff/orders_dashboard",
        views.staff_orders_dashboard,
        name="staff_orders_dashboard",
    ),
    path(
        "staff/orders-details/<int:order_id>-<int:product_id>/",
        views.orders_details,
        name="orders_details",
    ),
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
        "staff/create_appointment",
        views.staff_create_appointment,
        name="staff_create_appointment",
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
    path("staff/not-available/", views.not_available, name="not_available"),
    path(
        "staff/password_reset/", views.staff_password_reset, name="staff_password_reset"
    ),
    path(
        "staff/password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="staff/password/password_reset_done.html"
        ),
        name="staff_password_reset_done",
    ),
    path(
        "staff/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="staff/password/password_reset_confirm.html"
        ),
        name="staff_password_reset_confirm",
    ),
    path(
        "staff/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="staff/password/password_reset_complete.html"
        ),
        name="staff_password_reset_complete",
    ),
]
