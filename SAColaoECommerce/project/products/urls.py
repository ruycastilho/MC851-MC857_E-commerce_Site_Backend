from django.urls import path

from . import views

urlpatterns = [
    path('search_products_by_name/', views.search_products_by_name, name='search_products_by_name'),
    path('search_products_by_category/', views.search_products_by_category, name='search_products_by_category'),
    path('reserve/', views.reserve_product, name='reserve_product'),
    path('release/', views.release_product, name='release_product'),
    path('get_categories/', views.get_categories, name='get_categories'),
    path('get_products/', views.get_products, name='get_products'),
    path('add_product/', views.add_product, name='add_product'),
    path('add_category/', views.add_category, name='add_category')
]