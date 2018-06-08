from django.conf import settings
from . import categories

class Products():
    def __init__(self):
        self.product = product

    def add_product(self, request):
        for prod in request:
            if prod['id'] not in self.product:
                self.product[prod['id']] = {
                    'name'          : prod['name'],
                    'brand'         : prod['brand'],
                    'description'   : prod['description'],
                    'price'         : prod['price'],
                    'stock'         : prod['stock'],
                    'categoryId'    : prod['categoryId']
                }

    