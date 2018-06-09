from django.conf import settings
from . import categories

class Products():
    def __init__(self):
        self.product = product

    def add_product(self, request):
        for prod in request:
            if prod['id'] not in self.product:
                self.product[prod['id']] = {
                    "codigo" : prod['codigo'],
                    "nome" : prod['nome'],
                    "idcategoria" : prod['idcategoria'],
                    "preco" : prod['preco'],
                    "peso" : prod['peso'],
                    "dimensao_a" : prod['dimensao_a'],
                    "dimensao_c" : prod['dimensao_c'],
                    "dimensao_l" :prod['dimensao_l'],
                    "idempresa" : 1033,
                    "imagem_url" : prod['imagem_url'],
                    "campos" : prod['campos']
                }

    