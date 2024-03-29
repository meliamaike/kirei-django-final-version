from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from staff.forms import StaffLoginForm
from django.contrib.auth import authenticate
from agendas.models import Agenda
from orders.models import ProductOrder
from products.models import Product
from professionals.models import Professional
from customers.models import Customer
from appointments.models import Appointment
from my_payments.models import ProductPayment, AppointmentPayment, CartPayment
from django_plotly_dash import DjangoDash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash
import pandas as pd
import plotly.graph_objs as go
from services.models import Service, CategoryService
import plotly.express as px
from django.db.models import Count
from django.db.models.functions import Trunc
from orders.models import AppointmentOrder, ProductOrder
import datetime
import numpy as np
from django.views.decorators.http import require_GET
from django.urls import reverse
from itertools import groupby
from django.db.models import Sum
from datetime import date
from django.db.models import Q
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout
from django.contrib import messages


# STATISTICS
# Create a new Dash app
app = DjangoDash(
    "staff_statistic_dashboard", external_stylesheets=[dbc.themes.BOOTSTRAP]
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="products-category-chart"), width=6),
                dbc.Col(dcc.Graph(id="agenda-graph"), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="category-service-chart"), width=6),
                dbc.Col(dcc.Graph(id="professional-graph"), width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="payment-chart"), width=8),
                dbc.Col(dcc.Graph(id="customer-graph"), width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="most-reserved-service-graph"), width=12),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id="appointment-day-count"), width=12),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.H3("Cantidad de reservas")),
                dcc.Dropdown(
                    id="time-period",
                    options=[
                        {"label": "Por mes", "value": "month"},
                        {"label": "Por año", "value": "year"},
                    ],
                    value="month",
                ),
                dcc.Graph(id="appointment-count"),
            ]
        ),
        dbc.Row([dbc.Col(dcc.Graph(id="most-ordered-product"), width=12)]),
    ],
    fluid=True,
)


@app.callback(
    dash.dependencies.Output("category-service-chart", "figure"),
    [dash.dependencies.Input("category-service-chart", "hoverData")],
)
def category_service_chart(hoverData):
    categories = dict(CategoryService.objects.values_list("id", "category"))

    services = Service.objects.all().select_related("category")
    df_services = pd.DataFrame.from_records(
        services.values("id", "service", "category__id")
    )

    # Replace the category IDs with their human-readable names
    df_services["category"] = df_services["category__id"].apply(
        lambda x: categories.get(x)
    )

    # Count the number of services in each category
    service_counts = df_services["category"].value_counts()

    colors = ["#CC89CB", "#D36378", "#7F3C56", "#D98B9D", "#472333", "#C92E4F"]

    # Create a bar chart to display the results
    fig = go.Figure(
        data=[
            go.Bar(
                x=service_counts.index,
                y=service_counts.values,
                text=service_counts.values,
                textposition="auto",
                marker=dict(color=colors),
            )
        ],
        layout={
            "title": "Cantidad de servicios x Categoría",
            "xaxis_title": "Categoría",
            "yaxis_title": "Cantidad de Servicios",
            "yaxis": dict(tickmode="linear", tick0=1, dtick=1),
        },
    )

    return fig


# Productos x categoria
@app.callback(
    dash.dependencies.Output("products-category-chart", "figure"),
    [dash.dependencies.Input("products-category-chart", "hoverData")],
)
def products_category_chart(hoverData):
    products = Product.objects.all()
    category_counts = Product.objects.values("category").annotate(count=Count("id"))

    # create a list of the category labels and counts
    labels = [item["category"] for item in category_counts]
    counts = [item["count"] for item in category_counts]

    # create a pie chart trace
    trace = go.Pie(labels=labels, values=counts)

    # create the figure layout
    layout = go.Layout(title="Productos x Categorías")

    # create the figure object
    fig = go.Figure(data=[trace], layout=layout)

    # return the figure object
    return fig


# Cantidad de Agendas según horario de inicio
@app.callback(
    dash.dependencies.Output("agenda-graph", "figure"),
    [dash.dependencies.Input("agenda-graph", "hoverData")],
)
def update_agenda_graph(hoverData):
    # Query the database to get the counts per start_time
    agenda_counts = (
        Agenda.objects.values("start_time")
        .annotate(count=Count("id"))
        .order_by("start_time")
    )

    # Create the Plotly figure
    fig = {
        "data": [
            {
                "labels": [agenda["start_time"] for agenda in agenda_counts],
                "values": [agenda["count"] for agenda in agenda_counts],
                "type": "pie",
            }
        ],
        "layout": {"title": "Cantidad de Agendas según horario de inicio"},
    }
    return fig


