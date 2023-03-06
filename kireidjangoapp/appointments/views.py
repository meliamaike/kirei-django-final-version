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



def choose_service(request):
    services = Service.objects.all()
    if request.method == 'POST':
        service_id = request.POST['service']
        request.session['service'] = service_id
        return redirect('appointments:choose_professional', service_id=service_id)
    context = {
        'services': services
    }
    return render(request, 'appointments/choose_service.html', context)

def add_to_cart(request, service_id):
    service = Service.objects.get(id=service_id)
    cart = Cart(request)
    cart.add_service(service=service)
    return redirect('appointments:choose_professional', service_id=service_id)


def choose_professional(request, service_id):
    service = Service.objects.get(id=service_id)
    cart = Cart(request)

    if request.method == 'POST':
        professional_id = request.POST['professional']
        request.session['professional'] = professional_id
        return redirect('appointments:choose_slot', professional_id=professional_id)

    context = {
        'service': service,
        'cart': cart,
        'professionals': Professional.objects.filter(services=service.id),
    }
    return render(request, 'appointments/choose_professional.html', context)


def get_weeks():
    year = datetime.date.today().year
    week_num_initial = datetime.date.today().isocalendar()[1]
    weeks = []
    for week_num in range(week_num_initial, 53):
        # Calculate the start and end dates of the week
        week_start = datetime.date.fromisocalendar(year, week_num, 1)
        week_end = datetime.date.fromisocalendar(year, week_num, 7)
        
        # If the week crosses into the next year, skip it
        if week_end.year > year + 1:
            break

        # Create a list of the dates in the week
        week_dates = [week_start + datetime.timedelta(days=i) for i in range(5)]

        # Add the week and its dates to the list of weeks
        weeks.append({'week': week_num, 'dates': week_dates})

    return weeks


def choose_slot(request,professional_id):
    weeks = get_weeks()
    week_start_date = weeks[0]['dates'][0]
    week_end_date = week_start_date + timedelta(days=4)

    print("WEEEK START DATEE: ", week_start_date)
    print("WEEK END DAY : ", week_end_date)
    agenda = Agenda.objects.get(professional_id=professional_id)
    print("Agenda ", agenda.professional)
    
    modifications = AgendaModifications.objects.filter(
        agenda=agenda,
        date__range=[week_start_date, week_end_date],
    )
    print("Modification: ", modifications)

    appointments = []
    slots= agenda.get_time_slots()
    
    for dt in rrule.rrule(rrule.DAILY, dtstart=week_start_date, until=week_end_date):
        
        for slot in slots:
            start_time = slot.start_time
            end_time = slot.end_time
            print("SLOTS dates: ", start_time, end_time)
            start_datetime = datetime.datetime.combine(dt, start_time)
            end_datetime = datetime.datetime.combine(dt, end_time)


            if modifications.filter(date=dt, start_time=start_time, end_time=end_time).exists():
                continue
            if not Appointment.objects.filter(
                professional=agenda.professional,
                start_time__lte=end_datetime,
                end_time__gte=start_datetime,
            ).exists():
                appointments.append({
                    'start_time': start_datetime,
                    'end_time': end_datetime,
                })

    #return appointments
    return render(request, 'appointments/choose_slot.html',{"weeks": weeks})




def all_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, "appointments/all_appointment.html", {"appointments": appointments})

# def appointment_details():

def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        appointment.delete()
        return redirect("appointments/all_appointments.html")
    return render(request, "appointments/all_appointments.html", {"appointment": appointment})



