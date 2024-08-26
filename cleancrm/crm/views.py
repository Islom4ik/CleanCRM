import json
import os
import re
import time
from datetime import datetime
from typing import List
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.serializers import serialize
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import LoginForm, OperatorCreationForm
from .models import AccountDatas, Leads, Lead_comments
from django.contrib.auth.models import User
from .serializers import LeadFilterSerializer, LeadSerializer, OperatorAddLeadsSerializer, LeadEditSerializer, \
    CommentsAddSerializer, LeadAddSerializer
from .extras import sort_leads_by_date, date_to_unix, get_user_by_session_id, get_months_until, get_month_name_by_index

# Create your views here.

# Main page
def crm_view(request):
    if not request.user.is_authenticated: return redirect(to='login')

    account_data: AccountDatas = AccountDatas.objects.get(owner=request.user.pk)

    leads_db: List[Leads] = Leads.objects.all()
    leads_json = serialize(format='json', queryset=leads_db)

    leads = []
    new_leads = [i for i in leads_db if i.status == 'New']
    other_leads = [i for i in leads_db if i.status != 'New']

    new_leads = sort_leads_by_date(new_leads)
    if account_data.role != 'Operator':
        new_leads_to_last = [i for i in new_leads if i.operator]
        new_leads = [i for i in new_leads if not i.operator]

        new_leads.extend(new_leads_to_last)


    other_leads = sort_leads_by_date(other_leads)

    leads.extend(new_leads)
    leads.extend(other_leads)

    operators = AccountDatas.objects.filter(role='Operator')

    chart_datas = []

    operators: List[AccountDatas] = AccountDatas.objects.filter(role='Operator')
    for i in operators:
        datas: dict = eval(i.datas)
        sold_count = datas.get('sold_count', None)
        if sold_count == None:
            datas['sold_count'] = 0
            i.datas = str(datas)
            i.save()
            sold_count = datas['sold_count']

        chart_datas.append({"name": i.owner.first_name, "count": sold_count+1})

    chart_datas = chart_datas[:3]
    chart_datas = sorted(chart_datas, key=lambda x: x['count'], reverse=True)


    # Chart profit
    current_month = datetime.now().strftime("%B")
    chart_profit_months = {}
    for i in get_months_until(current_month):
        chart_profit_months[i] = 0

    sold_leads = Leads.objects.filter(status='Approved')

    for i in sold_leads:
        if i.sold_date != None:
            sold_price = i.price
            sold_date_datas = i.sold_date.split('/')
            sold_month = sold_date_datas[1]
            sold_year = sold_date_datas[2]
            if sold_month[0] == '0': sold_month = int(sold_month[-1:])
            month_name = get_month_name_by_index(sold_month-1)
            chart_profit_months[f'{month_name}_{sold_year}'] += sold_price

    chart_profit_months = list(chart_profit_months.values())

    # Statuses chart
    all_leads = Leads.objects
    approved_count = all_leads.filter(status='Approved').count() or 1
    new_count = all_leads.filter(status='New').count() or 1
    refused_count = all_leads.filter(status='Refused').count() or 1
    needapproved_count = all_leads.filter(status='Need approved').count() or 1
    statuses_dataset = [{"name": "Approved", "count": approved_count}, {"name": "New", "count": new_count}, {"name": "Refused", "count": refused_count}, {"name": "Need approved", "count": needapproved_count}]

    return render(request=request, template_name='crm/crm.html', context={'title': 'CleanCRM - Main', 'leads': leads, 'leads_json': leads_json, 'operators': operators, 'account_data': account_data, 'chart_datas': chart_datas, 'statuses_dataset': statuses_dataset, 'chart_profit_months': chart_profit_months})


def view_operators_page(request):
    operators: List[AccountDatas] = AccountDatas.objects.filter(role='Operator')
    return redirect('operator', operators[0].pk)


def view_operator_page(request, pk):
    operators_db: List[AccountDatas] = AccountDatas.objects.filter(role='Operator')
    operator_db: AccountDatas = AccountDatas.objects.get(pk=pk)

    operators = []
    for i in operators_db:
        operators.append({'operator': i, 'datas': eval(i.datas)})

    operator = {"operator": operator_db, 'datas': eval(operator_db.datas)}

    account_data: AccountDatas = AccountDatas.objects.get(owner=request.user)
    return render(request=request, template_name='crm/operators.html',
                  context={'title': 'CleanCRM - Operators', 'account_data': account_data, 'operators': operators, 'operator': operator})


