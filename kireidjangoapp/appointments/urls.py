from django.urls import path

from appointments import views

from django.contrib.auth import views as auth_views


app_name = "appointments"

urlpatterns = [
    # path("booking/new", views.new_appointment, name= "new_appointment"),
    # path("booking/all", views.all_appointments, name="all_appointments"),
    # path("booking/details", views.appointment_details, name="appointment_details"),
    # path("booking/cancel/<pk>", views.cancel_appointment, name="cancel_appointment"),
    path("booking/service/", views.choose_service, name="choose_service"),
    path(
        "booking/service/<int:service_id>/add_to_cart/",
        views.add_to_cart,
        name="add_to_cart",
    ),
    path(
        "booking/professional/<int:service_id>/",
        views.choose_professional,
        name="choose_professional",
    ),
    path('booking/week/<int:professional_id>/', views.choose_week, name='choose_week'),
    path('booking/slot/<int:professional_id>/<str:week_start_date>/', views.choose_slot, name='choose_slot'),
    # path('booking/professional/<int:professional_id>/add_to_cart/', views.add_professional_to_cart, name='add_professional_to_cart'),
    # path('booking/appointment_slot/', views.choose_appointment_slot, name='choose_appointment_slot'),
    # path('booking/appointment_slot/<int:appointment_slot_id>/checkout/', views.checkout, name='checkout'),
]
