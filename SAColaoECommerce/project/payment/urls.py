from django.urls import path

from . import views

urlpatterns = [
    path('pay_by_slip/', views.pay_by_slip, name='slip'),
    # path('all_cards/', views.all_cards, name='all_cards'),
    # path('card_by_number/', views.card_by_number, name='card_by_number'),
    path('pay_by_credit_card/', views.pay_by_credit_card, name='credit'),
    # path('slip_status/', views.slip_status, name='slip_status'),
    path('get_track_id/', views.get_track_id, name='get_track_id'),
	path('get_total_value/', views.get_total_value, name='get_total_value')    
    # path('invoice/', views.pay_by_credit_card, name='invoice'),
    # path('installments/', views.installments, name='installments')
]