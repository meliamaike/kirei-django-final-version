from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

from customers.forms import RegisterForm, CustomerLoginForm
from home.forms import ContactForm
from customers.views import signup_view, customer_login
from services.models import Service, CategoryService
from django.core.mail import send_mail
from customers.views import (
    signup_view_from_services,
    customer_login_from_services,
)
from django.contrib import messages


def contact_view(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():

            # Send the email
            subject = 'Solicitud de contacto desde el sitio web de Kirei'
            body = f'''
            Has recibido una solicitud de contacto desde el sitio web de Kirei:

            Nombre: {contact_form.cleaned_data["first_name"]} {contact_form.cleaned_data["last_name"]}
            Email: {contact_form.cleaned_data["email"]}
            Mensaje: 

            {contact_form.cleaned_data["message"]}
            '''

            message = body
            from_email = contact_form.cleaned_data["email"]
            recipient_list = ['hola@kirei.com']

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            print("Se envio el email?")
            messages.success(
            request,
            "Mensaje enviado. Te contestaremos a la brevedad."
        )
            return redirect('home:index')
        else:
            print("Form invalido de contacto.")
            messages.error(request, "Error. Mensaje no enviado. Intente más tarde.")
    else:
        contact_form = ContactForm()

    return render(request, "home/index.html", {"contact_form": contact_form})


def index(request):
    
    contact_form = ContactForm()
    register_form = RegisterForm()
    login_form = CustomerLoginForm()
    print("1er Request method:", request.method)

    if request.method == "POST":
        if "contact_form_submit" in request.POST:
            return contact_view(request)
        elif "register_form_submit" in request.POST:
            return signup_view(request)
        elif "login_form_submit" in request.POST:
            return customer_login(request)

    else:
        print("Request method:", request.method)

    context = {
        "contact_form": contact_form,
        "register_form": register_form,
        "login_form": login_form,
        "current_url": request.path,
    }

    return render(request, "home/index.html", context)


def services_index(request):
    services = Service.objects.all()
    categories = CategoryService.objects.all()
    register_form = RegisterForm()
    login_form = CustomerLoginForm()

    if request.method == "POST":
        if "register_form_submit" in request.POST:
            return signup_view_from_services(request)
        elif "login_form_submit" in request.POST:
            return customer_login_from_services(request)
        
    context = {
        "services": services,
        "categories": categories,
        "register_form": register_form,
        "login_form": login_form,
    }

    return render(request, "home/services.html", context)

def kirei_info(request):
    register_form = RegisterForm()
    login_form = CustomerLoginForm()

    if request.method == "POST":
        if "register_form_submit" in request.POST:
            return signup_view(request)
        elif "login_form_submit" in request.POST:
            return customer_login(request)
        
    context = {
        "register_form": register_form,
        "login_form": login_form,
    }
    return render(request, "home/kirei_info.html",context)

def faq(request):
    register_form = RegisterForm()
    login_form = CustomerLoginForm()

    if request.method == "POST":
        if "register_form_submit" in request.POST:
            return signup_view(request)
        elif "login_form_submit" in request.POST:
            return customer_login(request)
        
    context = {
        "register_form": register_form,
        "login_form": login_form,
    }

    return render(request, "home/faq.html",context)