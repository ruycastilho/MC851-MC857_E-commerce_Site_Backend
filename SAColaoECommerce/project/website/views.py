from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.http import HttpResponse
from django.http import JsonResponse

# Django Login system
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.models import User

# Permitir requisoces do Postman
from django.views.decorators.csrf import csrf_exempt

from . import models
# from .serializer import ClientSerializer, ProductSerializer, OrderSerializer
import requests
from rest_framework import viewsets
import json
from django.core import serializers
from jsonfield import JSONField

# Retorno para o front end
def django_message(message, status_code, content=None):
	return JsonResponse({
		'message'        : message,
		'status'         : status_code,
		'content'        : content,
		}
    )

# Tag para permitir requisicoes do Postman
@csrf_exempt
def create_user_view(request):

    json_data=json.loads(request.body.decode('utf-8'))

    username = json_data['username']
    email = json_data['email']
    password = json_data['password']
    cpf = json_data['cpf']
    address = json_data['address']

    print(json_data)
    user = User.objects.create_user(username, email, password)
    client = models.Client.objects.create(user=user, cpf=cpf, address=address, credit='valid')
    client.save()
    return JsonResponse({'Status':'Success'})

@csrf_exempt
def change_email(request):

    json_data=json.loads(request.body.decode('utf-8'))
    new_email = json_data['email']

    user = get_user(request)
    client = user.client

    client.email = new_email
    client.save()
    return django_message("Email alterado", 200, '')


# Tag para permitir requisicoes do Postman
@csrf_exempt
def login_view(request):

    json_data=json.loads(request.body.decode('utf-8'))
    username = json_data['username']
    password = json_data['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return django_message("Logado", 200, '')
    else:
        return django_message("Erro", 404, '')


# Tag para permitir requisicoes do Postman
@csrf_exempt
def logout_view(request):
    logout(request)
    return django_message("Deslogado", 200, '')

@csrf_exempt
def get_all_orders(request):

    user = get_user(request)
    client = user.client

    orders = models.Order.objects.filter(user__cpf=client.cpf)
    data = json.loads(serializers.serialize("json", orders))
    
    response = []
    for x in data:
        fields = x['fields']
        fields['date_of_order'] =   fields['date_of_order'].replace("T", " ")
        fields['date_of_payment'] = fields['date_of_payment'].replace("T", " ")
        # fields['products'] = json.loads(fields['products'])

        # print(fields)
        response.append(fields)


    print(response)
    return django_message("Retornando todos pedidos", 200, response)

# @csrf_exempt
# def get_order_by_id(request, order_id):
#     order = models.Orders.objects.filter(order_id=order_id)

#     return JsonResponse({'Status':'Logged out'})
