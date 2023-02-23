from django.urls import path

from agendas import views

from django.contrib.auth import views as auth_views


app_name = "agendas"

urlpatterns = [
    path("agenda/", views.create_agenda, name="create_agenda"),
    
]