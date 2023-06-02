# from django import forms
# from professionals.models import Professional


# class ProfessionalForm(forms.ModelForm):
#     class Meta:
#         model = Professional
#         fields = ['professional', 'services', 'start_date']


from django import forms
from professionals.models import Professional
from services.models import Service
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.utils.translation import gettext_lazy as _


class ProfessionalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["professional"].label = "Profesional"
        self.fields["services"].label = "Servicio"
        self.fields["start_date"].label = "Inicio de actividad laboral"

    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.SelectMultiple(attrs={"size": "10"}),
        required=True,
        help_text="Mantené apretado 'Control' o 'Command' en Mac para seleccionar varios elementos.",
    )

    class Meta:
        model = Professional
        fields = ["professional", "services", "start_date"]
        widgets = {
            "professional": forms.TextInput(
                attrs={"class": "vTextField", "maxlength": "255"}
            ),
            "start_date": DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "showTodayButton": True,
                }
            ),
        }
