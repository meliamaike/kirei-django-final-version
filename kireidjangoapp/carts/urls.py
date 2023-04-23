from django.urls import path
from . import views

app_name = "carts"


urlpatterns = [
    path("cart/add/<int:id>/", views.cart_add, name="cart_add"),
    path("cart/item_clear/<int:id>/<str:redirect_url>/", views.item_clear, name="item_clear"),
    path("cart/item_increment/<int:id>/<str:redirect_url>/", views.item_increment, name="item_increment"),
    path("cart/item_decrement/<int:id>/<str:redirect_url>/", views.item_decrement, name="item_decrement"),
    path("cart/cart_clear/", views.cart_clear, name="cart_clear"),
    path("cart/cart_detail/", views.cart_detail, name="cart_detail"),
    path(
        "cart/many_items_add/<int:id>/<int:quantity>/",
        views.many_items_add,
        name="many_items_add",
    ),
    path(
        "cart/catalog_item_increment/<int:id>/",
        views.catalog_item_increment,
        name="catalog_item_increment",
    ),
    path(
        "cart/replace_items_quantity/<int:id>/<int:quantity>/",
        views.replace_items_quantity,
        name="replace_items_quantity",
    ),
    path("cart/checkout/", views.cart_checkout, name="cart_checkout"),
    path("cart/success/", views.mercado_pago_success, name="mercado_pago_success"),
    path("cart/failure/", views.mercado_pago_failure, name="mercado_pago_failure"),
    path("cart/pending/", views.mercado_pago_pending, name="mercado_pago_pending"),
]
