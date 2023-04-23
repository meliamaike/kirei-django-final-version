from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("payments/", include("payments.urls")),
    path("", include("home.urls")),
    path("", include(("customers.urls", "customers"), namespace="customers")),
    path("", include(("carts.urls", "carts"), namespace="carts")),
    path("", include(("products.urls", "products"), namespace="products")),
    path("", include(("agendas.urls", "agendas"), namespace="agendas")),
    path("", include(("staff.urls", "staff"), namespace="staff")),
    path("", include(("appointments.urls", "appointments"), namespace="appointments")),
    path("", include(("orders.urls", "orders"), namespace="orders")),
]
