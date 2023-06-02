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


def choose_service(request):
    services = Service.objects.all()
    categories = CategoryService.objects.all()
    if request.method == "POST":
        service_id = request.POST["service"]
        request.session["service_id"] = service_id
        return redirect("appointments:choose_professional")
    context = {
        "services": services,
        "categories": categories,
    }
    return render(request, "appointments/choose_service.html", context)


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


@require_GET
def calendar(request):
    return render(request, "appointments/calendar.html")


class ChooseSlotView(View):
    def get(self, request):
        date_str = request.GET.get("date")
        date_slot = self.parsing_date(date_str)
        professional_id = request.session.get("professional_id")
        agenda = Agenda.objects.get(professional_id=professional_id)
        possible_appointments = self.get_possible_appointments(
            request, agenda, date_slot
        )

        return render(
            request,
            "appointments/choose_slot.html",
            {
                "possible_appointments": dict(possible_appointments),
                "date": date_slot,
            },
        )

    def parsing_date(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    def parsing_time(self, time_str):
        time_str_parts = time_str.split()

        if len(time_str_parts) == 5:
            month, day, year, time, am_pm = time_str_parts

            if len(time) == 1:
                time += ":00"

            if am_pm == "p.m.":
                am_pm = "PM"
            elif am_pm == "a.m.":
                am_pm = "AM"

            months = {
                "Ene.": "01",
                "Feb.": "02",
                "Mar.": "03",
                "Abr.": "04",
                "May.": "05",
                "Jun.": "06",
                "Jul.": "07",
                "Ago.": "08",
                "Sep.": "09",
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

        return date_obj

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
        possible_appointments = defaultdict(list)

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

            payment = AppointmentPayment.objects.create(
                appointment=appointment,
                payment_method=payment_method,
                status=PaymentStatus.WAITING,
                currency="ARS",
                total=service.price,
                description=service.service,
            )

            order = AppointmentOrder.objects.create(
                customer=customer,
                payment=payment,
            )

            request.session["appointment_payment_id"] = payment.id
            request.session["appointment_order_id"] = order.id

            return render(
                request,
                "appointments/appointment_detail.html",
                {
                    "professional": professional,
                    "service": service,
                    "start_date_time": start_date_time,
                    "appointment": appointment,
                    "order": order,
                },
            )

        else:
            return HttpResponseBadRequest("Error en el método de pago.")

    return render(
        request,
        "appointments/checkout.html",
        {
            "professional": professional,
            "service": service,
            "start_date_time": start_date_time,
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

    return render(
        request,
        "appointments/mercado_pago_success.html",
        {
            "payment_id": mercado_pago_payment_id,
            "merchant_order_id": merchant_order_id,
            "professional": professional,
            "service": service,
            "start_date_time": start_date_time,
            "appointment": appointment,
        },
    )


def mercado_pago_failure(request):
    return render(request, "appointments/mercado_pago_failure.html")


def appointment_detail(request):
    return render(request, "appointments/appointment_detail.html")


# For profile


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

    for appointment in appointments:
        for slot in appointment.appointment_slot.all():
            slot.booked = False
            slot.save()

        appointment.delete()

    return redirect(reverse("appointments:all_appointments"))