# Cantidad de profesionales por día
@app.callback(
    dash.dependencies.Output("professional-graph", "figure"),
    [dash.dependencies.Input("professional-graph", "hoverData")],
)
def update_professional_graph(hoverData):
    # Query the database to get the counts per start_date
    professional_counts = (
        Professional.objects.annotate(start_day=Trunc("start_date", "day"))
        .values("start_day")
        .annotate(count=Count("id"))
        .order_by("start_day")
    )

    # Create a DataFrame from the queryset
    df = pd.DataFrame(professional_counts)

    df["start_day"] = pd.to_datetime(df["start_day"])

    fig = go.Figure()

    bar_trace = go.Bar(
        x=df["start_day"],
        y=df["count"],
        name="Cantidad de profesionales",
    )

    fig.add_trace(bar_trace)

    fig.update_layout(
        title="Cantidad de profesionales nuevos por día",
        xaxis=dict(
            title="Fecha de inicio",
            tickformat="%Y-%m-%d",
            tickmode="array",
            tickvals=df["start_day"],
            ticktext=df["start_day"].dt.strftime("%Y-%m-%d"),
            dtick="M1",  # Display ticks every 1 month
        ),
        yaxis=dict(title="Cantidad de profesionales"),
    )

    fig.update_yaxes(tickmode="linear", dtick=1)

    # Display the chart
    return fig


# Ganancias Totales por día
@app.callback(
    dash.dependencies.Output("payment-chart", "figure"),
    [dash.dependencies.Input("payment-chart", "hoverData")],
)
def update_payment_chart(hoverData):
    appointment_orders = AppointmentOrder.objects.all()
    cart_orders = ProductOrder.objects.all()

    # Create a list of dates and corresponding total payments for appointment orders
    appointment_dates = []
    appointment_totals = []
    for order in appointment_orders:
        date = order.created_at.date()
        if date in appointment_dates:
            appointment_totals[-1] += order.payment.total
        else:
            appointment_dates.append(date)
            appointment_totals.append(order.payment.total)

    # Create a list of dates and corresponding total payments for cart orders
    cart_dates = []
    cart_totals = []
    for order in cart_orders:
        date = order.created_at.date()
        if date in cart_dates:
            cart_totals[-1] += order.payment.cart_total
        else:
            cart_dates.append(date)
            cart_totals.append(order.payment.cart_total)

    # Create the plotly figure
    fig = go.Figure()

    # Add a trace for appointment payments
    fig.add_trace(
        go.Scatter(
            x=appointment_dates,
            y=appointment_totals,
            mode="lines",
            name="Ganancias x Turnos",
        )
    )

    # Add a trace for cart payments
    fig.add_trace(
        go.Scatter(x=cart_dates, y=cart_totals, mode="lines", name="Ganancias x Venta de productos")
    )

    # Set the x-axis label
    fig.update_xaxes(title_text="Fecha")

    # Set the y-axis label
    fig.update_yaxes(title_text="Ganancia Total")

    # Set the title of the figure
    fig.update_layout(title_text="Ganancias Totales por día")

    # Return the updated figure

    return fig


# Cantidad Total de Clientes
@app.callback(
    Output("customer-graph", "figure"), [Input("customer-graph", "hoverData")]
)
def update_customer_graph(n_clicks):
    total_customers = Customer.objects.filter(
        ~Q(is_admin=True) & ~Q(is_staff=True)
    ).count()
    
    
    fig = {
        "data": [
            {
                "x": ["Clientes totales"],
                "y": [total_customers],
                "type": "bar",
                "text": total_customers,
                "textposition": "auto",
            }
        ],
        "layout": {"title": "Cantidad Total de Clientes", "yaxis": {"dtick": 1}},
    }

    return fig


# Servicios más reservados
@app.callback(
    Output("most-reserved-service-graph", "figure"),
    [Input("most-reserved-service-graph", "hoverData")],
)
def update_most_reserved_service_graph(n):
    # Get all appointment payments and related services
    appointment_payments = AppointmentPayment.objects.all().prefetch_related("appointment__service")
    services = [payment.appointment.service for payment in appointment_payments]

    # Count the occurrences of each service
    service_counts = {
        service.service: services.count(service) for service in set(services)
    }

    # Create the bar chart figure

    colors = ["#CC89CB", "#D36378", "#7F3C56", "#D98B9D", "#472333"]
    fig = go.Figure(
        data=[
            go.Bar(
                x=list(service_counts.keys()),
                y=list(service_counts.values()),
                marker=dict(color=colors),
                text=list(service_counts.values()),
                textposition="auto",
            )
        ],
        layout={
            "title": "Servicios más reservados",
            "xaxis": {"title": "Servicio"},
            "yaxis": {"title": "Cantidad de veces reservado"},
        },
    )

    return fig



