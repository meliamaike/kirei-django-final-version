from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404

def product_catalog_view(request):
    categories = Product.objects.values('category').distinct()
    selected_category = request.GET.get('category')
    if selected_category:
        products = Product.objects.filter(category=selected_category, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)
    context = {'products': products, 'categories': categories, 'selected_category': selected_category}
    return render(request, 'products/products_catalog.html', context)

def product_detail_view(request, product_name, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product, 'id': product_id})


