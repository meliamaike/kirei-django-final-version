from django.urls import path
from . import views

app_name = "my_payments"

urlpatterns = [
    path('payment/success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('payment/failed/<int:payment_id>/', views.payment_failed, name='payment_failed'),
]
