import requests
import json
from django.http import HttpResponse, HttpRequest, JsonResponse

# Permitir requisoces do Postman
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user

from ..cart.cart import Cart
from ..website.models import Client, Order
from time import gmtime, strftime

from random import randrange

base_url = 'https://payment-server-mc851.herokuapp.com'
logistica_url = 'https://hidden-basin-50728.herokuapp.com/'
logistica_api_key = '3b8e8f59-6425-5b97-acc5-6fda92b7ada0'
cepOrigem = "13083-852"

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

# Retorno do codigo de rastreio para o produto
@csrf_exempt
def get_track_id(requisition):
    body = format_json(requisition)
    payload = {
        "idProduto": body['idProduto'],
        "tipoEntrega": body['tipoEntrega'],
        "cepOrigem": cepOrigem,
        "cepDestino": body['cepDestino'],
        "peso": body['peso'],
        "tipoPacote": "Caixa",
        "altura": body['altura'],
        "largura": body['largura'],
        "comprimento": body['comprimento'],
        "apiKey": logistica_api_key
    }
    response = requests.post('https://hidden-basin-50728.herokuapp.com/cadastrarentrega', json=payload).json()
    return django_message("Codigo de rastreio", response['status'], response['codigoRastreio'])

# Retorna o valor total do carrinho + frete
# Hardcoded para sempre ser PAC por enquanto
@csrf_exempt
def get_total_value(requisition):
    cart = Cart(requisition)
    payload = json.loads(requisition.body)
    # content = cart.get_total_price(payload['CEP'], payload['tipoEntrega'])
    content = cart.get_total_price(payload['CEP'], 'PAC')
    return django_message("Mostrando preco total", 200, content)

# Pagamento via cartao de credito
# POST com informacoes no body
# {
#     "clientCardName": "",
#     "cpf": "18845601056",
#     "cardNumber": "7410852096307410",
#     "month":"02",
#     "year": "2020",
#     "securityCode":"190",
#     "value": "1000.00",
#     "instalments": "12",
#     "CEP": "13083-852",
#     "tipoEntrega": "PAC"
# }
@csrf_exempt
def pay_by_credit_card(request):
    cart = Cart(request)
    cart_itens = (cart.get_cart_itens())
    url = '/payments/creditCard'
    payload = json.loads(request.body)
    to_pay = json.loads(get_total_value(request).content)
    payload['value'] = to_pay['content']['preco_total']

    user = get_user(request)
    client = user.client
    django_return = None
    if(client.credit == Client.VALID_CREDIT):
        module_request = requests.post(base_url + url, json=payload)
        # zerar carrinho sem recolocar no estoque
        # criar order
        order = Order.objects.create(       order_id=int(str(randrange(0, 999))+strftime('%Y%m%d%H%M%S', gmtime())), 
                                            products=cart_itens, 
                                            order_status=Order.SUCCESS, 
                                            user=client, 
                                            date_of_order=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            date_of_payment=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            price=payload['value'], 
                                            type_of_payment=Order.CREDIT, 
                                            payment_status=Order.ACCEPTED, 
                                            delivery_address="", 
                                            delivery_code=payload['CEP'], 
                                            delivery_status=Order.PENDING,
                                            address=payload['CEP'])
        django_return = django_message("Ok", "200", content=None)
        # cart.clear_session()
    else:
        # zerar carrinho, recolocar no estoque
        # criar order para mostrar o porque falhou
        order = Order.objects.create(       order_id=int(str(randrange(0, 999))+strftime('%Y%m%d%H%M%S', gmtime())), 
                                            products=cart_itens, 
                                            order_status=Order.FAILED_DUE_TO_CREDIT, 
                                            user=client, 
                                            date_of_order=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            date_of_payment=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            price=payload['value'], 
                                            type_of_payment=Order.CREDIT, 
                                            payment_status=Order.UNPAYED, 
                                            delivery_address="", 
                                            delivery_code=payload['CEP'], 
                                            delivery_status=Order.PENDING,
                                            address=payload['CEP'])
        django_return = django_message("Error", "404", content=None)
        # cart.clear_cart()

    # response = module_request.json()

    # if response['result'] == "AUTHORIZED":
    #     return HttpResponse("Hello, world. You're at the polls index.")
  
    # else :
    #     return JsonResponse(response)

    # return JsonResponse(response)
    return django_return

