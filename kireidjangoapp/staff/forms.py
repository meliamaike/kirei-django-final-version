from allauth.account.forms import LoginForm
from crispy_forms.helper import FormHelper


class StaffLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields["login"].label = "Email"
        self.fields["password"].label = "Contraseña"
        self.fields["remember"].label = "Recuérdame"
        self.helper.form_method = "post"
        self.fields["password"].widget.attrs["placeholder"] = ""
        self.fields["login"].widget.attrs["placeholder"] = ""
        self.fields["login"].widget.attrs.update({"class": "form-control my-2"})
        self.fields["password"].widget.attrs.update({"class": "form-control my-2"})