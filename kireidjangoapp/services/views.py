from django.shortcuts import render, redirect, get_object_or_404
from services.models import CategoryService, Service
from services.forms import CategoryServiceForm, ServiceForm, CategoryServiceEditForm


# Category service
def all_category_service(request):
    categories = CategoryService.objects.all()
    return render(
        request, "services/category_service_list.html", {"categories": categories}
    )


def create_category_service(request):
    if request.method == "POST":
        form = CategoryServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("services:all_category_service")
    else:
        form = CategoryServiceForm()
    return render(request, "services/category_service_form.html", {"form": form})


def edit_category_service(request, pk):
    category = get_object_or_404(CategoryService, pk=pk)
    if request.method == "POST":
        form = CategoryServiceEditForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("services:all_category_service")
    else:
        form = CategoryServiceEditForm(instance=category)
    return render(
        request,
        "services/edit_category_service.html",
        {"form": form, "category": category},
    )


def delete_category_service(request, pk):
    category = get_object_or_404(CategoryService, pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect("services:all_category_service")

    context = {"category": category}
    return render(request, "category_service_list.html", context)


# Services
def all_service(request):
    services = Service.objects.all()
    return render(request, "services/service_list.html", {"services": services})


def create_service(request):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("services:all_service")
    else:
        form = ServiceForm()
    return render(request, "services/service_form.html", {"form": form})


def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect("services:all_service")
    else:
        form = ServiceForm(instance=service)
    return render(
        request, "services/edit_service.html", {"form": form, "service": service}
    )


def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        service.delete()
        return redirect("services:all_service")
    return render(request, "services/service_list.html", {"service": service})
