from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from datetime import datetime
import time

def get_user_by_session_id(session_id):
    try:
        session = Session.objects.get(session_key=session_id)
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        if user_id:
            return User.objects.get(pk=user_id)
    except:
        return None

def sort_leads_by_date(leads):
    sorted_leads = sorted(leads, key=lambda lead: datetime.strptime(lead.request_date, '%d/%m/%Y'))
    sorted_leads = sorted_leads[::-1]
    return sorted_leads

def date_to_unix(date_string):
    date_obj = datetime.strptime(date_string, '%d/%m/%Y')
    unix_time = int(time.mktime(date_obj.timetuple()))
    return unix_time


def get_months_until(month):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    if month not in months:
        raise ValueError("Invalid month name")

    index = months.index(month)
    current_year = datetime.now().year
    result = []

    for i in range(6):
        # Вычисляем текущий индекс месяца с учетом перехода года
        current_index = (index - 5 + i) % 12
        year_adjustment = (index - 5 + i) // 12
        # Определяем, нужно ли увеличивать год
        year = current_year + year_adjustment
        result.append(f"{months[current_index]}_{year}")

    return result


def get_month_name_by_index(index):
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    if index < 0 or index > 11:
        raise ValueError("Invalid index. Please provide a value between 0 and 11.")

    return months[index]