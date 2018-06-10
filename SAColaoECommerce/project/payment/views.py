import requests
import json
from django.http import HttpResponse, HttpRequest, JsonResponse

# Permitir requisoces do Postman
from django.views.decorators.csrf import csrf_exempt

base_url = 'https://payment-server-mc851.herokuapp.com'
logistica_url = 'https://hidden-basin-50728.herokuapp.com/'
logistica_api_key = '3b8e8f59-6425-5b97-acc5-6fda92b7ada0'
cepOrigem = "13083-852"

def format_json(requisition):
    body_unicode = requisition.body.decode('utf-8')
    return json.loads(body_unicode)

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
    return JsonResponse({
        'message'        : "Codigo de rastreio",
        'status'         : response['status'],
        'content'        : response['codigoRastreio']
        }
    )

@csrf_exempt
def pay_by_credit_card(request):
    url = '/payments/creditCard'
    payload = json.loads(request.body)

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

def pay_by_slip(request):
    url = '/payments/bankTicket'
    payload = json.loads(request.body)

    module_request = requests.post(base_url + url, json=payload)

    response = module_request.json()

    return JsonResponse(response)

def slip_status(request):
    url = '/payments/creditCard/installments'
    parameter = json.loads(request.body)

    module_request = requests.get(base_url + url, params=parameter)

    response = module_request.json()

    return JsonResponse(response)

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