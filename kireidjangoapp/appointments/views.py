from math import ceil
from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from appointments.models import Appointment, AppointmentSlot
from services.models import Service, CategoryService
from professionals.models import Professional
from customers.models import Customer
from cart.cart import Cart
from agendas.models import Agenda
from my_payments.models import AppointmentPayment
from django.db.models import Q
from collections import defaultdict
from django.contrib import messages
from django.views.decorators.http import require_GET
from datetime import datetime
from payments.models import PaymentStatus
from django.http import HttpResponseBadRequest
from itertools import groupby
import mercadopago
from orders.models import AppointmentOrder
from customers.forms import RegisterForm, CustomerLoginForm
from customers.views import (
    signup_view_from_appointment,
    customer_login_from_appointment,
)
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def choose_service(request):
    services = Service.objects.all()
    categories = CategoryService.objects.all()
    register_form = RegisterForm()
    login_form = CustomerLoginForm()

    show_login_modal = False
    if request.method == "POST":
        if "register_form_submit" in request.POST:
            return signup_view_from_appointment(request)
        elif "login_form_submit" in request.POST:
            return customer_login_from_appointment(request)
        else:
            if request.user.is_authenticated:
                service_id = request.POST["service"]
                request.session["service_id"] = service_id
                return redirect("appointments:choose_professional")
            else:
                show_login_modal = True

    context = {
        "services": services,
        "categories": categories,
        "register_form": register_form,
        "login_form": login_form,
        "show_login_modal": show_login_modal,
    }

    return render(request, "appointments/choose_service.html", context)


def choose_professional(request):
    service_id = request.session.get("service_id")
    if not service_id:
        messages.error(request, "Elegí un servicio primero!")  
        return redirect("appointments:choose_service")

    service = get_object_or_404(Service, pk=service_id)
    cart = Cart(request)
    #professionals = Professional.objects.filter(services=service)
    professionals = Professional.objects.filter(services=service, agenda__isnull=False).distinct()

    if request.method == "POST":
        professional_id = request.POST["professional"]
        # agenda = Agenda.objects.get(professional_id=professional_id)
        request.session["professional_id"] = professional_id
        # request.session ["agenda"]= agenda
        return redirect("appointments:calendar")

    context = {
        "service": service,
        "professionals": professionals,
    }
    return render(request, "appointments/choose_professional.html", context)


@require_GET
def calendar(request):
    return render(request, "appointments/calendar.html")


