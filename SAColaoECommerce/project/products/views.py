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

'''
{
    "idusuario_empresa": 28,
    "nome": "SAColaoAdmin",
    "email": "admin@sac.com",
    "senha": "5f4dcc3b5aa765d61d8327deb882cf99",
    "api_key": "daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f"
}
{ 
  "nome_fantasia" : "SAColão E-Commerce",
  "cnpj" : "12345678901200"
}
{
    "idempresa": 1033,
    "nome_fantasia": "SAColão E-Commerce",
    "cnpj": "12345678901200",
    "idusuario_empresa": 28,
    "admin": "SAColaoAdmin"
}

# Objeto JSON para cadastrar um produto
{
"codigo" : varchar,
"nome" : varchar,
"idcategoria" : int,
"preco" : float,
"peso" : float,
"dimensao_a" : float,
"dimensao_c" : float,
"dimensao_l" :float,
"idempresa" : int,
"imagem_url" : varchar,
"campos" : vetor {idcampo, valor}, valor é o valor que o campo recebe
}

'''
# Variaveis globais
api_key = 'Bearer 672aeb004b2ce0ebcc8c6627d596b29f8097f0fd8a2c49d4c491d172f7a73c2c'
headers = {'Authorization': api_key, 'Content-Type': 'application/json'}
# id_empresa = '1033'
id_empresa = '1029'


# Retorna o requisition em formato json para o python
def format_json(requisition):
    body_unicode = requisition.body.decode('utf-8')
    return json.loads(body_unicode)

# Retorno para o front end
def django_message(message, status_code, content=None):
	return JsonResponse({
		'message'        : message,
		'status'         : status_code,
		'content'        : content,
		}
	)

@csrf_exempt
def get_products(request):
    response = requests.get('http://produtos.vitainformatica.com/api/produto?idempresa=%s' %id_empresa, headers=headers).json()
    # print (response)
    return django_message("Retornando todos produtos", 200, response)




@csrf_exempt
def get_products_by_category(request, token):
    response = requests.get('http://produtos.vitainformatica.com/api/produto?idempresa=%s' %id_empresa, headers=headers).json()

    filtered = []
    item = None
    for item in response:
        if(str(token).lower() in str(item['categoria']).lower()):
            filtered.append(item)

    return django_message("Retornando produtos filtrados por categoria", 200, filtered)



@csrf_exempt
def get_products_by_name(request, token):
    response = requests.get('http://produtos.vitainformatica.com/api/produto?idempresa=%s' %id_empresa, headers=headers).json()

    filtered = []
    item = None
    for item in response:
        if(str(token).lower() in str(item['nome']).lower()):
            filtered.append(item)

    return django_message("Retornando produtos filtrados por nome", 200, filtered)
