from time import strptime
from django.shortcuts import render
from appointments.models import Appointment
from django.shortcuts import render, get_object_or_404, redirect

from services.models import Service, CategoryService
from professionals.models import Professional
from cart.cart import Cart
from agendas.models import Agenda, AgendaModifications
from dateutil import rrule
import datetime
from datetime import timedelta
from django.db.models import Q
from datetime import date
from collections import defaultdict
from django.contrib import messages
from django.views.decorators.http import require_GET



def choose_service(request):
    services = Service.objects.all()
    categories = CategoryService.objects.all()
    if request.method == "POST":
        service_id = request.POST["service"]
        request.session["service_id"] = service_id
        add_to_cart(request, service_id)
        return redirect("appointments:choose_professional")
    context = {"services": services,
               "categories": categories,
                }
    return render(request, "appointments/choose_service.html", context)

def add_to_cart(request, service_id):

    service = Service.objects.get(id=service_id)
    cart = Cart(request)
    cart.add_service(service=service)
    return redirect("appointments:choose_professional")


def choose_professional(request):
    service_id = request.session.get("service_id")
    if not service_id:
        messages.error(request, "Elegí un servicio primero!")
        return redirect("appointments:choose_service")
    
    service = get_object_or_404(Service, pk=service_id)
    cart = Cart(request)

    if request.method == "POST":
        professional_id = request.POST["professional"]
        request.session["professional_id"] = professional_id
        return redirect("appointments:calendar")

    context = {
        "service": service,
        "professionals": Professional.objects.filter(services=service),
    }
    return render(request, "appointments/choose_professional.html", context)

# /booking/slot/?date=2023-03-16
@require_GET
def calendar(request):
    return render(request, 'appointments/calendar.html')

def choose_slot(request):
    if request.method == 'GET':
        date_str = request.GET.get('date')
        print("Dia que trae dentro de choose slot funciton: ",date_str)
        from datetime import datetime

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        start_datetime = datetime.combine(date, datetime.min.time())
        end_datetime = datetime.combine(date, datetime.max.time())

        print("Start time and end time: ", start_datetime, end_datetime)        

        professional_id = request.session.get("professional_id")

        agenda = Agenda.objects.get(professional_id=professional_id)

        modifications = AgendaModifications.objects.filter(
            agenda=agenda,
            date = date,
        )

        print("Modificaciones: ", modifications)

        possible_appointments = defaultdict(list)

        # Brings the time slots
        slots = agenda.get_time_slots()

        for slot in slots:
            start_time = slot.start_time
            end_time = slot.end_time

            # Combine the current day with the start_time of the time slot
            start_datetime = datetime.combine(date, start_time)
            end_datetime = datetime.combine(date, end_time)

            if modifications.filter(
                available=False
            ).exists():
                continue
            elif modifications.filter(
                start_time=start_time, 
                end_time=end_time,
                available = True
            ).exists():
                continue

            if not Appointment.objects.filter(
                professional=agenda.professional,
                appointment_slot__start_time__lte=end_datetime,
                appointment_slot__end_time__gte=start_datetime,
            ).exists():
                possible_appointments[date].append(
                    {
                        "start_time": start_datetime,
                        "end_time": end_datetime,
                    }
                )

    if request.method == "POST":
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        request.session["start_time"] = start_time
        request.session["end_time"] = end_time
        return redirect("appointments:checkout")

    return render(
        request,
        "appointments/choose_slot.html",
        {
            "possible_appointments": dict(possible_appointments),
            "date": date,
        },
    )







def get_weeks():
    year = datetime.date.today().year
    week_num_initial = datetime.date.today().isocalendar()[1]
    weeks = []

    # Calculate the weeks from today to 6 months
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

        # Parse into '%d-%m-%Y' format
        parsed_week_dates = []
        for date in week_dates:
            parsed_week_dates.append(date.strftime("%d-%m-%Y"))

        # Add the week and its dates to the list of weeks
        weeks.append({"week": week_num, "dates": parsed_week_dates})

    return weeks




# def choose_week(request):
#     import calendar
#     import datetime
#     professional_id = request.session.get("professional_id")
#     if not professional_id:
#         messages.error(request, "Elegí primero un profeesional.")
#         return redirect("appointments:choose_professional")

#     # Get today's date
#     today = datetime.date.today()

#     # Calculate the start and end months for the calendar
#     start_month = today.month
#     end_month = start_month + 6
#     if end_month > 12:
#         end_month -= 12

#     # Calculate the start and end years for the calendar
#     start_year = today.year
#     end_year = start_year if end_month > start_month else start_year + 1

#     # Generate a calendar for each month in the range
#     weeks = []
#     for year in range(start_year, end_year + 1):
#         for month in range(start_month if year == start_year else 1, end_month + 1):
#             cal = calendar.monthcalendar(year, month)
#             for week in cal:
#                 # Filter out weeks with no days in the current month
#                 if week[0] == 0:
#                     continue

