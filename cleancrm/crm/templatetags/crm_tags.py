from django import template
from crm.models import Leads, Lead_comments


register = template.Library()  # Переменная нужна для декоратера


@register.simple_tag
def get_status(status):  # Функция которая будит возвращать список категорий на любой HTML
    style_dict = {
        'New': 'text-blue-400',
        'Refused': 'text-red-400',
        'Approved': 'text-green-400',
        'Need approved': 'text-yellow-400',
    }
    html = f'<p class="{style_dict[status]}">{status}</p>'
    return html

@register.simple_tag
def get_operator_leads(user):  # Функция которая будит возвращать список категорий на любой HTML
    return Leads.objects.filter(operator=user)

@register.simple_tag
def get_lead_detail_status_options(status):  # Функция которая будит возвращать список категорий на любой HTML
    options = [
        {'value': 'Approved', 'text': 'Approved', 'class': 'text-green-400'},
        {'value': 'New', 'text': 'New', 'class': 'text-blue-400'},
        {'value': 'Refused', 'text': 'Refused', 'class': 'text-red-400'},
        {'value': 'Need approved', 'text': 'Need approved', 'class': 'text-yellow-400'},
    ]

    html_options = []
    for option in options:
        selected = ' selected' if option['value'] == status else ''
        html_options.append(
            f'<option class="{option["class"]}" value="{option["value"]}"{selected}>{option["text"]}</option>'
        )

    return '\n'.join(html_options)

@register.simple_tag
def get_lead_detail_products_options(product):  # Функция которая будит возвращать список категорий на любой HTML
    options = [
        {'value': 'Lactos', 'text': 'Lactos'},
        {'value': 'Laditex', 'text': 'Laditex'},
        {'value': 'PerfectMan', 'text': 'PerfectMan'},
    ]

    html_options = []
    for option in options:
        selected = ' selected' if option['value'] == product else ''
        html_options.append(
            f'<option value="{option["value"]}"{selected}>{option["text"]}</option>'
        )

    return '\n'.join(html_options)


@register.simple_tag
def get_lead_detail_addresses_options(selected_region):
    options = [
        {'value': 'Tashkent', 'text': 'Tashkent'},
        {'value': 'Andijan', 'text': 'Andijan'},
        {'value': 'Bukhara', 'text': 'Bukhara'},
        {'value': 'Jizzakh', 'text': 'Jizzakh'},
        {'value': 'Kashkadarya', 'text': 'Kashkadarya'},
        {'value': 'Navoi', 'text': 'Navoi'},
        {'value': 'Namangan', 'text': 'Namangan'},
        {'value': 'Samarkand', 'text': 'Samarkand'},
        {'value': 'Surkhandarya', 'text': 'Surkhandarya'},
        {'value': 'Syrdarya', 'text': 'Syrdarya'},
        {'value': 'Tashkent region', 'text': 'Tashkent region'},
        {'value': 'Fergana', 'text': 'Fergana'},
        {'value': 'Khorezm', 'text': 'Khorezm'},
        {'value': 'Republic of Karakalpakstan', 'text': 'Republic of Karakalpakstan'},
    ]

    html_options = []
    for option in options:
        selected = ' selected' if option['value'] == selected_region else ''
        html_options.append(
            f'<option value="{option["value"]}"{selected}>{option["text"]}</option>'
        )

    return '\n'.join(html_options)


@register.simple_tag
def get_lead_comments(lead):
    comments: Lead_comments = Lead_comments.objects.filter(lead=lead)
    for i in comments:
        if i.owner:
            print(i.owner.owner.first_name)
    return comments