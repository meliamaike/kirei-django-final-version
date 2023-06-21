from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
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
    path("", include(("invoices.urls", "invoices"), namespace="invoices")),
    path("", include(("services.urls", "services"), namespace="services")),
    path(
        "", include(("professionals.urls", "professionals"), namespace="professionals")
    ),
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
]

urlpatterns += staticfiles_urlpatterns()