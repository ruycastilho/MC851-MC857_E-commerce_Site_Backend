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
from django.contrib.auth import get_user

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

# Retorno para o front end
def django_message(message, status_code, content=None):
	return JsonResponse({
		'message'        : message,
		'status'         : status_code,
		'content'        : content,
		}
    )


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
    json_data=json.loads(request.body.decode('utf-8'))

    payload={
        'timestamp': strftime('%Y-%m-%dT%H:%M', gmtime()),
        'sender'   : get_user(request).username,
        # 'sender'   : '263.153.130-27',
        'message'  : json_data['message']
    }
    # print(json_data['message'])
    user = get_user(request)
    # if not(request.user.is_authenticated):
    #     print("AQUIIIIIIII")
    
    # print("username " + user.password)
    # print(str(type(strftime('%Y-%m-%d %H:%M:%S', gmtime()))) + " " + str(type(get_user(request).username)) + " "  + str(type(json_data['message'])))
    response = requests.post(base_url + '%s/%s/' %(site_id, get_user(request).client.cpf), json=payload)
    # response = requests.post(base_url + '%s/%s/' %(site_id,'263.153.130-27'), json=payload)

    # print(response.status_code + str(response.content))
    return django_message("Ticket adicionado", response.status_code, str(response.content))

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
    json_data=json.loads(request.body.decode('utf-8'))

    payload={
        'timestamp': strftime('%Y-%m-%dT%H:%M', gmtime()),
        # 'sender'   : get_user(request).username,
        'sender'   : '263.153.130-27',
        'message'  : json_data['message']
    }

    order_id = json_data['order']
    # print(json.dumps(payload))
    response = requests.post(base_url + '%s/%s/compra/%s' %(site_id, get_user(request).client.cpf, order_id), json=payload)
    # response = requests.post(base_url + '%s/%s/compra/%s' %(site_id,'263.153.130-27', order_id), json=payload)


    return django_message("Ticket adicionado", response.status_code, str(response.content))

# Adicionar mensagem a ticket
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/add_message_to_ticket/ (PUT) com body:
# {
# 	'message'  : 'Reclamação',
#	'ticket_id' : '1'
# }
# Devolve sinal 200 em sucesso, 400 em falha e 404 caso ticket não seja encontrado
@csrf_exempt
def add_message_to_ticket(request, ticket_id):
    json_data=json.loads(request.body.decode('utf-8'))

    payload={
        'timestamp': strftime('%Y-%m-%dT%H:%M', gmtime()),
        'sender'   : get_user(request).username,
        # 'sender':  'user',
        'message'  : json_data['message']
    }
    response = requests.put(base_url + '%s/%s/ticket/%s' %(site_id, get_user(request).client.cpf, ticket_id), json=payload)
    # response = requests.put(base_url + '%s/%s/ticket/%s' %(site_id, '263.153.130-27', ticket_id), json=payload)

    return django_message("Mensagem adicionada", response.status_code, str(response.content))

# Receber tickets de um cliente
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/get_all_tickets/ (GET);
# Devolve sinal 200 em sucesso, 400 em falha e 404 caso o site id esteja errado
@csrf_exempt
def get_all_tickets(request):
    response = requests.get(base_url + '%s/%s/' %(site_id, get_user(request).client.cpf))
    # response = requests.get(base_url + '%s/263.153.130-27/' %(site_id))

    dump = json.loads(str(response.content.decode('utf-8')))
    ticket_list = ""

    if (response.status_code == 200):
        ticket_list = dump['ticketsList']

    return django_message("Devolvendo tickets", response.status_code, ticket_list)

# Receber ticket especifico de um cliente
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/get_ticket_by_number/1 (GET);
# Devolve sinal 200 em sucesso, 404 caso não encontre nenhum ticket e 400 caso o site id esteja errado
@csrf_exempt
def get_ticket_by_number(request, ticket_id):
    response = requests.get(base_url + '%s/%s/ticket/%s/' %(site_id, get_user(request).client.cpf, ticket_id))

    dump = json.loads(str(response.content.decode('utf-8')))

    return django_message("Devolvendo ticket por id", response.status_code, dump)


# Receber mensagens ticket especifico de um cliente
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/get_ticket_by_number/1 (GET);
# Devolve sinal 200 em sucesso, 404 caso não encontre nenhum ticket e 400 caso o site id esteja errado
@csrf_exempt
def get_message_by_number(request, ticket_id):
    response = requests.get(base_url + '%s/%s/ticket/%s/' %(site_id, get_user(request).client.cpf, ticket_id))
    # response = requests.get(base_url + '%s/263.153.130-27/ticket/%s/' %(site_id, ticket_id))
    dump = json.loads(str(response.content.decode('utf-8')))

    # print(dump['ticketsList'][0]['messagesList'])

    return django_message("Devolvendo ticket por id", response.status_code, dump['ticketsList'][0]['messagesList'])


# Receber ticket especifico de um cliente por numero de pedido
# Recebe json
# ex de chamada: http://localhost:8000/customer_support/get_ticket_by_order/1 (GET);
# Devolve sinal 200 em sucesso, 404 caso não encontre nenhum ticket e 400 caso o site id esteja errado
@csrf_exempt
def get_ticket_by_order(request, order_id):
    response = requests.get(base_url + '%s/%s/compra/%s/' %(site_id, get_user(request).client.cpf, order_id))

    dump = json.loads(str(response.content.decode('utf-8')))

    return django_message("Devolvendo ticket por compra", response.status_code, dump)

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
    json_data=json.loads(request.body.decode('utf-8'))

    payload={
        'timestamp': strftime('%Y-%m-%dT%H:%M', gmtime()),
        'sender'   : get_user(request).username,
        # 'sender'   : '263.153.130-27',
        'message'  : json_data['message']
    }

    response = requests.delete(base_url + '%s/%s/ticket/%s?code=1' %(site_id, get_user(request).client.cpf, ticket_id), json=payload)
    # response = requests.delete(base_url + '%s/%s/ticket/%s?code=1' %(site_id, '263.153.130-27', ticket_id), json=payload)

    return django_message("Devolvendo ticket por compra", response.status_code, str(response.content))
