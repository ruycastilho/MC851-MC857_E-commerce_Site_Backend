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
import requests
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

    user = get_user(request)
    user2 = request.user
    # print(user)
    # print("")
    # print(user2)

    json_data=json.loads(request.body.decode('utf-8'))

    username = json_data['username']
    email = json_data['email']
    password = json_data['password']
    cpf = json_data['cpf']
    address = json_data['address']

    print(json_data)

    find1 = models.Client.objects.filter(cpf=cpf)
    find2 = models.Client.objects.filter(user__username=username)

    if not find1 and not find2:
     
        user = User.objects.create_user(username, email, password)

        client = models.Client.objects.create(user=user, email=email, cpf=cpf, address=address, credit='valid')
        client.save()

        return django_message("Usuário foi cadastrado", 200, "")

    else:
   
        return django_message("Usuário já existe com este CPF", 400, "")

@csrf_exempt
def change_email(request):

    json_data=json.loads(request.body.decode('utf-8'))
    new_email = json_data['email']

    user = get_user(request)
    client = user.client

    client.email = new_email
    client.save()
    
    return django_message("Email alterado", 200, '')


@csrf_exempt
def get_info(request):

    user = get_user(request)
    client = user.client
    email = client.email
    cpf = client.cpf
    address = client.address

    # print (email + "!")

    content = {
        'email'         : email,
        'cpf'           : cpf,
        'address'       : address,
    }

    # content = {
    #     'email'         : "teste email",
    #     'cpf'           : "teste cpf",
    #     'address'       : "teste endereco",
    # }

    return django_message("Email alterado", 200, content)



# Tag para permitir requisicoes do Postman
@csrf_exempt
def login_view(request):

    json_data=json.loads(request.body.decode('utf-8'))
    username = json_data['username']
    password = json_data['password']
    print(username + " " + password)

    user = authenticate(request, username=username, password=password)
    print("LOGIN")

    # print(user.username)
    if user is not None:
        print("LOGIN")
        login(request, user)

        if request.user.is_authenticated:
            print(str(request.user.is_authenticated))
        return django_message("Logado", 200, '')
    else:
        return django_message("Erro", 404, str(request.user.is_authenticated))


# Tag para permitir requisicoes do Postman
@csrf_exempt
def logout_view(request):
    x=(str(request.user.is_authenticated))
    if request.user.is_authenticated:
        # x=(str(request.user.is_authenticated))
        print(str(request.user.is_authenticated))
    
    print(str(request.user.is_authenticated))

    
    logout(request)
    print("LOGOUT")

    return django_message("Deslogado", 200, x)

@csrf_exempt
def get_all_orders(request):

    user = get_user(request)
    client = user.client

    orders = models.Order.objects.filter(user__cpf=client.cpf)  #orderby
    data = json.loads(serializers.serialize("json", orders))
    
    response = []
    for x in data:
        fields = x['fields']
        fields['date_of_order'] =   fields['date_of_order'].replace("T", " ")
        fields['date_of_payment'] = fields['date_of_payment'].replace("T", " ")
        # fields['products'] = json.loads(fields['products'])

        # print(fields)
        response.append(fields)

    # products =[
    #     {
    #         'price'  : "R$ 25,00",
    #         'quantity' : "1",
    #         'url'    : "https://images-na.ssl-images-amazon.com/images/I/51ELLu0XQxL._SX317_BO1,204,203,200_.jpg",
    #         'nome'   : "Produto 1",
    #     },
    #     {
    #         'price'  : "R$ 25,00",
    #         'quantity' : "1",
    #         'url'    : "https://images-na.ssl-images-amazon.com/images/I/51ELLu0XQxL._SX317_BO1,204,203,200_.jpg",
    #         'nome'   : "Produto 2",
    #     },
    #     {
    #         'price'  : "R$ 25,00",
    #         'quantity' : "1",
    #         'url'    : "https://images-na.ssl-images-amazon.com/images/I/51ELLu0XQxL._SX317_BO1,204,203,200_.jpg",
    #         'nome'   : "Produto 3",
    #     },
    #     {
    #         'price'  : "R$ 25,00",
    #         'quantity' : "1",
    #         'url'    : "https://images-na.ssl-images-amazon.com/images/I/51ELLu0XQxL._SX317_BO1,204,203,200_.jpg",
    #         'nome'   : "Produto 4",
    #     }
    # ]

    # content = {
    #     'order_id'          : "teste id",
    #     'type_of_payment'   : "teste tipo de pagamento",
    #     'date_of_payment'   : "teste data de pagamento",
    #     'date_of_order'     : "teste data de entrega",
    #     'payment_status'    : "teste situação de pagamento",
    #     'delivery_status'   : "teste situação entrega",
    #     'delivery_code'     : "teste codigo",
    #     'address'           : "teste endereco",
    #     'price'             : "100,00",
    #     'products'          : products,

    # }
    # response = []
    # response.append(content)
    # response.append(content)
    # response.append(content)

    print(response)
    return django_message("Retornando todos pedidos", 200, response)

# @csrf_exempt
# def get_order_by_id(request, order_id):
#     order = models.Orders.objects.filter(order_id=order_id)

#     return JsonResponse({'Status':'Logged out'})
