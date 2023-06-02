from django import template

register = template.Library()


@register.filter
def get_range(value):
    return range(value)


@register.filter
def convert_category_key(value):
    category_mapping = {
        "cuidado-facial": "Cuidado de la Piel",
        "maquillaje": "Maquillaje",
        "cuidado-corporal": "Cuidado Corporal",
        "perfumes": "Perfumes",
        "labios": "Labios",
        "cejas": "Cejas",
        "ojos": "Ojos",
        "nails": "Nails",
        "accesorios": "Accesorios",
        "baño-y-ducha": "Baño y Ducha",
        "exfoliantes": "Exfoliantes",
        "hidratantes": "Hidratantes",
        "aceites": "Aceites",
        "protectores-solares": "Protectores Solares",
        "manos": "Manos",
        "pies": "Pies",
    }
    return category_mapping.get(value, value)