#                 # Create a list of the dates in the week in datetime.date() format
#                 week_dates = [datetime.date(year, month, day) for day in week if day != 0]

#                 # Filter out dates before today
#                 week_dates = [date for date in week_dates if date >= today]

#                 # Parse into '%d-%m-%Y' format
#                 parsed_week_dates = [date.strftime("%d-%m-%Y") for date in week_dates]

#                 # Add the week and its dates to the list of weeks
#                 weeks.append({"week": week[0], "dates": parsed_week_dates})

#     context = {
#         "weeks": weeks,
#     }

#     return render(request, "appointments/choose_week.html", context)

# def choose_week(request):
#     professional_id = request.session.get("professional_id")
#     if not professional_id:
#         messages.error(request, "Elegí primero un profeesional.")
#         return redirect("appointments:choose_professional")
    
    
#     weeks = get_weeks()
#     context = {
#         "weeks": weeks,
        
#     }
    
#     return render(request, "appointments/choose_week.html", context)



def choose_slot2(request):
    if request.method == "GET":
        from datetime import datetime

        week_start_day = request.GET.get('week_start_day')
        

        start_date = datetime.strptime(week_start_day, "%d-%m-%Y")
        end_date = start_date + timedelta(days=5)

        professional_id = request.session.get("professional_id")

        agenda = Agenda.objects.get(professional_id=professional_id)

        modifications = AgendaModifications.objects.filter(
            agenda=agenda,
            date__range=[start_date, end_date],
        )

        possible_appointments = defaultdict(list)

        # Brings the time slots
        slots = agenda.get_time_slots()

        # dt is the current day
        for dt in rrule.rrule(rrule.DAILY, dtstart=start_date, until=end_date):
            if modifications.filter(date=dt, available=False).exists():
                continue
            for slot in slots:
                start_time = slot.start_time
                end_time = slot.end_time

                # Combine the current day with the start_time of the time slot
                import datetime

                start_datetime = datetime.datetime.combine(dt, start_time)
                end_datetime = datetime.datetime.combine(dt, end_time)
                

                if modifications.filter(
                    date=dt, start_time=start_time, end_time=end_time
                ).exists():
                    continue
                if not Appointment.objects.filter(
                    professional=agenda.professional,
                    appointment_slot__start_time__lte=end_datetime,
                    appointment_slot__end_time__gte=start_datetime,
                ).exists():
                    possible_appointments[dt.date()].append(
                        {
                            "start_time": start_datetime,
                            "end_time": end_datetime,
                        }
                    )
        
    if request.method == "POST": 
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        print("Tipo de dato de start time",start_time)
        request.session["start_time"] = start_time
        request.session["end_time"] = end_time
        return redirect("appointments:checkout")
    
    return render(
        request,
        "appointments/choose_slot.html",
        {
            "possible_appointments": dict(possible_appointments),
            "week_start_date": week_start_day,
        },
    )


def checkout(request):
    professional_id=request.session.get("professional_id")
    service_id=request.session.get("service_id")
    start_time = request.session.get("start_time")
    end_time = request.session.get("end_time")
    professional = Professional.objects.get(id=professional_id)
    service = Service.objects.get(id=service_id)

    # if not appointment_details:
    #     messages.error(request, "Tenes que elegir una fecha!")
    #     return redirect("appointments:choose_week")

    # if request.method == "POST":
    #     form = PaymentForm(request.POST)
    #     if form.is_valid():
    #         # Create the appointment object
    #         appointment = Appointment.objects.create(
    #             professional_id=request.session.get("professional_id"),
    #             service_id=request.session.get("service_id"),
    #             start_time=appointment_details["start_time"],
    #             end_time=appointment_details["end_time"],
    #             user=request.user,
    #         )

    #         # Create the payment object
    #         payment = Payment.objects.create(
    #             appointment=appointment,
    #             amount=appointment.service.price,
    #             payment_method=form.cleaned_data["payment_method"],
    #             card_number=form.cleaned_data["card_number"],
    #             cardholder_name=form.cleaned_data["cardholder_name"],
    #             expiration_date=form.cleaned_data["expiration_date"],
    #         )

    #         # Clear the cart
    #         cart = Cart(request)
    #         cart.clear()

    #         messages.success(request, "Su cita ha sido agendada!")
    #         return redirect("appointments:appointment_detail", appointment_id=appointment.id)
    # else:
    #     form = PaymentForm()

    return render(
        request,
        "appointments/checkout.html",
        {
            #"form": form,
            "professional":professional,
            "service":service,
            "start_time":start_time,
            "end_time":end_time,
  
        },
    )








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
