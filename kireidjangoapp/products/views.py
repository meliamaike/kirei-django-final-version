from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Min, Max, Sum
from django.core.paginator import Paginator
from decimal import Decimal, InvalidOperation
from products.forms import ProductForm

from customers.forms import RegisterForm, CustomerLoginForm
from customers.views import signup_view_from_product, customer_login_from_product,customer_login_from_product_detail, signup_view_from_product_detail
from django.contrib import messages


def product_catalog(request):
    all_products = Product.objects.filter(is_available=True)
    products_total = all_products.count()

    categories = Product.objects.values("category").distinct()
    selected_category = request.GET.get("category")

    min_price = Product.objects.aggregate(Min("price"))["price__min"]
    max_price = Product.objects.aggregate(Max("price"))["price__max"]

    # Get the selected price range from the request's GET parameters
    selected_min_price = request.GET.get("min_price")
    selected_max_price = request.GET.get("max_price")

    # Get selected sorting method from request's GET parameters
    selected_sorting = request.GET.get("orderby")

    # Apply selected sorting method to products
    orderby = request.GET.get("orderby")
    if orderby == "price":
        products = all_products.order_by("price")
    elif orderby == "price-desc":
        products = all_products.order_by("-price")
    else:
        products = all_products

    # Get counts of products for each category
    counts = {}
    for category in categories:
        if selected_category:
            count = Product.objects.filter(
                category=category["category"],
                is_available=True,
                category__exact=selected_category,
            ).count()
        else:
            count = Product.objects.filter(
                category=category["category"], is_available=True
            ).count()
        counts[category["category"]] = count

    # Get counts of products for each category
    category_counts = {}
    for category in categories:
        count = Product.objects.filter(
            category=category["category"], is_available=True
        ).count()
        category_counts[category["category"]] = count

    # Filter products by selected category
    if selected_category:
        products = products.filter(category=selected_category, is_available=True)
    else:
        products = products.filter(is_available=True)

    # Apply selected price range filter
    if selected_min_price and selected_max_price:
        products = products.filter(
            price__gte=selected_min_price, price__lte=selected_max_price
        )

    paginator = Paginator(products, 15)
    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    # Login & register when not authenticated
    register_form = RegisterForm()
    login_form = CustomerLoginForm()

    context = {
        "products": products,
        "products_total": products_total,
        "categories": categories,
        "selected_category": selected_category,
        "min_price": min_price,
        "max_price": max_price,
        "page_obj": page_obj,
        "is_paginated": paginator.num_pages > 1,
        "counts": counts,
        "category_counts": category_counts,
        "selected_min_price": selected_min_price,
        "selected_max_price": selected_max_price,
        "selected_sorting": selected_sorting,
        "register_form": register_form,
        "login_form": login_form,
    }

    if request.method == "POST":
        if "register_form_submit" in request.POST:
            return signup_view_from_product(request, context)
        elif "login_form_submit" in request.POST:
            return customer_login_from_product(request, context)

    return render(request, "products/products_catalog.html", context)


def product_detail(request, product_name, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # Login & register when not authenticated
    register_form = RegisterForm()
    login_form = CustomerLoginForm()

    context={
        "product": product, 
         "id": product_id,
         "register_form": register_form,
         "login_form": login_form
    }

    if request.method == "POST":
        if "register_form_submit" in request.POST:
            return signup_view_from_product_detail(request, context)
        elif "login_form_submit" in request.POST:
            return customer_login_from_product_detail(request, context)

    return render(
        request, "products/product_detail.html", context
        
    )


# Staff panel product
def all_product(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})


def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("products:all_product")
    else:
        form = ProductForm()
    return render(request, "products/product_form.html", {"form": form})


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("products:all_product")
    else:
        form = ProductForm(instance=product)
    return render(
        request, "products/edit_product.html", {"form": form, "product": product}
    )


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("products:all_product")
    return render(request, "products/product_list.html", {"product": product})
