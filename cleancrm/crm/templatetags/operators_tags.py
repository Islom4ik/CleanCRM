import time
from datetime import datetime

import pytz
from django import template
from crm.models import AccountDatas, Leads

register = template.Library()

@register.simple_tag
def get_lead_activities_percentage(lead_activities:dict):
    result = {}
    for i in lead_activities:
        if lead_activities[i] == 0: lead_activities[i] = 1

    total = sum(lead_activities.values())
    for i in lead_activities:
        result[i] = round((lead_activities[i] * 100) / total, 2)

    return result

@register.simple_tag
def calculate_operator_attendance(attendance:dict):
    weekly_total = 6
    monthly_total = 30

    data_dict = attendance.copy()

    del data_dict['started_working']
    del data_dict['end_working']

    if sum(data_dict.values()) == 0:
        return {"weekly": 0, "monthly": 0}

    for i in data_dict:
        if data_dict[i] == 0: data_dict[i] = 1

    result = {}

    for i in data_dict:
        if i == 'weekly':
            result[i] = round((data_dict[i] * 100) / weekly_total, 2)
        else:
            result[i] = round((data_dict[i] * 100) / monthly_total, 2)

    return result

@register.simple_tag
def unix_to_time_format(unix_time:int):
    if not unix_time:
        return {
            'hours': '00',
            'minutes': '00',
            'seconds': '00'
        }

        # Временная зона Ташкента
    tz_tashkent = pytz.timezone('Asia/Tashkent')

    # Конвертируем Unix-время в объект datetime
    dt_utc = datetime.utcfromtimestamp(unix_time).replace(tzinfo=pytz.utc)

    # Преобразуем в локальное время Ташкента
    dt_local = dt_utc.astimezone(tz_tashkent)

    return {
        'hours': dt_local.strftime('%H'),
        'minutes': dt_local.strftime('%M'),
        'seconds': dt_local.strftime('%S')
    }

@register.simple_tag
def calculate_revenue(operator):
    operator_db: AccountDatas = AccountDatas.objects.get(id=operator)
    datas = eval(operator_db.datas)
    approved_operator_leads = Leads.objects.filter(pk__in=datas['leads'], status='Approved')
    needapproved_operator_leads = Leads.objects.filter(pk__in=datas['leads'], status='Need approved')
    approved_earned = sum([i.price for i in approved_operator_leads if i.price != None])
    needapproved_earned = sum([i.price for i in needapproved_operator_leads if i.price != None])
    return {'approved': f"{approved_earned:,}", 'need_approved': f"{needapproved_earned:,}"}

@register.simple_tag
def calculate_regwards(operator):
    operator_db: AccountDatas = AccountDatas.objects.get(id=operator)
    datas = eval(operator_db.datas)
    approved_operator_leads = Leads.objects.filter(pk__in=datas['leads'], status='Approved', regwarded=False)
    approved_earned = sum([i.price for i in approved_operator_leads if i.price != None])
    total = 15_000_000
    percentage = (approved_earned * 100) // total
    multiplier = percentage // 25
    claim_price = 1_000_000 * multiplier
    return {'percentage': percentage, 'claim_price': claim_price}