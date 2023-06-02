from django.shortcuts import render, redirect, get_object_or_404
from professionals.models import Professional
from professionals.forms import ProfessionalForm


def all_professional(request):
    professionals = Professional.objects.all()
    return render(
        request,
        "professionals/professional_list.html",
        {"professionals": professionals},
    )


def create_professional(request):
    if request.method == "POST":
        form = ProfessionalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("professionals:all_professional")
    else:
        form = ProfessionalForm()
    return render(request, "professionals/professional_form.html", {"form": form})


def edit_professional(request, pk):
    professional = get_object_or_404(Professional, pk=pk)
    if request.method == "POST":
        form = ProfessionalForm(request.POST, instance=professional)
        if form.is_valid():
            form.save()
            return redirect("professionals:all_professional")
    else:
        form = ProfessionalForm(instance=professional)
    return render(
        request,
        "professionals/edit_professional.html",
        {"form": form, "professional": professional},
    )


def delete_professional(request, pk):
    professional = get_object_or_404(Professional, pk=pk)
    if request.method == "POST":
        professional.delete()
        return redirect("professionals:all_professional")
    return render(
        request, "professionals/professional_list.html", {"professional": professional}
    )
