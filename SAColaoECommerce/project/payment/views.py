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
def get_track_id(cart_itens, tipoEntrega, cepDestino):
    body = cart_itens[0]
    payload = {
        "idProduto": int(body['id']),
        "tipoEntrega": str(tipoEntrega),
        "cepOrigem": str(cepOrigem),
        "cepDestino": "13348-863",
        # "peso": float(body['peso']),
        "peso": 104,        
        "tipoPacote": "Caixa",
        "altura": int(body['altura']),
        "largura": int(body['largura']),
        "comprimento": int(body['comprimento']),
        "apiKey": str(logistica_api_key)
    }
    print(payload)
    response = requests.post('https://hidden-basin-50728.herokuapp.com/cadastrarentrega', json=payload).json()
    return response['codigoRastreio']

# Validade CEP
def validade_cep(cep):
    h = {'x-api-key': '4f5bc7c5-ba73-4d4c-8e49-8d466270865e'}
    response = requests.get("http://node.thiagoelg.com/paises/br/cep/%s" %cep, headers=h)
    django_return = None        
    if response.status_code == requests.codes.ok:
        return 0
    return -1

# Retorna o valor total do carrinho + frete
# Hardcoded para sempre ser PAC por enquanto
@csrf_exempt
def get_total_value(requisition):
    cart = Cart(requisition)
    payload = json.loads(requisition.body.decode('utf-8'))
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
    payload = json.loads(request.body.decode('utf-8'))
    # print(json.loads(get_total_value(request).content.decode('utf-8')))
    if(validade_cep(payload['CEP']) != 0):
        print("invalid cep")
        return django_message("CEP Invalido", 400, None)
    to_pay = json.loads(get_total_value(request).content.decode('utf-8'))
    payload['value'] = to_pay['content']['preco_total']
    delivery_estimated_time = to_pay['content']['tempo_entrega']
    track_id = get_track_id(cart_itens, payload['tipoEntrega'], payload['CEP'])
    print(track_id)

    # cart_itens = json.dumps(json.loads(cart_itens).decode('utf-8'))
    user = get_user(request)
    client = user.client
    django_return = None
    if(client.credit == Client.VALID_CREDIT):
        module_request = requests.post(base_url + url, json=payload)
        # zerar carrinho sem recolocar no estoque
        # criar order
        order = Order.objects.create(       order_id=int(str(randrange(0, 999))+strftime('%Y%m%d%H%M%S', gmtime())), 
                                            # track_id=track_id,
                                            # slip_code="",                                      
                                            products=cart_itens, 
                                            order_status=Order.SUCCESS, 
                                            user=client, 
                                            date_of_order=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            date_of_delivery=delivery_estimated_time,
                                            date_of_payment=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            price=payload['value'], 
                                            type_of_payment=Order.CREDIT, 
                                            payment_status=Order.ACCEPTED, 
                                            delivery_address="", 
                                            delivery_code=payload['CEP'], 
                                            delivery_status=Order.PENDING,
                                            address=payload['CEP'])
        django_return = django_message("Ok", 200, content=None)
        cart.clear_session()
    else:
        # zerar carrinho, recolocar no estoque
        # criar order para mostrar o porque falhou
        order = Order.objects.create(       order_id=int(str(randrange(0, 999))+strftime('%Y%m%d%H%M%S', gmtime())), 
                                            # track_id=track_id,
                                            # slip_code="",
                                            products=cart_itens, 
                                            order_status=Order.FAILED_DUE_TO_CREDIT, 
                                            user=client, 
                                            date_of_order=strftime('%Y-%m-%d %H:%M:%S', gmtime()),                                             
                                            date_of_delivery=delivery_estimated_time, 
                                            date_of_payment=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            price=payload['value'], 
                                            type_of_payment=Order.CREDIT, 
                                            payment_status=Order.UNPAYED, 
                                            delivery_address="", 
                                            delivery_code=payload['CEP'], 
                                            delivery_status=Order.PENDING,
                                            address=payload['CEP'])
        django_return = django_message("Error", 404, content=None)
        cart.clear_cart_on_fail()

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
    cart_itens = (cart.get_cart_itens())
    url = '/payments/bankTicket'
    payload = json.loads(request.body)
    if(validade_cep(payload['CEP']) != 0):
        return django_message("CEP Invalido", 400, None)    
    to_pay = json.loads(get_total_value(request).content)
    tipoEntrega = payload['tipoEntrega']
    payload['value'] = str(to_pay['content']['preco_total'])
    payload['cep'] = payload['CEP']
    payload['clientName'] = "sindo"
    del payload['CEP']
    del payload['tipoEntrega']

    delivery_estimated_time = to_pay['content']['tempo_entrega']
    track_id = get_track_id(cart_itens, tipoEntrega, payload['cep'])
    # print(track_id)

    user = get_user(request)
    client = user.client
    django_return = None    
    if(client.credit == Client.VALID_CREDIT):
        module_request = requests.post(base_url + url, json=payload)
        response = module_request.json()
        # zerar carrinho
        # criar order
        order = Order.objects.create(order_id=int(str(randrange(0, 999))+strftime('%Y%m%d%H%M%S', gmtime())), 
                                            # track_id=track_id,
                                            # slip_code=response['code'],
                                            products={str(cart_itens)}, 
                                            order_status=Order.SUCCESS, 
                                            user=client,
                                            date_of_order=strftime('%Y-%m-%d %H:%M:%S', gmtime()),                                              
                                            date_of_delivery=delivery_estimated_time, 
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
                                            # track_id=track_id,
                                            # slip_code="",
                                            products={str(cart_itens)}, 
                                            order_status=Order.FAILED_DUE_TO_CREDIT, 
                                            user=client, 
                                            date_of_order=strftime('%Y-%m-%d %H:%M:%S', gmtime()),                                             
                                            date_of_delivery=delivery_estimated_time, 
                                            date_of_payment=strftime('%Y-%m-%d %H:%M:%S', gmtime()), 
                                            price=payload['value'], 
                                            type_of_payment=Order.CREDIT, 
                                            payment_status=Order.UNPAYED, 
                                            delivery_address="", 
                                            delivery_code=payload['cep'], 
                                            delivery_status=Order.PENDING)        
        django_return = django_message("Error", "404", content=None)            
        cart.clear_cart_on_fail()

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