from django.urls import path

from appointments import views

from django.contrib.auth import views as auth_views


app_name = "appointments"

urlpatterns = [
    path("booking/all/", views.all_appointments, name="all_appointments"),
    path("booking/cancel/", views.cancel_appointment, name="cancel_appointment"),
    path("booking/service/", views.choose_service, name="choose_service"),
    path(
        "booking/professional/",
        views.choose_professional,
        name="choose_professional",
    ),
    path("booking/calendar/", views.calendar, name="calendar"),
    path("booking/slot/", views.ChooseSlotView.as_view(), name="choose_slot"),
    path("booking/checkout/", views.checkout, name="checkout"),
    path("booking/detail/", views.appointment_detail, name="appointment_detail"),
    path("booking/success/", views.mercado_pago_success, name="mercado_pago_success"),
    path("booking/failure/", views.mercado_pago_failure, name="mercado_pago_failure"),
]