# Cantidad de reservas por día
@app.callback(
    Output("appointment-day-count", "figure"),
    [Input("appointment-day-count", "hoverData")],
)
def update_appointment_day_count(n):
    # Get all appointments and count the number of appointments per day
    appointments = AppointmentPayment.objects.all()

    df_appointments = pd.DataFrame.from_records(appointments.values("id", "appointment__date"))
    df_counts = df_appointments.groupby("appointment__date").count()

    # Create the scatter plot figure
    fig = go.Figure(
        data=[go.Scatter(x=df_counts.index, y=df_counts["id"], mode="lines+markers")],
        layout={
            "title": "Cantidad de reservas por día",
            "xaxis_title": "Fecha",
            "yaxis_title": "Cantidad de reservas",
            "yaxis": {"range": [0, df_counts["id"].max() + 1]},
        },
    )

    return fig


# Cantidad de reservas por mes y por año
@app.callback(Output("appointment-count", "figure"), [Input("time-period", "value")])
def update_appointment_count(time_period):
    # Get all appointment payments and count the number of payments per month/year
    appointment_payments = AppointmentPayment.objects.all()
    df_payments = pd.DataFrame.from_records(appointment_payments.values("id", "appointment__date"))

    df_payments["appointment__date"] = pd.to_datetime(df_payments["appointment__date"])

    if time_period == "month":
        df_counts = df_payments.groupby(
            df_payments["appointment__date"].dt.strftime("%Y-%m")
        )["id"].count()
        x_title = "Mes"
        y_title = "Cantidad de reservas"
    else:
        df_counts = df_payments.groupby(df_payments["appointment__date"].dt.strftime("%Y"))[
            "id"
        ].count()
        x_title = "Año"
        y_title = "Cantidad de reservas"

    # Create the bar chart figure
    fig = go.Figure(
        data=[go.Bar(x=df_counts.index, y=df_counts.values)],
        layout={"xaxis_title": x_title, "yaxis_title": y_title},
    )

    return fig





# Productos más ordenados
@app.callback(
    Output("most-ordered-product", "figure"), Input("most-ordered-product", "hoverData")
)
def most_ordered_product_chart(hoverData):
    orders = ProductOrder.objects.all()

    product_counts = {}
    for order in orders:
        products = ProductPayment.objects.filter(cart_payment=order.payment)
        for product in products:
            if product.product.name in product_counts:
                product_counts[product.product.name] += product.quantity
            else:
                product_counts[product.product.name] = product.quantity

    fig = px.pie(
        values=list(product_counts.values()),
        names=list(product_counts.keys()),
        title="Productos más ordenados",
    )

    return fig


# DASHBOARDS
def staff_statistic_dashboard(request):
    # render the template with the Dash app component
    return render(request, "staff/staff_statistic_dashboard.html")


def staff_main_dashboard(request):
    appointment_total_revenue = AppointmentPayment.objects.aggregate(
        total_revenue=Sum("total")
    )["total_revenue"]
    product_total_revenue = ProductPayment.objects.aggregate(
        total_revenue=Sum("total")
    )["total_revenue"]
    customer_count = Customer.objects.filter(is_admin=False, is_staff=False).count()
    most_booked_service = (
        Service.objects.annotate(reservation_count=Count("appointment"))
        .filter(reservation_count__gt=0)
        .order_by("-reservation_count")
        .first()
    )
    last_appointment = AppointmentPayment.objects.order_by("-id").first()

    last_order = ProductPayment.objects.order_by("-id").first()

    last_user = (
        Customer.objects.filter(is_admin=False, is_staff=False).order_by("-id").first()
    )
    context = {
        "appointment_total_revenue": appointment_total_revenue
        if appointment_total_revenue is not None
        else 0,
        "product_total_revenue": product_total_revenue
        if product_total_revenue is not None
        else 0,
        "customer_count": customer_count,
        "most_booked_service": most_booked_service,
        "last_appointment": last_appointment,
        "last_order": last_order,
        "last_user": last_user,
    }

    return render(request, "staff/main_dashboard.html", context)


