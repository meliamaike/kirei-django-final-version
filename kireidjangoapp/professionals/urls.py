from django.urls import path
from . import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

app_name = "professionals"
urlpatterns = [
    path("staff/professional/all", views.all_professional, name="all_professional"),
    path(
        "staff/professional/create",
        views.create_professional,
        name="create_professional",
    ),
    path(
        "staff/professional/<int:pk>/edit/",
        views.edit_professional,
        name="edit_professional",
    ),
    path(
        "staff/professional/<int:pk>/delete/",
        views.delete_professional,
        name="delete_professional",
    ),
]
