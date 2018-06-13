from django.urls import path

from . import views

urlpatterns = [
    path('get_products/', views.get_products, name='get_products'),
    path('get_products_by_category/<str:token>', views.get_products_by_category, name='get_products_by_category'),
    path('get_products_by_name/<str:token>', views.get_products_by_name, name='get_products_by_name'),
    path('get_products_by_name_or_category/<str:cat>/<str:name>', views.get_products_by_name_or_category, name='get_products_by_name_or_category'),
    path('get_stock_id/<str:product_id>', views.get_stock, name='get_stock_id')
]

