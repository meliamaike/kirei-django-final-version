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


from customers.forms import RegisterForm,CustomerLoginForm
from django.contrib.auth import authenticate



from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            customer = form.signup(request)
            login(request, customer,backend="django.contrib.auth.backends.ModelBackend")
            return redirect("home:index")
    else:
        form = RegisterForm()
    return render(request, 'home/index.html', {"form": form})

def customer_login(request):
    form = CustomerLoginForm(request=request)
    if request.method == 'POST':
        form = CustomerLoginForm(data=request.POST, request=request)
        print("FORMULARIO: ", form)
        if form.is_valid():
            # Authenticate the user
            email = form.cleaned_data.get('login')
            print("Email: ", email)
            password = form.cleaned_data.get('password')
            print("Pass: ", password)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # Log the user in
                login(request, user)
                # Redirect to a success page
                return redirect('home:index')
            else:
                # Return an 'invalid login' error message
                form.add_error(None, 'Invalid login')
        else:
            print(form.errors)
    else:
        form = CustomerLoginForm()
    return render(request, 'home/index.html', {'form': form})
    #return render(request, 'home/index.html', {'form': form})



# Cerrar sesion
def logout_view(request):
    logout(request)
    messages.info(request, "Ha cerrado sesión correctamente.")
    return redirect("home:index")


# Olvido de contraseña
def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = Customer.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Cambio de contraseña"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "Kirei estética",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
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
                    except BadHeaderError:
                        return HttpResponse("Se encontró una cabecera invalida..")
                    # return redirect("/password_reset/done/")
                    messages.success(
                        request,
                        "Te enviamos un e-mail con las instrucciones para poder cambiar la contraseña.",
                    )
                    return redirect("home:index")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="customers/password/password_reset.html",
        context={"password_reset_form": password_reset_form},
    )
