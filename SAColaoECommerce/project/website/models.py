from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11)
    address = models.CharField(max_length=100, default='')
    email = models.CharField(max_length=100, default='')

    VALID_CREDIT = 'valid'
    INVALID_CREDIT = 'invalid'

    CREDIT_CHOICES = (
        (VALID_CREDIT, 'Crédito Válido'),
        (INVALID_CREDIT, 'Crédito Inválido')
    )

    credit = models.CharField(choices=CREDIT_CHOICES, max_length=100, default=VALID_CREDIT)

    def __str__(self):
        return self.cpf

class Order(models.Model):
    order_id = models.CharField(max_length=50)

    products = PickledObjectField()

    SUCCESS = 'A compra foi um sucesso'
    FAILED_DUE_TO_CREDIT = 'A compra falhou devido a restrições de crédito'

    PAYMENT_CHOICES = (
        (SUCCESS, 'Sucesso'),
        (FAILED_DUE_TO_CREDIT, 'Falha devido a restrições de crédito')
    )
    order_status = models.CharField(choices=PAYMENT_CHOICES, default=SUCCESS, max_length=50)
    
    user = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
    )
 
    date_of_order = models.DateTimeField()
    date_of_payment = models.DateTimeField()
    price = models.DecimalField(decimal_places=2, max_digits=1000)
 
    CREDIT = 'Cartão de Crédito'
    SLIP = 'Boleto Bancário'
    PAYMENT_CHOICES = (
        (CREDIT, 'Cartão de Crédito'),
        (SLIP, 'Boleto Bancário')
    )
    type_of_payment = models.CharField(choices=PAYMENT_CHOICES, default=CREDIT, max_length=50)
    
    ACCEPTED = 'Pagamento Realizado'
    PENDING = 'Pagamento Pendente'
    UNPAYED = 'Pagamento Não Realizado'
    STATUS_CHOICES = (
        (ACCEPTED, 'Pagamento Realizado'),
        (PENDING, 'Pagamento Pendente'),
        (UNPAYED, 'Pagamento Não Realizado')
    )
    payment_status = models.CharField(choices=STATUS_CHOICES, default=ACCEPTED, max_length=50)
    
    delivery_address = models.CharField(max_length=100, default='')
    delivery_code = models.CharField(max_length=50, default='')

    DELIVERED = 'Entrega Realizada'
    PENDING = 'Entrega Pendente'
    RETURNED = 'Entrega Devolvida'
    DELIVERY_CHOICES = (
        (DELIVERED, 'Entrega Realizada'),
        (PENDING, 'Entrega Pendente'),
        (RETURNED, 'Entrega Devolvida'),

    )
    delivery_status = models.CharField(choices=DELIVERY_CHOICES, default=DELIVERED, max_length=50)
    

    def __str__(self):
        return self.order_id

# class Product(models.Model):

#     name = models.CharField(max_length=50)
#     brand = models.CharField(max_length=50)
#     description = models.CharField(max_length=200)
#     price = models.DecimalField(decimal_places=2, max_digits=2)
#     amount = models.IntegerField()
#     category = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name