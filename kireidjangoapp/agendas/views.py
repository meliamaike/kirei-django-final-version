from django.shortcuts import render,get_object_or_404, redirect
from agendas.models import Agenda
from professionals.models import Professional
from agendas.forms import AgendaForm, AgendaEditForm


def create_agenda(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            professional = form.cleaned_data['professional']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            Agenda.objects.create(professional=professional, start_time=start_time, end_time=end_time)
            return redirect('agenda_list')
    else:
        form = AgendaForm()
        context = {'form': form}
    return render(request, 'agendas/create_agenda.html', context)

def all_agendas(request):
    agendas = Agenda.objects.all()
    return render(request, 'all_agendas.html', {'agendas': agendas})

def agenda_detail(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    return render(request, 'agendas/agenda_detail.html',{'agenda': agenda})


def edit_agenda(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == 'POST':
        form = AgendaEditForm(request.POST, instance=agenda)
        if form.is_valid():
            form.save()
            return redirect('agenda_list')
    else:
        form = AgendaEditForm(instance=agenda)
    
    context = {'form': form, 'agenda': agenda}
    return render(request, 'agendas/edit_agenda.html', context)

def delete_agenda(request,pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == 'POST':
        agenda.delete()
        return redirect('agendas/all_agendas.html')
    return render(request, 'delete_agenda.html', {'agenda': agenda})


def delete_agenda(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == 'POST':
        agenda.delete()
        return redirect('agenda_list')
    return render(request, 'delete_agenda.html', {'agenda': agenda})




