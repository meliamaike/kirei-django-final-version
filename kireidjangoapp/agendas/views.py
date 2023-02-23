from django.shortcuts import render
from agendas.models import Agenda
from agendas.forms import AgendaForm

def create_agenda(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            agenda = form.save(commit=False)
            agenda.professional = request.user.professional
            agenda.save()
    else:
        form = AgendaForm()

    context = {'form': form}
    return render(request, 'agendas/create_agenda.html', context)
