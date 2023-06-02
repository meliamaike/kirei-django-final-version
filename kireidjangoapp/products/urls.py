from django.urls import path
from . import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

app_name = "products"
urlpatterns = [
    path("products/", views.product_catalog, name="product_catalog"),
    path(
        "products/<slug:product_name>-<int:product_id>/",
        views.product_detail,
        name="product_detail",
    ),
    path("staff/product/all", views.all_product, name="all_product"),
    path("staff/product/create", views.create_product, name="create_product"),
    path("staff/product/<int:pk>/edit/", views.edit_product, name="edit_product"),
    path("staff/product/<int:pk>/delete/", views.delete_product, name="delete_product"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
