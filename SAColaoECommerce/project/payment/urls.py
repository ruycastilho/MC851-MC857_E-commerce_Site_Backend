from django.urls import path

from . import views

urlpatterns = [
    path('pay_by_slip/', views.pay_by_slip, name='slip'),
    path('all_cards/', views.all_cards, name='all_cards'),
    path('card_by_number/', views.card_by_number, name='card_by_number'),
    path('pay_by_credit_card/', views.pay_by_credit_card, name='credit'),
    path('slip_status/', views.pay_by_credit_card, name='slip_status'),
    path('invoice/', views.pay_by_credit_card, name='invoice'),
    path('installments/', views.installments, name='installments')

]