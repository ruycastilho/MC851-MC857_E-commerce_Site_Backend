from decimal import Decimal
from django.conf import settings

import requests
import json

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        self.idempresa = '1033'
        self.api_key = 'Bearer daeaffa89950427c269d19d54c3f8e2409d5b6e0c5134f20facc797ca62d868f'
        self.headers = {'Authorization': self.api_key, 'Content-Type': 'application/json'}
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
     
    def add_product(self, product_id, quantity, price, weight, lenght, width, height, name, description, url, category):
        if product_id not in self.cart:
            self.cart[product_id] = {'id': product_id, 'quantity': quantity, 'price': price, 'peso': weight, 'comprimento': lenght, 'largura': width, 'altura': height, 'nome': name, 'descricao': description, 'url': url, 'category':category}
        self.save_session()

    def update_product(self, product_id, quantity):
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
        self.save_session()
 
    def save_session(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear_session(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def clear_cart_on_fail(self):
        for product_id in self.cart:
            query_id = self.cart[product_id]['id']
            query_quantity = self.cart[product_id]['quantity']
            payload = {'idempresa': self.idempresa, 'idproduto': query_id, 'quantidade': query_quantity}
            response = requests.post('http://produtos.vitainformatica.com/api/movimento_estoque/estornar', json=payload, headers=self.headers)
        self.clear_session()

    def get_product_quantity(self, product_id):
        if product_id in self.cart:
            return self.cart[product_id]['quantity']
 
    def remove_product(self, product_id):
        quantity = 0
        if product_id in self.cart:
            quantity=self.cart[product_id]['quantity']
            del self.cart[product_id]
            self.save_session()
            return quantity
 
    # Retorna o valor total dos itens do carrinho
    def get_cart_price(self):
        cart_itens  = {}
        cart_value = 0;
        for product_id in self.cart:
            cart_itens[product_id] = self.cart[product_id]
        for _, dici in cart_itens.items():
            cart_value += float(dici['price']) * float(dici['quantity'])
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
 
    # Preco total, frete e produtos
    def get_total_price(self, CEP, tipoEntrega):
        frete = self.get_frete_price(CEP, tipoEntrega)
        products = self.get_cart_price()
        total = float(frete['preco_frete']) + float(products['preco_carrinho'])
        return {'preco_total': total}

    # Retornar os itens do carrinho para que a compra prossiga
    def get_cart_itens(self):
        cart_itens = []
        for product_id in self.cart:
            cart_itens.append(self.cart[product_id])
        return cart_itens