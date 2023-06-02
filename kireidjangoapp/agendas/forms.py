from django import forms
from agendas.models import Agenda, AgendaModifications
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


class AgendaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["professional"].label = "Profesional"
        self.fields["start_time"].label = "Horario de inicio"
        self.fields["end_time"].label = "Horario de finalización"

        self.fields["professional"].choices = [
            ("", "Elegí el nombre del profesional...")
        ] + list(self.fields["professional"].choices)[1:]
        self.fields["start_time"].choices = [
            ("", "Elegí el horario de inicio...")
        ] + list(self.fields["start_time"].choices)[1:]
        self.fields["end_time"].choices = [
            ("", "Elegí el horario de finalización...")
        ] + list(self.fields["end_time"].choices)[1:]

    class Meta:
        model = Agenda
        fields = ("professional", "start_time", "end_time")


class EditAgendaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["professional"].widget.attrs["readonly"] = True
        self.fields["professional"].label = "Profesional"
        self.fields["start_time"].label = "Horario de inicio"
        self.fields["end_time"].label = "Horario de finalización"

    class Meta:
        model = Agenda
        fields = ["professional", "start_time", "end_time"]


class AgendaDayModificationsForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control datepicker"}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["available"].initial = False
        self.fields["date"].label = "Fecha"
        self.fields["available"].label = "Disponible ese día "
        self.fields["start_time"].label = "Horario de inicio"
        self.fields["end_time"].label = "Horario de finalización"

    class Meta:
        model = AgendaModifications
        fields = ["date", "available", "start_time", "end_time"]
