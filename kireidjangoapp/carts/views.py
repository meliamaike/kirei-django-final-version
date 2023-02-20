from django.shortcuts import render, redirect
from products.models import Product
from django.contrib.auth.decorators import login_required
from cart.cart import Cart


@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home:index")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("carts:cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("carts:cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("carts:cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("carts:cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    return render(request=request, template_name="carts/cart_detail.html")


@login_required(login_url="/login")
def many_items_add(request, id, quantity):
    print("cantidad: ", quantity)
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.adding_many(product=product, quantity=quantity)
    return redirect("carts:cart_detail")

@login_required(login_url="/login")
def catalog_item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("products:product_catalog")