def login_page(request):
    if request.user.is_authenticated: return redirect(to='crm')
    if 'timeout' in request.session:
        timeout = request.session['timeout']
        current_unix = int(time.time())
        if current_unix < timeout:
            return render(request=request, template_name='crm/index.html')
        else:
            del request.session['timeout']
            request.session['login_try'] = 0

    if request.POST:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request=request, user=user)
                del request.session['login_try']
                return redirect(to='crm')
            else:
                for field in form.errors:
                    messages.error(request=request, message=form.errors[field].as_text())

                return render(request=request, template_name='crm/index.html', context={'form': form})
        else:
            request.session['login_try'] += 1
            login_trys = request.session['login_try']
            if login_trys >= 10:
                request.session['timeout'] = int(time.time()) + 120
                return redirect(to='login')

            for field in form.errors:
                messages.error(request=request, message=form.errors[field].as_text())

            return redirect(to='login')
    else:
        if 'login_try' not in request.session:
            request.session['login_try'] = 0

        form = LoginForm()

    return render(request=request, template_name='crm/index.html', context={'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request=request)

    return redirect(to='login')

def post_lead(request):
    if 'Name' in request.GET and 'PhoneNumber' in request.GET and 'Adress' in request.GET and 'Product' in request.GET and 'Date' in request.GET:
        Leads.objects.create(name=request.GET['Name'], phone=request.GET['PhoneNumber'], adress=request.GET['Adress'], product=request.GET['Product'], request_date=request.GET['Date'])
    return HttpResponse('OK')


def create_operator_view(request):
    if not request.user.is_superuser: return redirect(to='crm')

    if request.POST:
        form = OperatorCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()

            avatar = form.cleaned_data.get('avatar')
            if not avatar:
                if form.cleaned_data['gender'] == 'Male':
                    avatar = 'avatars/default_male_avatar.webp'
                else:
                    avatar = 'avatars/default_female_avatar.webp'
            else:
                avatar.name = f'{uuid4().hex}{os.path.splitext(avatar.name)[1]}'


            current_unix = int(time.time())
            datas = {'sold_count': 0, 'lead_activities': {'Approved': 0, 'Refused': 0, 'Need_approved': 0, 'New': 0}, 'attendance': {'weekly': 0, 'monthly': 0, 'started_working': None, 'end_working': None}, 'joined_to_company': current_unix, 'leads': [], 'personal_card': {'card_number': '**** **** **** ****', 'holder_name': 'Not specified', 'valid_thru': '**/**'}}

            AccountDatas.objects.create(owner=user, phone=form.cleaned_data['phone'], gender=form.cleaned_data['gender'], avatar=avatar, datas=datas)
            messages.success(request=request, message='Created ✅')
            return redirect(to='create_operator')
        else:
            for field in form.errors:
                messages.error(request=request, message=form.errors[field].as_text())

            return redirect(to='create_operator')

    form = OperatorCreationForm()

    return render(request=request, template_name='crm/create_operator.html', context={'title': 'CleanCRM - Create Operator', 'form': form})








# API
class API_Leads_get(APIView):
    def get(self, request):
        filter_serializer = LeadFilterSerializer(data=request.GET)
        filters = {}

        filter_serializer.is_valid(raise_exception=True)

        validated_data = filter_serializer.validated_data

        if 'date' in validated_data and validated_data['date'] != 'All':
            filters['request_date'] = validated_data['date']

        if 'operator' in validated_data and validated_data['operator'] != 'All':
            filters['operator'] = validated_data['operator']

        if 'product' in validated_data and validated_data['product'] != 'All':
            filters['product'] = validated_data['product']

        if 'status' in validated_data and validated_data['status'] != 'All':
            filters['status'] = validated_data['status']

        lst = Leads.objects.filter(**filters)
        print(lst)
        return Response({'leads': LeadSerializer(lst, many=True).data})


def is_valid_date(date_text):
    pattern = r'^([0-2][0-9]|3[01])/(0[1-9]|1[0-2])/([0-9]{4})$'
    match = re.match(pattern, date_text)
    return bool(match)

class API_Lead_post(APIView):
    def post(self, request):
        # user = get_user_by_session_id(session_id=request.data['session_key'])
        # latitude = request.data['latitude']
        # longitude = request.data['longitude']
        # serializer = LeadSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        # username = User.username
        # if not user:
        #     return Response({'saved': False})

        serializer = LeadAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        lead = serializer.create(validated_data=validated_data)
        if not is_valid_date(validated_data['request_date']):
            return Response({'bad_request': 'invalid request_date format'})

        # lead = Leads.objects.create(**validated_data)
        # print(lead)

        # print(f'{user.username} location:\n\nLatitude: {latitude}\n\nLongitude: {longitude}')
        return Response({'saved': True, 'lead': serializer.data})


class API_Lead_edit(APIView):
    def post(self, request):
        serializer = LeadEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        lead: Leads = Leads.objects.get(pk=validated_data['pk'])
        lead.phone = validated_data['lead_phone']
        lead.status = validated_data['lead_status']
        lead.product = validated_data['lead_product']
        lead.address = validated_data['lead_address']
        if validated_data['lead_soldcount']:
            lead.quantity = validated_data['lead_soldcount']

        if validated_data['lead_soldprice']:
            lead.price = validated_data['lead_soldprice']

        if validated_data['lead_callcount']:
            lead.call_count = validated_data['lead_callcount']

        if validated_data['lead_calldate']:
            lead.lead_calldate = validated_data['lead_calldate']

        if validated_data['solddate']:
            lead.sold_date = validated_data['solddate']

        lead.save()

        return Response({'saved': True})

class API_OperatorLead_post(APIView):
    def post(self, request):
        serializer = OperatorAddLeadsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        operator: AccountDatas = AccountDatas.objects.get(owner=validated_data['operator'])
        datas = eval(operator.datas)
        for i in validated_data['leads']:
            lead: Leads = Leads.objects.get(pk=i)
            lead.operator = operator.owner
            lead.save()
            datas['leads'].append(i)

        operator.datas = str(datas)
        operator.save()

        return Response({'saved': True})

class API_Operator_Avatar(APIView):
    def get(self, request):
        avatar = '/static/crm/images/clientIcon.jpg'
        if request.GET['pk'] != 'null':
            operator: AccountDatas = AccountDatas.objects.get(owner=int(request.GET['pk']))
            avatar = operator.avatar.url
        return Response({'avatar': avatar})


class API_Comment_Add(APIView):
    def post(self, request):
        serializer = CommentsAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        comment: Lead_comments = Lead_comments.objects.create(owner=validated_data['owner'], text=validated_data['text'], lead=validated_data['lead'])
        comments_count = Lead_comments.objects.filter(lead=validated_data['lead']).count()
        return Response({'saved': True, 'comments_count': comments_count, 'comment': CommentsAddSerializer(comment).data, 'commentator': {'first_name': comment.owner.owner.first_name or comment.owner.owner.username, 'role': comment.owner.role, 'avatar': comment.owner.avatar.url}})