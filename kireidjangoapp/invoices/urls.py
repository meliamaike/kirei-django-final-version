from django.urls import path
from . import views

app_name = "invoices"

urlpatterns = [
    path(
        "factura/<int:order_id>-<int:product_id>/",
        views.generate_invoice,
        name="generate_invoice",
    ),
]
