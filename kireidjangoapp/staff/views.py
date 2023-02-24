from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from staff.forms import StaffLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def staff_dashboard(request):
    return render(request, "staff/dashboard.html")


class StaffLoginView(LoginView):
    template_name = 'staff/login.html'
    authentication_form = StaffLoginForm
    success_url = reverse_lazy('staff_dashboard')


def logout_view(request):
    logout(request)
    messages.info(request, "Ha cerrado sesión correctamente.")
    return redirect("staff:staff_login")