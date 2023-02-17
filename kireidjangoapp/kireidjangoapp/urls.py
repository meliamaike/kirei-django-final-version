from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", include("home.urls")),
    path("", include(("customers.urls", "customers"), namespace="customers")),
    path("", include(("carts.urls", "carts"), namespace="carts")),
    path("", include(("products.urls", "products"), namespace="products")),


    
]
