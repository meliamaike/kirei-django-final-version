from django import forms
from agendas.models import Agenda, AgendaModifications

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ('professional','start_time', 'end_time')

class AgendaEditForm(forms.ModelForm):

    class Meta:
        model = AgendaModifications
        fields = ['date','available','start_time', 'end_time']
