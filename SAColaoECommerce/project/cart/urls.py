from django.urls import path

from . import views

urlpatterns = [
    path('add_product/', views.add_product, name='add_product'),
    path('update_product/', views.update_product, name='update_product'),
    path('remove_product/', views.remove_product, name='remove_product'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('get_frete_value/', views.get_frete_value, name='get_frete_value'),
    path('get_cart_value/', views.get_cart_value, name='get_cart_value')
]