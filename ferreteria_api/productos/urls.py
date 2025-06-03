from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet
from .views import index, vista_productos, registro_usuario, login_usuario, logout_usuario
from .views import registro_usuario, login_usuario, logout_usuario
from . import views
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', index, name='inicio'),
    path('productos/', vista_productos, name='productos'),
    path('productos/', views.vista_productos, name='vista_productos'),
    path('registro/', registro_usuario, name='registro'),
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),
]