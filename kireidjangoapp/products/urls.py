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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)