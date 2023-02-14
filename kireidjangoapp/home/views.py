from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

from customers.forms import RegisterForm


def index(request):
    contact_form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "email": form.cleaned_data["email_address"],
                "message": form.cleaned_data["message"],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, "admin@example.com", ["admin@example.com"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect("home:index")
    context = {
        
        'contact_form': contact_form
    }
    return render(request, 'home/index.html', context)   
