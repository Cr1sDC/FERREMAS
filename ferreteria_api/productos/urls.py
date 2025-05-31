from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet
from .views import registro_usuario, login_usuario, logout_usuario
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registro/', registro_usuario, name='registro'),
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),
]