from django.urls import path
from . import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

app_name = "services"
urlpatterns = [
    path(
        "staff/category-service/all",
        views.all_category_service,
        name="all_category_service",
    ),
    path(
        "staff/category-service/create",
        views.create_category_service,
        name="create_category_service",
    ),
    path(
        "staff/category-service/<int:pk>/edit/",
        views.edit_category_service,
        name="edit_category_service",
    ),
    path(
        "staff/category-service/<int:pk>/delete/",
        views.delete_category_service,
        name="delete_category_service",
    ),
    path("staff/service/all", views.all_service, name="all_service"),
    path("staff/service/create", views.create_service, name="create_service"),
    path("staff/service/<int:pk>/edit/", views.edit_service, name="edit_service"),
    path("staff/service/<int:pk>/delete/", views.delete_service, name="delete_service"),
]
