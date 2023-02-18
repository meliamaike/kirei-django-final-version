from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("products/", views.product_catalog_view, name="product_catalog"),
    path(
        "products/<slug:product_name>-<int:product_id>/",
        views.product_detail_view,
        name="product_detail",
    ),
]
