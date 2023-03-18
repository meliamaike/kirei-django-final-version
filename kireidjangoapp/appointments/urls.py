from django.urls import path

from appointments import views

from django.contrib.auth import views as auth_views


app_name = "appointments"

urlpatterns = [
    # path("booking/all", views.all_appointments, name="all_appointments"),
    # path("booking/details", views.appointment_details, name="appointment_details"),
    # path("booking/cancel/<pk>", views.cancel_appointment, name="cancel_appointment"),
    path("booking/service/", views.choose_service, name="choose_service"),
    path(
        "booking/service/add-to-cart/<int:service_id>/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "booking/professional/",
        views.choose_professional,
        name="choose_professional",
    ),
    path("booking/calendar/", views.calendar, name="calendar"),
    path("booking/slot/", views.ChooseSlotView.as_view(), name="choose_slot"),
    path("booking/checkout/", views.checkout, name="checkout"),
]