class ChooseSlotView(View):
    def get(self, request):
        date_str = request.GET.get("date")

        print("date_str: ", date_str)#2023-06-19
        print("Data type of date_str:", type(date_str))#<class 'str'>
        date_slot = self.parsing_date(date_str)

       
        print("Parsing date de date_str: ", date_slot)#2023-06-19

        print("Data type of date_slot:", type(date_slot)) #<class 'datetime.date'>

        professional_id = request.session.get("professional_id")

        if professional_id is None:
            return redirect("appointments:choose_professional")

        
        try:
            agenda = Agenda.objects.get(professional_id=professional_id)
            possible_appointments = self.get_possible_appointments(request, agenda, date_slot)

            return render(
                request,
                "appointments/choose_slot.html",
                {
                    "possible_appointments": dict(possible_appointments),
                    "date": date_slot,
                },
            )
        except Agenda.DoesNotExist:
   
            return redirect("appointments:choose_professional")


    def parsing_date(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    def parsing_time(self, time_str):
        date_obj = None

        time_str_parts = time_str.split()

        if len(time_str_parts) == 5 :
            month, day, year, time, am_pm = time_str_parts
        elif len(time_str_parts) == 4:
            month, day, year, time = time_str_parts

        if len(time) == 1 or len(time) == 2:
            time += ":00"
        elif time == 'mediodía':
            time = "12:00"
            am_pm = "PM"

        if am_pm == "p.m.":
            am_pm = "PM"
        elif am_pm == "a.m.":
            am_pm = "AM"

        months = {
            "Ene.": "01",
            "Feb.": "02",
            "Mar.": "03",
            "Abr.": "04",
            "Mayo": "05",
            "Jun.": "06",
            "Jul.": "07",
            "Ago.": "08",
            "Sept.": "09",
            "Oct.": "10",
            "Nov.": "11",
            "Dic.": "12",
        }

        print(month.rstrip("."))
        # Convert the month name to a number
        month_number = months[month]

        # Construct datetime object
        date_str = f"{day} {month_number} {year} {time} {am_pm}"

        date_obj = datetime.strptime(date_str, "%d, %m %Y, %I:%M %p")
    
        if date_obj is not None:
            return date_obj
        else:
            raise ValueError("Invalid time format")


    def post(self, request):
        professional_id = request.session.get("professional_id")
        agenda = Agenda.objects.get(professional_id=professional_id)

        start_time_str = request.POST.get("start_time")
        request.session["start_date_time"] = start_time_str

        end_time_str = request.POST.get("end_time")
        start_time_obj = self.parsing_time(start_time_str)
        end_time_obj = self.parsing_time(end_time_str)

        request.session["appointment_date"] = str(start_time_obj)

    
        # get the appointment slot object based on start and end times
        slot = AppointmentSlot.objects.filter(
            agenda=agenda.id,
            start_time=start_time_obj.time(),
            end_time=end_time_obj.time(),
            booked=False,
        ).first()

        request.session["slot_id"] = slot.id

        return redirect("appointments:checkout")

    def get_possible_appointments(self, request, agenda, date_slot):
        #List where the possible_appointments are going to be saved
        possible_appointments = defaultdict(list)

        #For the duration of the service
        service_id = request.session.get("service_id")
        service = get_object_or_404(Service, pk=service_id)
        service_duration = service.duration

        slots = agenda.get_time_slots(date_slot, agenda, service_duration)

        for slot in slots:
            start_time = slot.start_time
            end_time = slot.end_time

            start_datetime = datetime.combine(date_slot, start_time)
            end_datetime = datetime.combine(date_slot, end_time)

            if not self.has_conflicting_appointments(
                date_slot, agenda, start_datetime, end_datetime
            ):
                possible_appointments[date_slot].append(
                    {
                        "start_time": start_datetime,
                        "end_time": end_datetime,
                    }
                )
        return possible_appointments

    def has_conflicting_appointments(
        self, date_slot, agenda, start_datetime, end_datetime
    ):
        return Appointment.objects.filter(
            professional=agenda.professional,
            date=date_slot,
            appointment_slot__start_time__lt=end_datetime,
            appointment_slot__end_time__gt=start_datetime,
        ).exists()


def checkout(request):
    professional_id = request.session.get("professional_id")
    service_id = request.session.get("service_id")
    start_date_time = request.session.get("start_date_time")
    end_time = request.session.get("end_time")
    appointment_date = request.session.get("appointment_date")


    # parse the input string into a datetime object
    parsed_appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M:%S")


    # extract the date part of the datetime object
    parsed_appointment_date_solo = parsed_appointment_date.date()


    # Extract the time from the datetime object
    appointment_time = parsed_appointment_date.time()

    # Format the time as a string in the desired format
    formatted_time = appointment_time.strftime("%H:%M")
    formatted_date = parsed_appointment_date_solo.strftime("%d/%m/%Y")

   
    professional = Professional.objects.get(id=professional_id)
    service = Service.objects.get(id=service_id)

    slot_id = request.session.get("slot_id")

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")
        request.session["payment_method"] = payment_method

        if payment_method == "mercadopago":
            # PROD_ACCESS_TOKEN needed
            sdk = mercadopago.SDK("")

            # Create an item in the preference
            customer = Customer.objects.get(id=request.user.id)

            preference_data = {
                "items": [
                    {
                        "title": service.service,
                        "quantity": 1,
                        "unit_price": float(service.price),
                        "currency_id": "ARS",
                    }
                ],
                "back_urls": {
                    "success": "http://127.0.0.1:8000/booking/success/",
                    "failure": "http://127.0.0.1:8000/booking/failure",
                },
                "auto_return": "approved",
                "binary_mode": True,
            }

            preference_response = sdk.preference().create(preference_data)
            preference = preference_response["response"]

            return render(
                request, "appointments/mercado_pago.html", {"item_id": preference["id"]}
            )

        elif payment_method == "cash":
            try:
                customer = Customer.objects.get(id=request.user.id)

                # Calculate the number of slots required based on the appointment duration
                num_slots = ceil(service.duration / 30)

                current_slot_id = slot_id

                for i in range(num_slots):
                    # Create the appointment object as before
                    appointment = Appointment.objects.create(
                        professional_id=professional_id,
                        service_id=service_id,
                        date=parsed_appointment_date_solo,
                        customer=customer,
                    )

                    # Mark the selected appointment slot as booked
                    slot = AppointmentSlot.objects.get(id=current_slot_id)
                    appointment.appointment_slot.add(slot)
                    slot.booked = True
                    slot.save()

                    current_slot_id += 1

                # Create the payment object with status 'waiting'

                payment = AppointmentPayment.objects.create(
                    appointment=appointment,
                    payment_method=payment_method,
                    status=PaymentStatus.WAITING,
                    currency="ARS",
                    total=service.price,
                    description=service.service,
                    billing_first_name=customer.first_name,
                    billing_last_name=customer.last_name,
                    billing_email=customer.email,
                    billing_phone=customer.phone_number,
                )

                order = AppointmentOrder.objects.create(
                    customer=customer,
                    payment=payment,
                )

                request.session["appointment_payment_id"] = payment.id
                request.session["appointment_order_id"] = order.id

                # Prepare the context data to pass to the template
                context = {
                    "professional": professional,
                    "service": service,
                    "formatted_date":formatted_date,
                    "formatted_time":formatted_time,
                    "appointment": appointment,
                    "order": order,
                }

                # Render the HTML content of the email template
                html_message = render_to_string("appointments/appointment_detail_email.html", context)

                # Strip the HTML tags to generate the plain text version of the email
                plain_message = strip_tags(html_message)

                # Send the email
                send_mail(
                    subject="Reserva pendiente de pago",
                    message=plain_message,
                    from_email="hola@kirei.com", 
                    recipient_list=[customer.email],  
                    html_message=html_message,
                    fail_silently=False,
                )

                return render(request, "appointments/appointment_detail.html", context)

            except Customer.DoesNotExist:
                messages.error(request, "Error. No existe usuario.")

        else:
            return messages.error(request, "Error en el método de pago. Intente más tarde.")

    return render(
        request,
        "appointments/checkout.html",
        {
            "professional": professional,
            "service": service,
            "start_date_time": start_date_time,
            "formatted_time":formatted_time,
            "formatted_date":formatted_date
        },
    )


def mercado_pago_success(request):
    professional_id = request.session.get("professional_id")
    service_id = request.session.get("service_id")
    start_date_time = request.session.get("start_date_time")

    appointment_date = request.session.get("appointment_date")

    # parse the input string into a datetime object
    parsed_appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d %H:%M:%S")

    # extract the date part of the datetime object
    parsed_appointment_date_solo = parsed_appointment_date.date()

    # Extract the time from the datetime object
    appointment_time = parsed_appointment_date.time()

    # Format the time as a string in the desired format
    formatted_time = appointment_time.strftime("%H:%M")
    formatted_date = parsed_appointment_date_solo.strftime("%d/%m/%Y")

    professional = Professional.objects.get(id=professional_id)
    service = Service.objects.get(id=service_id)

    mercado_pago_payment_id = request.GET.get("payment_id")
    merchant_order_id = request.GET.get("merchant_order_id")
    slot_id = request.session.get("slot_id")
    payment_method = request.session.get("payment_method")

    # Calculate the number of slots required based on the appointment duration
    num_slots = ceil(service.duration / 30)

    current_slot_id = slot_id

    customer = Customer.objects.get(id=request.user.id)

    for i in range(num_slots):
        # Create the appointment object as before
        appointment = Appointment.objects.create(
            professional_id=professional_id,
            service_id=service_id,
            date=parsed_appointment_date_solo,
            customer=customer,
        )

        # Mark the selected appointment slot as booked
        slot = AppointmentSlot.objects.get(id=current_slot_id)
        appointment.appointment_slot.add(slot)
        slot.booked = True
        slot.save()

        current_slot_id += 1

    # Create the payment object with status 'waiting'

    mypayment = AppointmentPayment.objects.create(
        id_mercado_pago=mercado_pago_payment_id,
        appointment=appointment,
        payment_method=payment_method,
        status=PaymentStatus.CONFIRMED,
        currency="ARS",
        total=service.price,
        description=service.service,
        billing_first_name=customer.first_name,
        billing_last_name=customer.last_name,
        billing_email=customer.email,
        billing_phone=customer.phone_number,
    )

    #Added later check
    order = AppointmentOrder.objects.create(
        customer=customer,
        payment=mypayment,
        )

    context = {
        "payment_id": mercado_pago_payment_id,
        "merchant_order_id": merchant_order_id,
        "professional": professional,
        "service": service,
        "formatted_date":formatted_date,
        "formatted_time":formatted_time,
        "appointment": appointment,
    }

    # Render the HTML content of the email template
    html_message = render_to_string("appointments/mercado_pago_success_email.html", context)

    # Strip the HTML tags to generate the plain text version of the email
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject="Reserva de turno en Kirei",
        message=plain_message,
        from_email="hola@kirei.com", 
        recipient_list=[customer.email],  
        html_message=html_message,
        fail_silently=False,
    )


    return render(
        request,
        "appointments/mercado_pago_success.html",
        context
    )


