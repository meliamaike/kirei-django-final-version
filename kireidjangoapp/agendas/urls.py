from django.urls import path

from agendas import views

from django.contrib.auth import views as auth_views


app_name = "agendas"

urlpatterns = [
    path("agenda/all", views.all_agenda, name="all_agenda"),
    path("agenda/create", views.create_agenda, name="create_agenda"),
    path("agenda/<int:pk>/edit", views.edit_agenda, name="edit_agenda"),
    path(
        "agenda/<int:pk>/day_modification",
        views.day_modification,
        name="day_modification",
    ),
    path("agenda/<int:pk>/delete/", views.delete_agenda, name="delete_agenda"),
    path(
        "agenda/modifications/all",
        views.agenda_modifications_list,
        name="all_modifications_agenda",
    ),
    path(
        "agenda/modification/<int:pk>/delete/",
        views.agenda_modification_delete,
        name="agenda_modification_delete",
    ),
]
