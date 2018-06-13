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
import string
import unicodedata

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
api_key = 'Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f'
headers = {'Authorization': api_key, 'Content-Type': 'application/json'}
id_empresa = '1033'
# id_empresa = '1029'


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

    return django_message("Retornando todos produtos", 200, response)




@csrf_exempt
def get_products_by_category(request, token):
    response = requests.get('http://produtos.vitainformatica.com/api/produto?idempresa=%s' %id_empresa, headers=headers).json()

    words = str(token).split(" ")
    filtered = []
    item = None
    for item in response:
        for word in words:
            if ( str(word).lower() in str(item['categoria']).lower() or str(word).lower() in remove_accents(item['categoria'])):
                filtered.append(item)

    return django_message("Retornando produtos filtrados por categoria", 200, filtered)



@csrf_exempt
def get_products_by_name(request, token):
    response = requests.get('http://produtos.vitainformatica.com/api/produto?idempresa=%s' %id_empresa, headers=headers).json()

    words = str(token).split(" ")
    filtered = []
    item = None
    for item in response:
        for word in words:
            if ( str(word).lower() in str(item['nome']).lower() or str(word).lower() in remove_accents(item['nome']) ):
                filtered.append(item)

    result = []
    [result.append(item) for item in filtered if item not in result]           

    return django_message("Retornando produtos filtrados por nome", 200, result)


@csrf_exempt
def get_products_by_name_or_category(request, cat, name):
    response = requests.get('http://produtos.vitainformatica.com/api/produto?idempresa=%s' %id_empresa, headers=headers).json()

    words = str(name).split(" ")
    filtered = []
    item = None
    for item in response:
        for word in words:
            if ( (str(word).lower() in str(item['nome']).lower()) and ( str(cat).lower() == str(item['categoria'].lower() ) ) ):
                filtered.append(item)

    result = []
    [result.append(item) for item in filtered if item not in result]           

    return django_message("Retornando produtos filtrados por nome", 200, result)

@csrf_exempt
def get_stock(request, product_id):
    param={'idproduto' : product_id}
    response = requests.get('http://produtos.vitainformatica.com/api/saldo/atual', params=param, headers=headers).json()
    return django_message("Retornando saldo de produto", 200, response['saldo_final'])

def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

# def get_stock_all(product_id):
#     response = requests.get('http://produtos.vitainformatica.com/api/saldo/atual?idproduto=%s&idempresa=%s' %(product_id, id_empresa), headers=headers).json()

#     return response['saldo_final']