def mercado_pago_failure(request):
    return render(request, "appointments/mercado_pago_failure.html")


def appointment_detail(request):
    return render(request, "appointments/appointment_detail.html")


# For the profile


def all_appointments(request):
    appointments = Appointment.objects.filter(customer=request.user).order_by(
        "date", "professional", "service"
    )

    grouped_appointments = []
    for key, group in groupby(
        appointments, lambda appt: (appt.date, appt.professional, appt.service)
    ):
        appointments_list = list(group)
        grouped_appointments.append(
            {
                "date": key[0],
                "professional": key[1],
                "service": key[2],
                "appointments": appointments_list,
            }
        )

    return render(
        request,
        "appointments/all_appointment.html",
        {"grouped_appointments": grouped_appointments},
    )


@require_GET
def cancel_appointment(request):
    appointment_ids = request.GET.getlist("ids")
    appointment_ids = [int(id) for id in request.GET.get("ids").split(",")]
    appointments = Appointment.objects.filter(id__in=appointment_ids)
    customer= appointments[0].customer
    # Prepare the appointment details to pass to the email template
    context = {
        'service': appointments[0].service,
        'date': appointments[0].date,
        'time': appointments[0].start_time,
        'professional': appointments[0].professional,
        'customer':customer
    }

    for appointment in appointments:
        for slot in appointment.appointment_slot.all():
            slot.booked = False
            slot.save()
        
        appointment.delete()


    # Render the HTML content of the email template
    html_message = render_to_string("appointments/appointment_cancel_email.html", context)

    # Strip the HTML tags to generate the plain text version of the email
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject="Se canceló la reserva",
        message=plain_message,
        from_email="hola@kirei.com", 
        recipient_list=[customer.email, 'hola@kirei.com'],  
        html_message=html_message,
        fail_silently=False,
    )

    messages.success(
        request,
        "Reserva cancelada correctamente. Ya se le ha notificado al centro de belleza.",
    )

    return redirect(reverse("appointments:all_appointments"))
