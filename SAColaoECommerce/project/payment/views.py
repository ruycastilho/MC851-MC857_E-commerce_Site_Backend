import requests
import json
from django.http import HttpResponse, HttpRequest, JsonResponse

# Permitir requisoces do Postman
from django.views.decorators.csrf import csrf_exempt

from ..cart.cart import Cart

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
    url = '/payments/creditCard'
    payload = json.loads(request.body)
    to_pay = json.loads(get_total_value(request).content)
    payload['value'] = to_pay['content']['preco_total']
    module_request = requests.post(base_url + url, json=payload)

    response = module_request.json()

    # if response['result'] == "AUTHORIZED":
    #     return HttpResponse("Hello, world. You're at the polls index.")
  
    # else :
    #     return JsonResponse(response)

    return JsonResponse(response)

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
    url = '/payments/bankTicket'
    payload = json.loads(request.body)
    to_pay = json.loads(get_total_value(request).content)    
    payload['value'] = to_pay['content']['preco_total']
    payload['cep'] = payload['CEP']
    del payload['CEP']

    module_request = requests.post(base_url + url, json=payload)

    response = module_request.json()

    return JsonResponse(response)

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