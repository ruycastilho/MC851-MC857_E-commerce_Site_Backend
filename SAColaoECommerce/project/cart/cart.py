from decimal import Decimal
from django.conf import settings

import requests
import json

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
     
    def add_product(self, product_id, quantity, price, weight, lenght, width, height):
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity, 'price': price, 'peso': weight, 'comprimento': lenght, 'largura': width, 'altura': height}
        self.save_session()

    def update_product(self, product_id, quantity):
        if product_id in self.cart:
            self.cart[product_id] = {'quantity': quantity}
        self.save_session()
 
    def save_session(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear_session(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
 
    def remove_product(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save_session()
 
    # Retorna o valor total dos itens do carrinho
    def get_cart_price(self):
        cart_itens  = {}
        cart_value = 0;
        for product_id in self.cart:
            cart_itens[product_id] = self.cart[product_id]
        for _, dici in cart_itens.items():
            for key, val in dici.items():
                if(key == 'price'):
                    cart_value += float(val)
        return {'preco_carrinho': cart_value}

    def get_frete_price(self, CEP, tipoEntrega):
        cart_itens  = {}
        frete_total_value = 0;
        delivery_days = []
        payload = {'tipoEntrega': tipoEntrega, 'cepOrigem': '13091904', 'cepDestino': CEP, 'tipoPacote': 'Caixa'}
        for product_id in self.cart:
            cart_itens[product_id] = self.cart[product_id]
        for _, dici in cart_itens.items():
            for key, val in dici.items():
                if(key == 'peso' or key == 'comprimento' or key == 'altura' or key == 'largura'):
                    payload[key] = str(val)
            response = requests.get('https://hidden-basin-50728.herokuapp.com/calculafrete', params=payload)
            json_result=json.loads(response.text)
            frete_total_value += float(json_result['preco'])/100
            delivery_days.append(int(json_result['prazo']))
        return {'preco_frete': frete_total_value, 'tempo_entrega': str(max(delivery_days))}
 
    # Retornar os itens do carrinho para que a compra prossiga
    def get_cart_itens(self):
        cart_itens = {}
        for product_id in self.cart:
            cart_itens[product_id] = self.cart[product_id]
        return self.cart