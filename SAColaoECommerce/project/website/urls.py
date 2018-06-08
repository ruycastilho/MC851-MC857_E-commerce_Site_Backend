from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('clients', views.ClientViewSet)
router.register('products', views.ProductViewSet)
router.register('orders', views.OrderViewSet)
# router.register('create', views.create_user_view)
# router.register('login', view.login_view)
# router.register('logout', view.logout_view)

urlpatterns = [
    path('', include(router.urls)),
    path('createuser/', views.create_user_view, name='create_user_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view')
]
