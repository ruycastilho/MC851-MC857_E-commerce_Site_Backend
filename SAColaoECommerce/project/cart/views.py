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

# Esta é uma funcao de auxilio para as API's definidas abaixo
def get_product_info(product_id):
	response = requests.get('https://ftt-catalog.herokuapp.com/products/%s' %product_id)
	json_result=json.loads(response.text)
	# print(json_result['stock'])
	return json_result

def check_quantity(product_id, quantity):
	infos = get_product_info(product_id)
	if(int(quantity) > infos['stock']):
		return -1
	elif(int(quantity) <= 0):
		return -2

def product_existance(product_id):
	infos = get_product_info(product_id)
	if(infos['status'] == 404):
		return False
	return True

def get_product_specs(product_id):
	largest = 0
	infos = get_product_info(product_id)
	length, width, height = int(infos['length']), int(infos['width']), int(infos['height'])
	price = infos['price']
	weight = infos['weight']
	max_dimention = str(largest)
	return [price, weight, length, width, height]

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
	body = format_json(requisition)
	if(product_existance(body['product_id']) == False):
		return django_message("Produto nao existe", 404)
	if(check_quantity(body['product_id'], body['product_quantity']) == -1):
		return django_message("Nao existe quantia suficiente no estoque", 404)
	elif(check_quantity(body['product_id'], body['product_quantity']) == -2):
		return django_message("Quantia deve ser maior do que zero", 404)
	p, w, l, wid, h = get_product_specs(body['product_id'])
	cart.add_product(body['product_id'], body['product_quantity'], p, w, l, wid, h)
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
	if(product_existance(body['product_id']) == False):
		return django_message("Produto nao existe", 404)
	if(check_quantity(body['product_id'], body['product_quantity']) == -1):
		return django_message("Nao existe quantia suficiente no estoque", 404)
	elif(check_quantity(body['product_id'], body['product_quantity']) == -2):
		return django_message("Quantia deve ser maior do que zero", 404)
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
	if(product_existance(body['product_id']) == False):
		return django_message("Produto nao existe", 404)	
	cart.remove_product(body['product_id'])
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
# nao precisa mandar nada, so um get
# ex de chamada: http://localhost:8000/cart/get_frete_value/ (GET)
# Devolve sinal 200
@csrf_exempt
def get_frete_value(requisition):
	CEP = '13091904'
	tipoEntrega = 'PAC'
	cart = Cart(requisition)
	content = cart.get_frete_price(CEP, tipoEntrega)
	return django_message("Mostrando frete, valor em centavos", 200, content)


# Mostra valor total dos itens no carrinho em reais.
# nao precisa mandar nada, so um get
# ex de chamada: http://localhost:8000/cart/get_cart_value/ (GET)
# Devolve sinal 200
@csrf_exempt
def get_cart_value(requisition):
	cart = Cart(requisition)
	content = cart.get_cart_price()
	return django_message("Mostrando preco carrinho", 200, content)
