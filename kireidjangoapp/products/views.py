from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Max
from django.core.paginator import Paginator
from django.urls import resolve



def product_catalog_view(request):

    
    print("METODO: ", request.GET)

    categories = Product.objects.values("category").distinct()
    selected_category = request.GET.get("category")
    min_price = Product.objects.aggregate(Min('price'))['price__min']
    max_price = Product.objects.aggregate(Max('price'))['price__max']
    
    # Get the selected price range from the request's GET parameters
    selected_min_price = request.GET.get("min_price")
    selected_max_price = request.GET.get("max_price")
    print("Request:",selected_min_price)
    counts = {}
    for category in categories:
        if selected_category:
            count = Product.objects.filter(category=category['category'], is_available=True, category__exact=selected_category).count()
        else:
            count = Product.objects.filter(category=category['category'], is_available=True).count()
        counts[category['category']] = count
        


    if selected_category:
        products = Product.objects.filter(category=selected_category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)
    
    # Apply selected price range filter
    if selected_min_price and selected_max_price:
        products = products.filter(price__gte=selected_min_price, price__lte=selected_max_price)
    
    paginator = Paginator(products, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
        "min_price": min_price,
        "max_price": max_price,
        "page_obj": page_obj,
        "is_paginated": paginator.num_pages > 1,
        "counts": counts,
        "selected_min_price": selected_min_price,
        "selected_max_price": selected_max_price,
    }
    return render(request, "products/products_catalog.html", context)


def product_detail_view(request, product_name, product_id):
    product = get_object_or_404(Product, pk=product_id)
    print("URL de la IMG: ", product.image.url)
    return render(
        request, "products/product_detail.html", {"product": product, "id": product_id}
    )
