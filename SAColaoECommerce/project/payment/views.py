import requests
import json
from django.http import HttpResponse, HttpRequest, JsonResponse

base_url = 'https://payment-server-mc851.herokuapp.com'


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

def installments(request):
    url = '/payments/creditCard/installments'
    payload = json.loads(request.body)

    module_request = requests.post(base_url + url, json=payload)

    response = module_request.json()

    return JsonResponse(response)

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

def invoice(request):
    url = '/invoice'
    payload = json.loads(request.body)

    module_request = requests.post(base_url + url, json=payload)

    response = module_request.json()

    return JsonResponse(response)

def all_cards(request):
    url = '/creditCard'

    module_request = requests.get(base_url + url)

    response = module_request.json()

    return JsonResponse(response)

def card_by_number(request):
    url = '/creditCard/'
    payload = json.loads(request.body)

    module_request = requests.get(base_url + url + str(payload['number']), json=payload)

    response = module_request.json()

    return JsonResponse(response)