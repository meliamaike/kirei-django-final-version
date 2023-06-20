from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from customers.models import Customer
from django.db.models.query_utils import Q
from customers.forms import RegisterForm, CustomerLoginForm
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from customers.forms import ProfileCustomerForm
from home.forms import ContactForm
from django.template import loader
from services.models import Service, CategoryService
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.conf import settings
import os

#Signup
def signup_view(request):
    value = False

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("El formulario es valido y entro")
            customer = form.signup(request)
            login(
                request, customer, backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect("home:index")
        else:
            value = True
            print("Form invalido: ", form)
    else:
        form = RegisterForm()

    contact_form = ContactForm()
    login_form = CustomerLoginForm()

    context = {
        "register_form": form,
        "value_signup": value,
        "contact_form": contact_form,
        "login_form": login_form,
    }
    return render(request, "home/index.html", context)


def signup_view_from_appointment(request):
    value = False
    services = Service.objects.all()
    categories = CategoryService.objects.all()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("El formulario es valido y entro")
            customer = form.signup(request)
            login(
                request, customer, backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect("appointments:choose_service")
        else:
            value = True
    else:
        form = RegisterForm()

    contact_form = ContactForm()
    login_form = CustomerLoginForm()

    context = {
        "register_form": form,
        "value_signup": value,
        "contact_form": contact_form,
        "login_form": login_form,
        "services": services,
        "categories": categories,
    }
    return render(request, "appointments/choose_service.html", context)

def signup_view_from_services(request):
    value = False
    services = Service.objects.all()
    categories = CategoryService.objects.all()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("El formulario es valido y entro")
            customer = form.signup(request)
            login(
                request, customer, backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect("home:services")
        else:
            value = True
    else:
        form = RegisterForm()

    contact_form = ContactForm()
    login_form = CustomerLoginForm()

    context = {
        "register_form": form,
        "value_signup": value,
        "contact_form": contact_form,
        "login_form": login_form,
        "services": services,
        "categories": categories,
    }
    return render(request, "home/services.html", context)

def signup_view_from_product(request, context):
    value = False

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("El formulario es valido y entro")
            customer = form.signup(request)
            login(
                request, customer, backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect("products:product_catalog")
        else:
            value = True
    else:
        form = RegisterForm()

    context["register_form"] = form
    context["value_signup"] = value

    return render(request, "products/products_catalog.html", context)


def signup_view_from_product_detail(request,context):
    value = False
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("El formulario es valido y entro")
            customer = form.signup(request)
            login(
                request, customer, backend="django.contrib.auth.backends.ModelBackend"
            )
            return redirect("products:product_catalog")
        else:
            value = True
    else:
        form = RegisterForm()

    context["register_form"] = form
    context["value_signup"] = value

    return render(request, "products/product_detail.html", context)


#Login
def customer_login(request):
    form = CustomerLoginForm(request=request)
    value = False

    if request.method == "POST":
        form = CustomerLoginForm(data=request.POST, request=request)
        if form.is_valid():
            # Authenticate the user
            email = form.cleaned_data.get("login")
            print("Email: ", email)
            password = form.cleaned_data.get("password")
            print("Pass: ", password)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect to index
                return redirect("home:index")
            else:
                value = True
                print("mostrar con Swal mensaje de error.")
        else:
            value = True
            print("Formulario invalido.")

    else:
        form = CustomerLoginForm(data=request.POST, request=request)

    contact_form = ContactForm()
    register_form = RegisterForm()
    context = {
        "contact_form": contact_form,
        "register_form": register_form,
        "login_form": form,
        "value": value,
    }
    return render(request, "home/index.html", context)

def customer_login_from_appointment(request):
    form = CustomerLoginForm(request=request)
    services = Service.objects.all()
    categories = CategoryService.objects.all()
    value = False

    if request.method == "POST":
        form = CustomerLoginForm(data=request.POST, request=request)
        if form.is_valid():
            # Authenticate the user
            email = form.cleaned_data.get("login")
            print("Email: ", email)
            password = form.cleaned_data.get("password")
            print("Pass: ", password)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect to a success page
                return redirect("appointments:choose_service")
            else:
                # Return an 'invalid login' error message
                value = True
        else:
            value = True

    else:
        print("Mostrar mensaje con swal.")

    register_form = RegisterForm()
    context = {
        "register_form": register_form,
        "login_form": form,
        "value": value,
        "services": services,
        "categories": categories,
    }

    return render(request, "appointments/choose_service.html", context)

def customer_login_from_services(request):
    form = CustomerLoginForm(request=request)
    services = Service.objects.all()
    categories = CategoryService.objects.all()
    value = False

    if request.method == "POST":
        form = CustomerLoginForm(data=request.POST, request=request)
        if form.is_valid():
            # Authenticate the user
            email = form.cleaned_data.get("login")
            print("Email: ", email)
            password = form.cleaned_data.get("password")
            print("Pass: ", password)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect to a success page
                return redirect("home:services")
            else:
                # Return an 'invalid login' error message
                value = True
        else:
            value = True

    else:
        print("Mostrar mensaje con swal.")

    register_form = RegisterForm()
    context = {
        "register_form": register_form,
        "login_form": form,
        "value": value,
        "services": services,
        "categories": categories,
    }

    return render(request, "home/services.html", context)

def customer_login_from_product(request, context):
    form = CustomerLoginForm(request=request)

    value = False

    if request.method == "POST":
        form = CustomerLoginForm(data=request.POST, request=request)
        if form.is_valid():
            # Authenticate the user
            email = form.cleaned_data.get("login")
            print("Email: ", email)
            password = form.cleaned_data.get("password")
            print("Pass: ", password)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect to a success page
                return redirect("appointments:product_catalog")
            else:
                # Return an 'invalid login' error message
                value = True
        else:
            value = True

    else:
        print("Mostrar mensaje con swal.")

    context["login_form"] = form
    context["value"] = value

    return render(request, "products/products_catalog.html", context)

from django.urls import reverse
from django.utils.text import slugify
def customer_login_from_product_detail(request, context):
    form = CustomerLoginForm(request=request)

    value = False

    if request.method == "POST":
        form = CustomerLoginForm(data=request.POST, request=request)
        if form.is_valid():
            # Authenticate the user
            email = form.cleaned_data.get("login")
            print("Email: ", email)
            password = form.cleaned_data.get("password")
            print("Pass: ", password)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect to a success page
                product = context["product"]
                product_name_slug = slugify(product.name)
                url = reverse("products:product_detail", kwargs={"product_name": product_name_slug, "product_id": product.id})
                return redirect(url)
            else:
                # Return an 'invalid login' error message
                value = True
        else:
            value = True

    else:
        print("Mostrar mensaje con swal.")

    context["login_form"] = form
    context["value"] = value

    return render(request, "products/product_detail.html", context)


# Logout
def logout_view(request):
    logout(request)
    return redirect("home:index")


# Forgot password

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib import messages



def password_reset(request):
    register_form = RegisterForm()
    login_form = CustomerLoginForm()
    show_login_modal = False
    if request.method == "POST":
        if "register_form_submit" in request.POST:
            return signup_view(request)
        elif "login_form_submit" in request.POST:
            return customer_login(request)
        else:
            password_reset_form = PasswordResetForm(request.POST)
            
            if password_reset_form.is_valid():
                email = password_reset_form.cleaned_data["email"]
                associated_users = Customer.objects.filter(email=email)
                if associated_users.exists():
                    user = associated_users.first()
                    subject = "Cambio de contraseña"
                    email_template_name = "customers/password/password_reset_email.txt"
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    protocol = 'http' if request.is_secure() else 'https'
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "Kirei estética",
                        "uid": uid,
                        "user": user,
                        "token": token,
                        "protocol": protocol,
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "hola@kirei.com", 
                            [user.email],
                            fail_silently=False,
                        )
                        messages.success(
                            request,
                            "Te enviamos un e-mail con las instrucciones para poder cambiar la contraseña."
                        )
                    
                    except BadHeaderError:
                        messages.error(request, "Error. Intente más tarde por favor.")
                        return redirect("customers:password_reset")
                else:
                    messages.error(request, "Error. No existe el usuario ingresado.")
                    return redirect("customers:password_reset")
            else:
                messages.error(request, "Error. Formulario inválido.")
                show_login_modal = True
                return redirect("customers:password_reset")
            
                
                
    password_reset_form = PasswordResetForm()

    context = {
        "form":password_reset_form,
        "register_form": register_form,
        "login_form": login_form,
        "show_login_modal": show_login_modal,
    }
    
    return render(request,"customers/password/password_reset.html",context)

@login_required
def profile(request):
    if request.method == "POST":
        if request.POST.get("form_type") == "personal_info":
            profile_form = ProfileCustomerForm(request.POST, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return JsonResponse({"success": True})
            else:
                error_dict = profile_form.errors.as_json()
                return JsonResponse({"success": False, "error": error_dict})

        elif request.POST.get("form_type") == "change_password":
            change_pass_form = PasswordChangeForm(request.user, request.POST)
            if change_pass_form.is_valid():
                user = change_pass_form.save()
                update_session_auth_hash(request, user)
                return JsonResponse({"success": True})
            else:
                error_dict = change_pass_form.errors.as_json()
                return JsonResponse({"success": False, "error": error_dict})
        elif request.POST.get("form_type") == "edit_image":
            file_to_upload = request.FILES.get('fileToUpload')
            request.user.profile_picture = file_to_upload
            request.user.save()

            # # Delete the old profile picture if needed
            # if request.user.profile_picture and os.path.isfile(os.path.join(settings.MEDIA_ROOT, str(request.user.profile_picture))):
            #     os.remove(os.path.join(settings.MEDIA_ROOT, str(request.user.profile_picture)))

            return redirect('customers:profile')


    profile_form = ProfileCustomerForm(instance=request.user)
    change_pass_form = PasswordChangeForm(request.user)
    return render(
        request,
        "customers/profile.html",
        context={"profile_form": profile_form, "change_pass_form": change_pass_form},
    )




    
 
