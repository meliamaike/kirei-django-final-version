from django.shortcuts import render
from django.views import View
from appointments.models import Appointment, AppointmentSlot
from django.shortcuts import render, get_object_or_404, redirect
from services.models import Service, CategoryService
from professionals.models import Professional
from cart.cart import Cart
from agendas.models import Agenda
from my_payments.models import MyPayment
from django.db.models import Q
from collections import defaultdict
from django.contrib import messages
from django.views.decorators.http import require_GET
from datetime import datetime


def choose_service(request):
    services = Service.objects.all()
    categories = CategoryService.objects.all()
    if request.method == "POST":
        service_id = request.POST["service"]
        request.session["service_id"] = service_id
        # add_to_cart(request, service_id)
        return redirect("appointments:choose_professional")
    context = {
        "services": services,
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


@require_GET
def calendar(request):
    return render(request, "appointments/calendar.html")


class ChooseSlotView(View):
    
    def get(self, request):
        date_str = request.GET.get("date")
        date_slot = self.parsing_date(date_str)
        professional_id = request.session.get("professional_id")
        agenda = Agenda.objects.get(professional_id=professional_id)
        possible_appointments = self.get_possible_appointments(agenda, date_slot)
        
        return render(
            request,
            "appointments/choose_slot.html",
            {
                "possible_appointments": dict(possible_appointments),
                "date": date_slot,
            },
        )

    

    def parsing_time(self,time_str):
        time_str_parts = time_str.split()
        
        if len(time_str_parts) == 8:
            
            day, _, month, _, year, _, _, time = time_str_parts
            hour, minute = time.split(':')
        
            months = {
                'enero': '01',
                'febrero': '02',
                'marzo': '03',
                'abril': '04',
                'mayo': '05',
                'junio': '06',
                'julio': '07',
                'agosto': '08',
                'septiembre': '09',
                'octubre': '10',
                'noviembre': '11',
                'diciembre': '12'
            }

            # Convert the month name to a number
            month_number = months[month.lower()]

            # Construct datetime object
            date_str = f'{day} {month_number} {year} {time}'
            date_obj = datetime.strptime(date_str, '%d %m %Y %H:%M')

        return date_obj

    def post(self, request):

        professional_id = request.session.get("professional_id")
        agenda = Agenda.objects.get(professional_id=professional_id)

        start_time_str = request.POST.get("start_time")
        request.session['start_date_time'] = start_time_str
        end_time_str = request.POST.get("end_time")

        start_time_obj = self.parsing_time(start_time_str)
        end_time_obj = self.parsing_time(end_time_str)

        print("TIPO",type(start_time_obj))

        request.session['appointment_date'] = str(start_time_obj)


        # get the appointment slot object based on start and end times
        slot = AppointmentSlot.objects.filter(
            agenda=agenda.id,
            start_time=start_time_obj.time(),
            end_time=end_time_obj.time(),
            booked=False
        ).first()


        request.session["slot_id"] = slot.id

        return redirect("appointments:checkout")

    def parsing_date(self, date_str):
        return datetime.strptime(date_str, "%Y-%m-%d").date()

    def get_possible_appointments(self, agenda, date_slot):
        
        possible_appointments = defaultdict(list)
        slots = agenda.get_time_slots(date_slot, agenda)
        for slot in slots:
            start_time = slot.start_time
            end_time = slot.end_time

            start_datetime = datetime.combine(date_slot, start_time)
            end_datetime = datetime.combine(date_slot, end_time)

            if not self.has_conflicting_appointments(
                agenda, start_datetime, end_datetime
            ):
                possible_appointments[date_slot].append(
                    {
                        "start_time": start_datetime,
                        "end_time": end_datetime,
                    }
                )
        return possible_appointments

    def has_conflicting_appointments(self, agenda, start_datetime, end_datetime):
        return Appointment.objects.filter(
            professional=agenda.professional,
            appointment_slot__start_time__lte=end_datetime,
            appointment_slot__end_time__gte=start_datetime,
        ).exists()


# def checkout(request):
#     professional_id = request.session.get("professional_id")
#     service_id = request.session.get("service_id")
#     start_time = request.session.get("start_time")
#     end_time = request.session.get("end_time")
#     professional = Professional.objects.get(id=professional_id)
#     service = Service.objects.get(id=service_id)

#     if request.method == "POST":
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             # Create the payment object
#             payment = MyPayment.objects.create(
#                 variant=form.cleaned_data['payment_method'],
#                 description=f"Payment for appointment with {professional.name}",
#                 currency='USD',
#                 total=service.price,
#                 billing_first_name=form.cleaned_data['first_name'],
#                 billing_last_name=form.cleaned_data['last_name'],
#                 billing_address_1=form.cleaned_data['address_1'],
#                 billing_city=form.cleaned_data['city'],
#                 billing_postcode=form.cleaned_data['zipcode'],
#                 billing_country_code=form.cleaned_data['country_code'],
#                 billing_country_area=form.cleaned_data['country_area'],
#                 billing_email=form.cleaned_data['email'],
#                 billing_phone=form.cleaned_data['phone'],
#                 order=appointment
#             )

#             # Use the payment ID as the transaction ID
#             payment.transaction_id = payment.id
#             payment.save()

#             # Charge the payment
#             payment.change_status('pending')
#             payment.capture()

#             if payment.status == 'confirmed':
#                 # Update the appointment status to booked
#                 appointment = Appointment.objects.get(id=request.session.get('appointment_id'))
#                 appointment.status = 'booked'
#                 appointment.save()

#                 # Clear the cart
#                 cart = Cart(request)
#                 cart.clear()

#                 messages.success(request, "Su cita ha sido agendada!")
#                 return redirect("appointments:appointment_detail", appointment_id=appointment.id)
#             else:
#                 # Delete the appointment if payment fails
#                 appointment = Appointment.objects.get(id=request.session.get('appointment_id'))
#                 appointment.delete()

#                 messages.error(request, "No se pudo procesar su pago.")
#                 return redirect("appointments:checkout")
#     else:
#         form = PaymentForm()

#     # Create the appointment object with a "pending" status
#     appointment = Appointment.objects.create(
#         professional_id=request.session.get("professional_id"),
#         service_id=request.session.get("service_id"),
#         start_time=appointment_details["start_time"],
#         end_time=appointment_details["end_time"],
#         user=request.user,
#         status='pending'
#     )

#     # Save the appointment ID in the session
#     request.session['appointment_id'] = appointment.id

#     return render(
#         request,
#         "appointments/checkout.html",
#         {
#             "form": form,
#             "professional": professional,
#             "service": service,
#             "start_time": start_time,
#             "end_time": end_time,
#             "appointment_id": appointment.id
#         },
#     )

from django.shortcuts import render, redirect
from urllib.parse import urlencode
from django.contrib import messages
from django.http import HttpResponseBadRequest


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

        if payment_method == "mercadopago":
            # Prepare the data needed to redirect the user to the MercadoPago payment page
            # (e.g., the order ID, the amount to be paid, the return URL, etc.)
            # Example data for MercadoPago payment redirect
            data = {
                "preference_id": "<YOUR_PREFERENCE_ID>",
                "site_id": "MCO",
                "external_reference": "<YOUR_EXTERNAL_REFERENCE>",
                "customer_email": "<CUSTOMER_EMAIL>",
                "back_url": "<YOUR_BACK_URL>",
                "notification_url": "<YOUR_NOTIFICATION_URL>",
                "auto_return": "approved",
                "binary_mode": "true",
                "items": [
                    {
                        "id": "<ITEM_ID>",
                        "title": "<ITEM_TITLE>",
                        "description": "<ITEM_DESCRIPTION>",
                        "quantity": "<ITEM_QUANTITY>",
                        "unit_price": "<ITEM_UNIT_PRICE>",
                        "currency_id": "<ITEM_CURRENCY>",
                    }
                ],
                "payer": {
                    "name": "<CUSTOMER_NAME>",
                    "surname": "<CUSTOMER_SURNAME>",
                    "email": "<CUSTOMER_EMAIL>",
                    "phone": {
                        "area_code": "<CUSTOMER_PHONE_AREA_CODE>",
                        "number": "<CUSTOMER_PHONE_NUMBER>",
                    },
                    "identification": {
                        "type": "<CUSTOMER_IDENTIFICATION_TYPE>",
                        "number": "<CUSTOMER_IDENTIFICATION_NUMBER>",
                    },
                    "address": {
                        "zip_code": "<CUSTOMER_ZIP_CODE>",
                        "street_name": "<CUSTOMER_STREET_NAME>",
                        "street_number": "<CUSTOMER_STREET_NUMBER>",
                    },
                },
            }
            # Redirect the user to the MercadoPago payment page
            return redirect(
                "https://www.mercadopago.com/checkout/v1/redirect?" + urlencode(data)
            )

        elif payment_method == "cash":
            # Create the appointment object as before
            appointment = Appointment.objects.create(
                professional_id=professional_id,
                service_id=service_id,
                appointment_slot_id = slot_id,
                date = parsed_appointment_date_solo,

            )

            print("appo created: ", appointment)

            # Create the payment object with status 'pending'
            # payment = MyPayment.objects.create(
            #     appointment=appointment,
            #     amount=service.price,
            #     payment_method=payment_method,
            #     status=MyPayment.PENDING,
            # )


            messages.success(request, "Su cita ha sido agendada!")
            return redirect(
                "appointments:appointment_detail", appointment_id=appointment.id
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
            "end_time": end_time,
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
