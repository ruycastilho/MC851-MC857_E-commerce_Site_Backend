from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.http import HttpResponse
from django.http import JsonResponse

# Permitir requisoces do Postman
from django.views.decorators.csrf import csrf_exempt

import requests
import json
from .products import Products

# Retorna o requisition em formato json para o python
def format_json(requisition):
    body_unicode = requisition.body.decode('utf-8')
    return json.loads(body_unicode)

# Tag para permitir requisicoes do Postman

@csrf_exempt
def search_products_by_name(request):
    response = requests.get('https://ftt-catalog.herokuapp.com/products/?name=%s' %(request['product_name']) )


@csrf_exempt
def search_products_by_category(request):
    response = requests.get('https://ftt-catalog.herokuapp.com/categories/?name=%s' %(request['category_name']) )



@csrf_exempt
def reserve_product(request):
    response = requests.put('https://ftt-catalog.herokuapp.com/reservation/reserve/%s' %(request['productId']) )


@csrf_exempt
def release_product(request):   
    response = requests.put('https://ftt-catalog.herokuapp.com/reservation/release/%s' %(request['productId']))

    
@csrf_exempt
def get_categories():
    response = requests.get('https://ftt-catalog.herokuapp.com/categories/')
    cat = Categories()

    cat.add_category()
    
@csrf_exempt
def get_products():
    response = requests.get('https://ftt-catalog.herokuapp.com/products/')
    prod = Products()

    prod.add_product()

@csrf_exempt
def add_product(request):
    body = format_json(request)

    payload = {
        'name' : body['name'],
        'description' : body['description'],
        'price' : body['price'],
        'stock' : body['stock'],
        'brand' : body['brand'],
        'highlight' : body['highlight'],
        'categoryId' : body['categoryId'],
        'imageUrl' : body['imageUrl'],
        'additionalInfo' : body['additionalInfo']
    }

    response = requests.post('https://ftt-catalog.herokuapp.com/products/', json = payload)

@csrf_exempt
def add_category(request):
    body = format_json(request)

    payload = {
        'name' : body['name'],
        'description' : body['description'],
        'parentId'  : body['parentId'],
        'additionalInfo' : body['additionalInfo'],
        'status' : body['status']
    }   
    
    response = requests.post('https://ftt-catalog.herokuapp.com/categories/', json = payload)
