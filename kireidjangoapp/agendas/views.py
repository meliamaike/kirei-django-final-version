from django.shortcuts import render, get_object_or_404, redirect, reverse
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
                print("entro")
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


def agenda_list(request):
    agendas = Agenda.objects.all()
    return render(request, "agendas/all_agendas.html", {"agendas": agendas})


def agenda_detail(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    return render(request, "agendas/agenda_detail.html", {"agenda": agenda})


def edit_agenda(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == "POST":
        form = EditAgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            Agenda.objects.filter(pk=pk).update(
                start_time=form.cleaned_data["start_time"],
                end_time=form.cleaned_data["end_time"],
            )
            return redirect("agendas:all_agendas")
    else:
        form = EditAgendaForm(instance=agenda)
        context = {"form": form, "agenda": agenda}
        return render(request, "agendas/edit_agenda.html", context)

    context = {"form": form, "agenda": agenda}
    return render(request, "agendas/all_agendas.html", context)


def day_modification(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == "POST":
        form = AgendaDayModificationsForm(request.POST, instance=agenda)

        print("Form antes de is_valid: ", form)
        if form.is_valid():
            # agenda = agenda,
            date_f = (form.cleaned_data["date"],)
            available = (form.cleaned_data["available"],)
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]

            print("date: ", date_f)
            date_string = date_f.strftime("%m/%d/%Y")
            print("TRANSFOMRADO: ", date_string)
            form.save()
            am = AgendaModifications.objects.create(
                agenda=agenda,
                date=date_f,
                available=available,
                start_time=start_time,
                end_time=end_time,
            )
            print("Lo que se supone se debe haber creado: ", am)
            return redirect("agendas:all_agendas")
    else:
        print("Es el else y dsp el form: ")
        form = AgendaDayModificationsForm(instance=agenda)

    context = {"form": form, "agenda": agenda}
    return render(request, "agendas/day_modification.html", context)


def delete_agenda(request, pk):
    agenda = get_object_or_404(Agenda, pk=pk)
    if request.method == "POST":
        agenda.delete()
        return redirect("agendas/all_agendas.html")
    return render(request, "agendas/all_agendas.html", {"agenda": agenda})
