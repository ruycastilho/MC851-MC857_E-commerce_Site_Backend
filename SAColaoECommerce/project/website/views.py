from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.http import HttpResponse
from django.http import JsonResponse

# Django Login system
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Permitir requisoces do Postman
from django.views.decorators.csrf import csrf_exempt

from . import models
from .serializer import ClientSerializer, ProductSerializer, OrderSerializer
import requests
from rest_framework import viewsets

# ViewSets

class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Client.objects.all()
    serializer_class = ClientSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Order.objects.all()
    serializer_class = OrderSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer


# Tag para permitir requisicoes do Postman
@csrf_exempt
def create_user_view(request):

    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    cpf = request.POST['cpf']
    address = request.POST['address']

    user = User.objects.create_user(username, email, password)
    client = Client.objects.Create(user=user, cpf=cpf, address=address)
    client.save()
    return JsonResponse({'Status':'Success'})

# Tag para permitir requisicoes do Postman
@csrf_exempt
def login_view(request):

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'Status':'Success'})
    else:
        return JsonResponse({'Status':'Invalid Login'})


# Tag para permitir requisicoes do Postman
@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'Status':'Logged out'})

@csrf_exempt
def get_all_orders(request):
    client = request.user

    orders = models.Orders.objects.filter(client__cpf=client.cpf)

    return JsonResponse({'Status':'Logged out'})

@csrf_exempt
def get_order_by_id(request, order_id):
    order = models.Orders.objects.filter(order_id=order_id)

    return JsonResponse({'Status':'Logged out'})
