from django import template
from datetime import datetime
import pytz
from django.utils import timezone

register = template.Library()

MONTH_NAMES_ES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre",
}


def format_date(value):
    date_obj = datetime.strptime(value, "%d-%m-%Y")
    day = date_obj.strftime("%-d")
    month = MONTH_NAMES_ES[int(date_obj.strftime("%-m"))]
    year = date_obj.strftime("%Y")
    return f"{day} de {month} de {year}"


register.filter("format_date", format_date)


@register.filter
def is_after_now(value):
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')
    current_time_argentina = timezone.now().astimezone(argentina_tz)

    if value.time() > current_time_argentina.time():
        return 1
    else:
        return 0

    


