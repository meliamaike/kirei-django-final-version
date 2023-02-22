from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Max, Sum
from django.core.paginator import Paginator
from django.urls import resolve



def product_catalog_view(request):

    print("Request: ", request.method)
    all_products = Product.objects.filter(is_available=True)
    categories = Product.objects.values("category").distinct()
    selected_category = request.GET.get("category")
    min_price = Product.objects.aggregate(Min('price'))['price__min']
    max_price = Product.objects.aggregate(Max('price'))['price__max']
    
    # Get the selected price range from the request's GET parameters
    selected_min_price = request.GET.get("min_price")
    selected_max_price = request.GET.get("max_price")

    # Get selected sorting method from request's GET parameters
    selected_sorting = request.GET.get("orderby")

    print("Selected request: ", selected_sorting)

    # Apply selected sorting method to products
    if selected_sorting == "popularity":
        #products = Product.objects.filter(is_available=True).annotate(num_sold=Sum('sale__num_sold')).order_by('-num_sold')
        products = all_products# Fater a sale is done, you can update the sale table
    elif selected_sorting == "date":
        products = all_products.order_by('-id')
    elif selected_sorting == "price":
        products = all_products.order_by('price')
        print("de mas barato a mas caro: ", products)
    elif selected_sorting == "price-desc":
        products = all_products.order_by('-price')
        print("de mas caro a mas barato: ", products)
    else:
        products = all_products

    # Get counts of products for each category
    counts = {}
    for category in categories:
        if selected_category:
            count = Product.objects.filter(category=category['category'], is_available=True, category__exact=selected_category).count()
        else:
            count = Product.objects.filter(category=category['category'], is_available=True).count()
        counts[category['category']] = count
        
    # Filter products by selected category
    if selected_category:
        products = products.filter(category=selected_category, is_available=True)
    else:
        products = products.filter(is_available=True)
    
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
        "selected_sorting": selected_sorting,
    }

    return render(request, "products/products_catalog.html", context)


def product_detail_view(request, product_name, product_id):
    product = get_object_or_404(Product, pk=product_id)
    print("URL de la IMG: ", product.image.url)
    return render(
        request, "products/product_detail.html", {"product": product, "id": product_id}
    )