def staff_login(request):
    form = StaffLoginForm(request=request)

    if request.method == "POST":
        form = StaffLoginForm(data=request.POST, request=request)
        if form.is_valid():
            # Authenticate the user
            email = form.cleaned_data.get("login")
            print("Email: ", email)
            password = form.cleaned_data.get("password")
            print("Pass: ", password)
            user = authenticate(request, username=email, password=password)
            if user is not None and user.is_staff:
                # Log the user in
                login(request, user)
                # Redirect to a success page

                return redirect("staff:staff_main_dashboard")
            elif not user.is_staff:
                # Return an 'invalid login' error message
                form.add_error(None, "Permiso denegado.")
        else:
            print(form.errors)
    else:
        form = StaffLoginForm()

    return render(request, "staff/staff_login.html", {"form": form})


def staff_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect("staff:staff_login")


def staff_appointments_dashboard(request):
    today = date.today()

    appointments = Appointment.objects.filter(
        Q(date__gte=today) | Q(date=today)
    ).order_by("date", "professional", "service")

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
                "customer": appointments_list[0].customer,
            }
        )

    return render(
        request,
        "staff/appointments_dashboard.html",
        {"grouped_appointments": grouped_appointments, 
         "appointments": appointments
        },
    )

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
@require_GET
def staff_cancel_appointment(request):
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
    }

    for appointment in appointments:
        for slot in appointment.appointment_slot.all():
            slot.booked = False
            slot.save()
        
        appointment.delete()

    # Render the HTML content of the email template
    html_message = render_to_string("staff/appointment_cancel_email.html", context)

    # Strip the HTML tags to generate the plain text version of the email
    plain_message = strip_tags(html_message)

    # Send the email
    send_mail(
        subject="Tuvimos que cancelar tu reserva",
        message=plain_message,
        from_email="hola@kirei.com", 
        recipient_list=[customer.email],  
        html_message=html_message,
        fail_silently=False,
    )

    messages.success(
        request,
        "Reserva cancelada correctamente. Ya se le ha notificado al cliente en un e-mail.",
    )

    return redirect(reverse("staff:staff_appointments_dashboard"))


def staff_customers_dashboard(request):
    customers = Customer.objects.all()
    context = {"customers": customers}

    return render(request, "staff/customers_dashboard.html", context)


def staff_create_appointment(request):
    return render(request, "staff/create_appointment.html")


def not_available(request):
    return render(request, "staff/not_available.html")


def staff_orders_dashboard(request):
    orders = ProductOrder.objects.all()

    return render(request, "staff/orders_dashboard.html", {"orders": orders})


def orders_details(request, order_id, product_id):
    order = get_object_or_404(ProductOrder, pk=order_id)
    product = get_object_or_404(Product, pk=product_id)
    payment_method = order.payment.payment_method
    payment_status = order.payment.status
    payment_total = order.payment.cart_total
    specific_product = order.payment.productpayment_set.get(product_id=product_id)

    # get all ProductPayments with the same cart_payment_id
    product_payments = ProductPayment.objects.filter(
        cart_payment_id=specific_product.cart_payment_id
    )

    # sum the quantities of all ProductPayments
    total_quantity = product_payments.aggregate(Sum("quantity"))["quantity__sum"]

    return render(
        request,
        "staff/orders_details.html",
        {
            "order": order,
            "product": product,
            "payment_method": payment_method,
            "payment_status": payment_status,
            "payment_total": payment_total,
            "specific_product": specific_product,
            "total_quantity": total_quantity,
        },
    )




# Forgot password
def staff_password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = Customer.objects.filter(Q(email=data))
            if associated_users.exists() and associated_users.first().is_staff:
                for user in associated_users:
                    subject = "Cambio de contraseña"
                    email_template_name = "staff/password/password_reset_email.txt"
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    protocol = 'http' if request.is_secure() else 'https'

                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "Kirei estética",
                        "uid": uid,
                        "user": user,
                        "token": token,
                        "protocol": protocol,
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "hola@kirei.com",
                            [user.email],
                            fail_silently=False,
                        )
                        messages.success(
                            request,
                            "Te enviamos un e-mail con las instrucciones para poder cambiar la contraseña.",
                        )
                    except BadHeaderError:
                        messages.error(request, "Error. Intente más tarde por favor.")
                        return redirect("staff:staff_password_reset")
                    
                    return redirect("staff:staff_login")
            else:
                messages.error(request, "Error. No existe el usuario.")
                return redirect("staff:staff_password_reset")
        else:
            messages.error(request, "Error. Formulario inválido.")
            return redirect("staff:staff_password_reset")
    
    password_reset_form = PasswordResetForm()

    return render(
        request=request,
        template_name="staff/password/password_reset_form.html",
        context={"form": password_reset_form},
    )

