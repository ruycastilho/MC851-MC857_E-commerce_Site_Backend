from django.urls import path

from . import views

urlpatterns = [
    path('add_ticket/', views.add_ticket, name='add_ticket'),
    path('add_ticket_order/', views.add_ticket_order, name='add_ticket_order'),
    path('add_message_to_ticket/<str:ticket_id>', views.add_message_to_ticket, name='add_message_to_ticket'),
    path('get_all_tickets/', views.get_all_tickets, name='get_all_tickets'),
    path('get_ticket_by_number/<str:ticket_id>', views.get_ticket_by_number, name='get_ticket_by_number'),
    path('get_ticket_by_order/<str:order_id>', views.get_ticket_by_order, name='get_ticket_by_order'),
    path('close_ticket/<str:ticket_id>', views.close_ticket, name='close_ticket'),

]