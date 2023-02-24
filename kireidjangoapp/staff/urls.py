from django.urls import path
from . import views
from agendas.views import create_agenda, edit_agenda

app_name = 'staff'

urlpatterns = [
    path('', views.staff_dashboard, name='staff_dashboard'),
    path('login/', views.StaffLoginView.as_view(), name='staff_login'),
    #path('statistics/', views.statistics, name='statistics'),
    
]
