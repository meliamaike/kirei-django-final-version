from django.urls import path
from . import views

app_name = "orders"


urlpatterns = [
    path("order/order_detail/", views.order_detail, name="order_detail"),
    path("order/all/", views.all_order, name="all_order"),
    path("order/all/detail/<int:order_id>-<int:product_id>/", views.all_order_detail, name="all_order_detail"),

]