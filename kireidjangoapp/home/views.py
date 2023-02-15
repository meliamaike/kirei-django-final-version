from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

from customers.forms import RegisterForm, CustomerLoginForm
from customers.views import signup_view,customer_login

def contact_view(request):
    contact_form = ContactForm(request.POST)
    if contact_form.is_valid():
        subject = "Website Inquiry"
        body = {
            "first_name": contact_form.cleaned_data["first_name"],
            "last_name": contact_form.cleaned_data["last_name"],
            "email": contact_form.cleaned_data["email_address"],
            "message": contact_form.cleaned_data["message"],
        }
        message = "\n".join(body.values())
        try:
            send_mail(subject, message, "admin@example.com", ["admin@example.com"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return redirect("home:index")

def index(request):
    contact_form = ContactForm()
    register_form = RegisterForm()
    login_form = CustomerLoginForm()
    print("1er Request method:",request.method)

    if request.method == "POST":
        print("ENTRO AL POST")
        if 'contact_form_submit' in request.POST:
            return contact_view(request)
        elif 'register_form_submit' in request.POST:
            return signup_view(request)
        elif 'login_form_submit' in request.POST:
            return customer_login(request)
    
    else: 
        print("Request method:",request.method)
    

    context = {
        'contact_form': contact_form,
        'register_form': register_form,
        'login_form': login_form,
        'current_url': request.path
    }
    return render(request, 'home/index.html', context)   
