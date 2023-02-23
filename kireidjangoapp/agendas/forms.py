from django import forms
from agendas.models import Agenda

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ('professional','start_time', 'end_time')

