from django.urls import path, include
from rest_framework.routers import DefaultRouter
from productos.views import ProductoViewSet
from usuarios.views import UserViewSet

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
