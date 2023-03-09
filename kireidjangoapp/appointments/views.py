from time import strptime
from django.shortcuts import render
from appointments.models import Appointment
from django.shortcuts import render, get_object_or_404, redirect

from services.models import Service
from professionals.models import Professional
from cart.cart import Cart
from agendas.models import Agenda, AgendaModifications
from dateutil import rrule
import datetime
from datetime import timedelta
from django.db.models import Q
from datetime import date
from collections import defaultdict


def choose_service(request):
    services = Service.objects.all()
    if request.method == "POST":
        service_id = request.POST["service"]
        request.session["service"] = service_id
        return redirect("appointments:choose_professional", service_id=service_id)
    context = {"services": services}
    return render(request, "appointments/choose_service.html", context)


def add_to_cart(request, service_id):
    service = Service.objects.get(id=service_id)
    cart = Cart(request)
    cart.add_service(service=service)
    return redirect("appointments:choose_professional", service_id=service_id)


def choose_professional(request, service_id):
    service = Service.objects.get(id=service_id)
    cart = Cart(request)

    if request.method == "POST":
        professional_id = request.POST["professional"]
        request.session["professional"] = professional_id
        return redirect("appointments:choose_week", professional_id=professional_id)

    context = {
        "service": service,
        "cart": cart,
        "professionals": Professional.objects.filter(services=service.id),
    }
    return render(request, "appointments/choose_professional.html", context)


def get_weeks():
    year = datetime.date.today().year
    week_num_initial = datetime.date.today().isocalendar()[1]
    weeks = []
    
    #Calculate the weeks from today to 6 months
    week_num_end = week_num_initial + 25

    for week_num in range(week_num_initial, week_num_end):
        # Calculate the start and end dates of the week
        week_start = datetime.date.fromisocalendar(year, week_num, 1)
        week_end = datetime.date.fromisocalendar(year, week_num, 7)


        # If the week crosses into the next year, skip it
        if week_end.year > year + 1:
            break

        # Create a list of the dates in the week in datetime.date() format
        week_dates = [week_start + datetime.timedelta(days=i) for i in range(7)]
        
        #Parse into '%d-%m-%Y' format
        parsed_week_dates  = []
        for date in week_dates:
            parsed_week_dates.append(date.strftime('%d-%m-%Y'))

        # Add the week and its dates to the list of weeks
        weeks.append({"week": week_num, "dates": parsed_week_dates})

    return weeks

def choose_week(request, professional_id):
    weeks = get_weeks()
    context = {
        # "service": service,
        # "cart": cart,
        # "professionals": Professional.objects.filter(services=service.id),
        "weeks": weeks, 
        "professional_id": professional_id
    }
    return render(request, "appointments/choose_week.html",context) 


def choose_slot(request, professional_id,week_start_date):
    from datetime import datetime
    
    start_date = datetime.strptime(week_start_date, '%d-%m-%Y')
    end_date = start_date + timedelta(days=5)

    agenda = Agenda.objects.get(professional_id=professional_id)

    modifications = AgendaModifications.objects.filter(
        agenda=agenda,
        date__range=[start_date, end_date],
    )

    #possible_appointments = []
    possible_appointments = defaultdict(list)
    
    #Brings the time slots
    slots = agenda.get_time_slots()

    #dt is the current day
    for dt in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
        for slot in slots:
            start_time = slot.start_time
            end_time = slot.end_time
                        
            #Combine the current day with the start_time of the time slot
            import datetime
            start_datetime = datetime.datetime.combine(dt, start_time)
            end_datetime = datetime.datetime.combine(dt, end_time)

            if modifications.filter(
                date=dt, 
                start_time=start_time, 
                end_time=end_time
            ).exists():
                continue
            if not Appointment.objects.filter(
                professional=agenda.professional,
                appointment_slot__start_time__lte =end_datetime,
                appointment_slot__end_time__gte =start_datetime,
            ).exists():
                possible_appointments[dt.date()].append(
                    {
                        "start_time": start_datetime,
                        "end_time": end_datetime,
                    }
                )
            print("possible appointments: ", dict(possible_appointments))
    
    return render(request, "appointments/choose_slot.html", {"possible_appointments":dict(possible_appointments),"week_start_date":week_start_date})


def all_appointments(request):
    appointments = Appointment.objects.all()
    return render(
        request, "appointments/all_appointment.html", {"appointments": appointments}
    )


# def appointment_details():


def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.delete()
        return redirect("appointments/all_appointments.html")
    return render(
        request, "appointments/all_appointments.html", {"appointment": appointment}
    )
