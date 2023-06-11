from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, label="Nombre")
    last_name = forms.CharField(max_length=50, label="Apellido")
    email = forms.EmailField(max_length=150, label="E-mail")
    message = forms.CharField(widget=forms.Textarea, max_length=2000, label="Mensaje")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["first_name"].label = "Nombre"
        self.fields["last_name"].label = "Apellido"
        self.fields["email"].label = "Email"
        self.fields["message"].label = "Mensaje"
        self.helper.layout = Layout(
            "first_name",
            "last_name",
            "email",
            "message",
            Submit("submit", "Enviar", css_class="btn btn-primary mt-3"),
        )

    class Meta:
        template = "crispy_forms/field.html"
