from django.shortcuts import render
import requests
import json
from django.http import HttpResponse, HttpRequest, JsonResponse
from rest_framework import generics
from . import models
from . import serializer
from time import gmtime, strftime

# Permitir requisoces do Postman
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# Variavel global do site
site_id = '5b62f6bdbe9c399036412701aa662a7dc572100e'
base_url = 'http://centralatendimento-mc857.azurewebsites.net/tickets/'

def format_json(request):
	body_unicode = request.body.decode('utf-8')
	return json.loads(body_unicode)

# class TicketList(generics.ListCreateAPIView):
#     queryset = models.Ticket.objects.all()
#     serializer_class = serializer.SACSerializer

# class DetailTicket(generics.RetrieveUpdateDestroyAPIView):
#     queryset = models.Ticket.objects.all()
#     serializer_class = serializer.SACSerializer


# API's

# Adicionar ticket
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/add_ticket/ (POST) com body:
# {
# 	'message'  : 'Reclamação'
# }
# Devolve sinal 201 em sucesso, 400 em falha

# Tag para permitir requisicoes do Postman
@csrf_exempt
def add_ticket(request):
	body = format_json(request)
	# debug
	# print(body['sender'])

	payload={
		'timestamp': strftime('%Y-%m-%d %H:%M:%S', gmtime()),
  		'sender'   : request.user.client.cpf,
  		'message'  : body['message']
	}

	response = requests.post('http://centralatendimento-mc857.azurewebsites.net/tickets/%s/%s' %(site_id, request.user.client.cpf), json=payload)
	
	# debug
	# print(response.text)
	# print(response.status_code)

	django_response = HttpResponse(
		content      = response.content,
		status       = response.status_code,
		content_type = response.headers['Content-Type']
    )
	
	return django_response

# Adicionar ticket de pedido
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/add_ticket_order/ (POST) com body:
# {
# 	'message'  : 'Reclamação',
#	'order_id' : '1'
# }
# Devolve sinal 201 em sucesso, 400 em falha

@csrf_exempt
def add_ticket_order(request):
    body = format_json(request)

    payload={
		'timestamp': 'strftime("%Y-%m-%d %H:%M:%S", gmtime())',
  		'sender'   : request.user.client.cpf,
  		'message'  : body['message']
	}

    order_id = body['order_id']
    module_request = requests.post(base_url + '%s/%s/compra/%s' %(site_id, request.user.client.cpf, order_id), json=payload)

    django_response = HttpResponse(
		content      = response.content,
		status       = response.status_code,
		content_type = response.headers['Content-Type']
		)
	
    return django_response

# Adicionar mensagem a ticket
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/add_message_to_ticket/ (PUT) com body:
# {
# 	'message'  : 'Reclamação',
#	'ticket_id' : '1'
# }
# Devolve sinal 200 em sucesso, 400 em falha e 404 caso ticket não seja encontrado
@csrf_exempt
def add_message_to_ticket(request):
    body = format_json(request)
    ticket_id = body['ticket_id']

    payload={
		'timestamp': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
  		'sender'   : request.user.client.cpf,
  		'message'  : body['message']
	}
    
    module_request = requests.put(base_url + '%s/%s/id/%s' %(site_id, request.user.client.cpf, ticket_id), json=payload)

    response = module_request.json()

    return JsonResponse(response)

# Receber tickets de um cliente
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/get_all_tickets/ (GET);
# Devolve sinal 200 em sucesso, 400 em falha e 404 caso o site id esteja errado
@csrf_exempt
def get_all_tickets(request):
    module_request = requests.get(base_url + '%s/%s/' %(site_id, request.user.client.cpf))

    response = module_request.json()

    return JsonResponse(response)

# Receber ticket especifico de um cliente
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/get_ticket_by_number/1 (GET);
# Devolve sinal 200 em sucesso, 404 caso não encontre nenhum ticket e 400 caso o site id esteja errado
@csrf_exempt
def get_ticket_by_number(request, ticket_id):
    module_request = requests.get(base_url + '%s/%s/ticket/%s' %(site_id, request.user.client.cpf, ticket_id))

    response = module_request.json()

    return JsonResponse(response)

# Receber ticket especifico de um cliente por numero de pedido
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/get_ticket_by_order/1 (GET);
# Devolve sinal 200 em sucesso, 404 caso não encontre nenhum ticket e 400 caso o site id esteja errado
@csrf_exempt
def get_ticket_by_order(request, order_id):
    module_request = requests.get(base_url + '%s/%s/compra/%s' %(site_id, request.user.client.cpf, order_id))

    response = module_request.json()

    return JsonResponse(response)

# Encerrar ticket
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/close_ticket/ (DELETE) com body;:
# {
# 	'message'  : 'Encerrando ticket',
#	'ticket_id' : '1'
# }
# Devolve sinal 200 em sucesso, 404 caso não encontre nenhum ticket e 400 caso o site id esteja errado
@csrf_exempt
def close_ticket(request, ticket_id):
    body = format_json(request)

    payload={
		'timestamp': strftime("%Y-%m-%d %H:%M:%S", gmtime()),
  		'sender'   : request.user.client.cpf,
  		'message'  : body['message']
	}

    ticket_id = body['ticket_id']

    module_request = requests.delete(base_url + '%s/%s/ticket/%s?code=1' %(site_id, request.user.client.cpf, ticket_id), json=payload)

    response = module_request.json()

    return JsonResponse(response)
