from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from staff.forms import StaffLoginForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate


def staff_dashboard(request):
    return render(request, "staff/dashboard.html")


def staff_login(request):
    form = StaffLoginForm(request=request)
    
    if request.method == "POST":
        form = StaffLoginForm(data=request.POST, request=request)
        if form.is_valid():
            # Authenticate the user
            email = form.cleaned_data.get("login")
            print("Email: ", email)
            password = form.cleaned_data.get("password")
            print("Pass: ", password)
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_staff:
                # Log the user in
                login(request, user)
                # Redirect to a success page
                
                return redirect("staff:staff_dashboard")
            else:
                # Return an 'invalid login' error message
                form.add_error(None, "Login inválido")
        else:
            print(form.errors)
    else:
        form = StaffLoginForm()
    
    return render(request, 'staff/staff_login.html', {"form": form})


def staff_logout(request):
    logout(request)
    # messages.info(request, "Ha cerrado sesión correctamente.")
    return redirect("staff:staff_login")

 
