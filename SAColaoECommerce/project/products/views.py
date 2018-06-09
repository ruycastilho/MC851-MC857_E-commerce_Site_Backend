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


# Retorna o requisition em formato json para o python
def format_json(requisition):
    body_unicode = requisition.body.decode('utf-8')
    return json.loads(body_unicode)

# Tag para permitir requisicoes do Postman

@csrf_exempt
def get_categories():
    header = {
        "Authorization" : "Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f"
    }

    response = requests.get('http://produtos.vitainformatica.com/api/categoria', headers = header)
    cat = Categories()

    cat.add_category()


@csrf_exempt
def get_campos():
    header = {
        "Authorization" : "Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f"
    }

    response = requests.get('http://produtos.vitainformatica.com/api/campos', headers = header)
    cat = Categories()

    cat.add_category()


@csrf_exempt
def get_products():
    header = {
        "Authorization" : "Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f"
    }

    response = requests.get('http://produtos.vitainformatica.com/api/produto?idempresa=1033', headers = header)
    prod = Products()

    prod.add_product()


@csrf_exempt
def add_product(request):
    body = format_json(request)

    payload = {
        "codigo" : body['codigo'],
        "nome" : body['nome'],
        "idcategoria" : body['idcategoria'],
        "preco" : body['preco'],
        "peso" : body['peso'],
        "dimensao_a" : body['dimensao_a'],
        "dimensao_c" : body['dimensao_c'],
        "dimensao_l" :body['dimensao_l'],
        "idempresa" : 1033,
        "imagem_url" : body['imagem_url'],
        "campos" : body['campos']
    }

    header = {
        "Authorization" : "Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f"
    }

    response = requests.post('http://produtos.vitainformatica.com/api/produto', json = payload, headers = header)

    #pega o idproduto recem criado para criar o saldo dele
    response = format_json(response)

    payload = {
        "idproduto" : response['idproduto'],
        "quantidade" : body['quantidade']
    }

    response = requests.put('http://produtos.vitainformatica.com/api/saldo', json = payload, headers = header)


@csrf_exempt
def update_product(request):
    body = format_json(request)

    payload = {
        "codigo" : body['codigo'],
        "nome" : body['nome'],
        "idcategoria" : body['idcategoria'],
        "preco" : body['preco'],
        "peso" : body['peso'],
        "dimensao_a" : body['dimensao_a'],
        "dimensao_c" : body['dimensao_c'],
        "dimensao_l" :body['dimensao_l'],
        "idempresa" : 1033,
        "imagem_url" : body['imagem_url'],
        "campos" : body['campos']
    }

    header = {
        "Authorization" : "Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f"
    }

    response = requests.put('http://produtos.vitainformatica.com/api/produto?idempresa=1033&idusuario_empresa=28', json = payload, headers = header)

@csrf_exempt
def saldo_produto(request):
    header = {
        "Authorization" : "Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f"
    }

    response = requests.get('http://produtos.vitainformatica.com/api/saldo?idproduto=%s' %(request['idproduto']) , headers = header)


@csrf_exempt
def consulta_movimento(request):
    header = {
        "Authorization" : "Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f"
    }

    response = requests.get('http://produtos.vitainformatica.com/api/movimento_estoque', headers = header)


@csrf_exempt
def estornar_estoque(request):
    body = format_json(request)

    header = {
        "Authorization" : "Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f"
    }

    payload = {
        "idproduto" : body['idproduto'],
        "quantidade" : body['quantidade']
    }

    response = requests.get('http://produtos.vitainformatica.com/api/movimento_estoque/estornar', json = payload, headers = header)


@csrf_exempt
def vender_estoque(request):
    body = format_json(request)

    header = {
        "Authorization" : "Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f"
    }

    payload = {
        "idproduto" : body['idproduto'],
        "quantidade" : body['quantidade']
    }

    response = requests.get('http://produtos.vitainformatica.com/api/movimento_estoque/vender', json = payload, headers = header)
