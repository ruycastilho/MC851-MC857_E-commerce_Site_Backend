from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.http import HttpResponse
from django.http import JsonResponse

# Permitir requisoces do Postman
from django.views.decorators.csrf import csrf_exempt

import requests
import json
from .cart import Cart

# Variaveis globais
api_key = 'Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f'
headers = {'Authorization': api_key, 'Content-Type': 'application/json'}
id_empresa = '1033'

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

# Retorna um dicionario com as informacoes do produto
def get_product_info(product_id):
	payload = {'idempresa': id_empresa, 'idproduto': product_id}
	response = requests.get('http://produtos.vitainformatica.com/api/produto', headers=headers, params=payload).json()
	return response[0]

# Retorna a quantidade do item no estoque
#  http://produtos.vitainformatica.com/api/saldo/atual?idproduto=174&idempresa=1029
def check_quantity(product_id, quantity):
	response = requests.get('http://produtos.vitainformatica.com/api/saldo/atual?idproduto=%s' %product_id, headers=headers).json()

	print(response)
	if(int(quantity) > response['saldo_final']):
		return -1
	elif(int(quantity) <= 0):
		return -2
	return 0

# Metodos para alterar o estoque. Assumir que a quantia a ser decrementada é válida
def decrease_quantity(product_id, quantity):
	payload = {'idempresa': id_empresa, 'idproduto': product_id, 'quantidade': quantity}
	response = requests.post('http://produtos.vitainformatica.com/api/movimento_estoque/vender', json=payload, headers=headers)

def increase_quantity(product_id, quantity):
	payload = {'idempresa': id_empresa, 'idproduto': product_id, 'quantidade': quantity}
	response = requests.post('http://produtos.vitainformatica.com/api/movimento_estoque/estornar', json=payload, headers=headers)

# Retorna preco e dimensoes
def get_product_specs(product_id):
	largest = 0
	infos = get_product_info(product_id)
	length, width, height = int(infos['dimensao_c']), int(infos['dimensao_l']), int(infos['dimensao_a'])
	price = infos['preco']
	weight = infos['peso']
	nome = infos['nome']
	descricao = infos['descricao']
	category = infos['categoria']
	url = infos['imagem_url']
	return [price, weight, length, width, height, nome, descricao, url, category]

# API's

# Adicionar produto ao carrinho
# Receber json com ao menos produt_id e product_quantity nos campos
# ex de chamada: http://localhost:8000/cart/add_product/ (POST) com body:
# {
# 	"product_id" : "2d4636de-47c5-4a9a-b196-6a46c6f48a58",
# 	"product_quantity" : "12"
# }
# Devolve sinal 200 em sucesso, 404 em falha
@csrf_exempt
def add_product(requisition):
	cart = Cart(requisition)
	body=json.loads(requisition.body.decode('utf-8'))
	print(body)
	if(check_quantity(body['product_id'], body['product_quantity']) == -1):
		return django_message("Nao existe quantia suficiente no estoque", 404)
	elif(check_quantity(body['product_id'], body['product_quantity']) == -2):
		return django_message("Quantia deve ser maior do que zero", 404)
	decrease_quantity(body['product_id'], body['product_quantity'])
	p, w, l, wid, h, n, d, url, category = get_product_specs(body['product_id'])
	cart.add_product(body['product_id'], body['product_quantity'], p, w, l, wid, h, n, d, url, category)
	return django_message("Produto adicionado no carrinho", 200)

# Atualizar quantidade de itens do produto no carrinho
# receber json com ao menos produt_id e product_quantity nos campos
# ex de chamada: http://localhost:8000/cart/update_product/ (POST) com body:
# {
# 	"product_id" : "2d4636de-47c5-4a9a-b196-6a46c6f48a58",
# 	"product_quantity" : "1"
# }
# Devolve sinal 200 em sucesso, 404 em falha
@csrf_exempt
def update_product(requisition):
	cart = Cart(requisition)
	body = format_json(requisition)
	quantity = check_quantity(body['product_id'], body['product_quantity'])

	if( quantity == -1):
		return django_message("Nao existe quantia suficiente no estoque", 404)
	elif(quantity == -2):
		return django_message("Quantia deve ser maior do que zero", 404)
	new_quantity = int(cart.get_product_quantity(body['product_id'])) - int(body['product_quantity'])
	if new_quantity < 0:
		decrease_quantity(body['product_id'], abs(new_quantity))
	else:
		increase_quantity(body['product_id'], abs(new_quantity))
	cart.update_product(body['product_id'], body['product_quantity'])
	return django_message("Produto atualizado no carrinho", 200)

# Remover item do carrinho
# receber json com ao menos produt_id
# ex de chamada: http://localhost:8000/cart/remove_product/ (POST) com body:
# {
# 	"product_id" : "2d4636de-47c5-4a9a-b196-6a46c6f48a58",
# 	"product_quantity" : "12"
# }
# Devolve sinal 200 em sucesso, 404 em falha
@csrf_exempt
def remove_product(requisition):
	cart = Cart(requisition)
	body = format_json(requisition)
	quantity = cart.remove_product(body['product_id'])
	# print(body['product_id'])
	# print(quantity)
	increase_quantity(body['product_id'], quantity)
	return django_message("Produto removido do carrinho", 200)

# Mostra itens do carrinho. Retorna o ID do produto do Produtos1 e a quantidade no carrinho
# nao precisa mandar nada, so um get
# ex de chamada: http://localhost:8000/cart/show_cart/ (GET)
# Devolve sinal 200
@csrf_exempt
def show_cart(requisition):
	cart = Cart(requisition)
	cart_itens = cart.get_cart_itens()
	return django_message("Mostrando carrinho", 200, cart_itens)

# Mostra valor total do frete para o carrinho em reais.
# Deve receber um CEP e o tipo de entrega: PAC/SEDEX, formato json no BODY do request
# nao precisa mandar nada, so um get
# ex de chamada: http://localhost:8000/cart/get_frete_value/ (PUT)
# Devolve sinal 200
@csrf_exempt
def get_frete_value(requisition):
	cart = Cart(requisition)
	body = format_json(requisition)	
	content = cart.get_frete_price(body['CEP'], body['tipoEntrega'])
	return django_message("Mostrando frete, valor em reais", 200, content['preco_frete'])


# Mostra valor total dos itens no carrinho em reais.
# nao precisa mandar nada, so um get
# ex de chamada: http://localhost:8000/cart/get_cart_value/ (GET)
# Devolve sinal 200
@csrf_exempt
def get_cart_value(requisition):
	cart = Cart(requisition)
	content = cart.get_cart_price()
	return django_message("Mostrando preco carrinho", 200, content)

# Mostra valor total dos itens no carrinho + frete em reais.
# Deve receber um CEP e o tipo de entrega: PAC/SEDEX, formato json no BODY do request
# ex de chamada: http://localhost:8000/cart/get_cart_value/ (PUT)
# Devolve sinal 200
@csrf_exempt
def get_total_value(requisition):
	cart = Cart(requisition)
	body = format_json(requisition)	
	content = cart.get_total_price(body['CEP'], body['tipoEntrega'])	
	return django_message("Mostrando preco total", 200, content)

# Limpa o carrinho e recoloca os itens no estoque
# @csrf_exempt
# def clear_cart(requisition):
# 	cart = Cart(requisition)
# 	cart_itens = cart.get_cart_itens()
# 	for product_id in cart_itens:
# 		increase_quantity(product_id, cart_itens[product_id]['quantity'])
# 	cart.clear_session()
# 	return django_message("Clearing cart", 404, 'content')