# def installments(request):
#     url = '/payments/creditCard/installments'
#     payload = json.loads(request.body)

#     module_request = requests.post(base_url + url, json=payload)

#     response = module_request.json()

#     return JsonResponse(response)

# Pagar com boleto
# POST com informacoes no body
# {
# "clientName":"FULANO B SILVA",
# "cpf":"18845601056",
# "address":"",
# "CEP":"13083852",
# "value":"120.00",
# "tipoEntrega" : "PAC"
# }
@csrf_exempt
def pay_by_slip(request):
    cart = Cart(request)
    cart_itens = (cart.get_cart_itens()).pop()
    url = '/payments/bankTicket'
    payload = json.loads(request.body)
    to_pay = json.loads(get_total_value(request).content)
    payload['value'] = to_pay['content']['preco_total']
    payload['cep'] = payload['CEP']
    del payload['CEP']

    user = get_user(request)
    client = user.client
    django_return = None    
    if(client.credit == Client.INVALID_CREDIT):
        module_request = requests.post(base_url + url, json=payload)
        # zerar carrinho
        # criar order
        order = Order.objects.create(order_id=int(str(randrange(0, 999))+strftime('%Y%m%d%H%M%S', gmtime())), 
                                            products={str(cart_itens)}, 
                                            order_status=Order.SUCCESS, 
                                            user=client, 
                                            date_of_order=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            date_of_payment=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            price=payload['value'], 
                                            type_of_payment=Order.CREDIT, 
                                            payment_status=Order.ACCEPTED, 
                                            delivery_address="", 
                                            delivery_code=payload['cep'], 
                                            delivery_status=Order.PENDING)     
        django_return = django_message("Ok", "200", content=None)    
        # cart.clear_session()
    else:
        # zerar carrinho
        # criar order para mostrar o porque falhou
        order = Order.objects.create(order_id=int(str(randrange(0, 999))+strftime('%Y%m%d%H%M%S', gmtime())), 
                                            products={str(cart_itens)}, 
                                            order_status=Order.FAILED_DUE_TO_CREDIT, 
                                            user=client, 
                                            date_of_order=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            date_of_payment=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            price=payload['value'], 
                                            type_of_payment=Order.CREDIT, 
                                            payment_status=Order.UNPAYED, 
                                            delivery_address="", 
                                            delivery_code=payload['CEP'], 
                                            delivery_status=Order.PENDING)        
        django_return = django_message("Error", "404", content=None)            
        # cart.clear_cart()
    # response = module_request.json()

    return django_return

# Retorna o numero de parcelas do cartao
# {
#     "value": "1000.01",
#     "cardFlag": "MASTER_CARD"
# }
# @csrf_exempt
# def slip_status(request):
#     url = '/payments/creditCard/installments'
#     parameter = json.loads(request.body)
#     module_request = requests.post(base_url + url, json=parameter)

#     response = module_request.json()

#     return JsonResponse(response)

# def invoice(request):
#     url = '/invoice'
#     payload = json.loads(request.body)

#     module_request = requests.post(base_url + url, json=payload)

#     response = module_request.json()

#     return JsonResponse(response)

# def all_cards(request):
#     url = '/creditCard'

#     module_request = requests.get(base_url + url)

#     response = module_request.json()

#     return JsonResponse(response)

# def card_by_number(request):
#     url = '/creditCard/'
#     payload = json.loads(request.body)

#     module_request = requests.get(base_url + url + str(payload['number']), json=payload)

#     response = module_request.json()

#     return JsonResponse(response)