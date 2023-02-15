from django import forms
from customers.models import Customer
from django.contrib.auth import authenticate, get_user_model


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from django import forms
from django.db.models.query_utils import Q

from django import forms

from allauth.account.forms import SignupForm, LoginForm



# Form de registro


class RegisterForm(SignupForm):

    first_name = forms.CharField(label="Nombre", max_length=30, required=True)
    last_name = forms.CharField(label="Apellido", max_length=30, required=True)
    document_number = forms.CharField(
        label="Nro. Documento", max_length=30, required=True
    )
    area_code = forms.CharField(label="Código Área", max_length=5, required=True)
    phone_number = forms.CharField(label="Nro. Teléfono", max_length=20, required=True)
    
    def signup(self, request):
        user = super(RegisterForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.document_number = self.cleaned_data['document_number']
        user.area_code = self.cleaned_data['area_code']
        user.phone_number = self.cleaned_data['phone_number']
        user.save()
        return user

    class Meta:
        model = get_user_model()
    
    


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["email"].label = "Email"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmá tu contraseña"
        self.fields["email"].widget.attrs["placeholder"] = ""
        self.fields["password1"].widget.attrs["placeholder"] = ""
        self.fields["password2"].widget.attrs["placeholder"] = ""
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['document_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['area_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})




    

# Form de Login


class CustomerLoginForm(LoginForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["login"].label = "Email"
        self.fields["password"].label = "Contraseña"
        self.fields["remember"].label = "Recuérdame"
        self.helper.form_method = "post"
        self.fields["password"].widget.attrs["placeholder"] = ""
        self.fields["login"].widget.attrs["placeholder"] = ""
        self.fields['login'].widget.attrs.update({'class': 'form-control my-2'})
        self.fields['password'].widget.attrs.update({'class': 'form-control my-2'})