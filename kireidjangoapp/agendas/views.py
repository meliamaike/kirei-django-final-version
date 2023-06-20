from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from agendas.models import Agenda
from professionals.models import Professional
from agendas.forms import AgendaForm, EditAgendaForm, AgendaDayModificationsForm
from django.http import JsonResponse
from django.template.loader import render_to_string
import json
from .models import AgendaModifications


def create_agenda(request):
    if request.method == "POST":
        form = AgendaForm(request.POST)
        if form.is_valid():
            professional = form.cleaned_data["professional"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]

            if Agenda.objects.filter(professional=professional).exists():
                modal_content = {
                    "title": "Ya existe una agenda con ese profesional!",
                    "text": "Si desea modificarla, por favor, editela.",
                }
                # Return a JsonResponse with the modal content
                return JsonResponse(
                    {"success": False, "modal_content": json.dumps(modal_content)}
                )
            else:
                Agenda.objects.create(
                    professional=professional, start_time=start_time, end_time=end_time
                )
                return JsonResponse({"success": True})
    else:
        form = AgendaForm()

    context = {"form": form}
    return render(request, "agendas/create_agenda.html", context)


def all_agenda(request):
    agendas = Agenda.objects.all()
    return render(request, "agendas/all_agenda.html", {"agendas": agendas})

from datetime import date
def agenda_modifications_list(request):

    today = date.today()
    modifications = AgendaModifications.objects.filter(date__gte=today)
    return render(request, "agendas/all_modifications.html", {"modifications": modifications})
   


def agenda_modification_delete(request, pk):
    modification = get_object_or_404(AgendaModifications, pk=pk)
    if request.method == "POST":
        modification.delete()
        return JsonResponse({"status": 200})
    return render(
        request, "agendas/all_modifications.html", {"modifications": modification}
    )


def edit_agenda(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == "POST":
        form = EditAgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            Agenda.objects.filter(pk=pk).update(
                start_time=form.cleaned_data["start_time"],
                end_time=form.cleaned_data["end_time"],
            )
            return redirect("agendas:all_agenda")
    else:
        form = EditAgendaForm(instance=agenda)
        context = {"form": form, "agenda": agenda}
        return render(request, "agendas/edit_agenda.html", context)

    context = {"form": form, "agenda": agenda}
    return render(request, "agendas/all_agenda.html", context)


def day_modification(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == "POST":
        form = AgendaDayModificationsForm(
            request.POST, instance=AgendaModifications(agenda=agenda)
        )
        if form.is_valid():
            # check if there is already a modification for the selected date
            date = form.cleaned_data["date"]
            existing_modification = AgendaModifications.objects.filter(
                agenda=agenda, date=date
            ).exists()
            if existing_modification:
                return JsonResponse({"success": False})
            else:
                form.save()
                return JsonResponse({"success": True})

    else:
        form = AgendaDayModificationsForm(instance=agenda)

    context = {"form": form, "agenda": agenda}
    return render(request, "agendas/day_modification.html", context)


def delete_agenda(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == "POST":
        agenda.delete()
        return redirect("agendas/all_agenda.html")
    return render(request, "agendas/all_agenda.html", {"agenda": agenda})
