from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet
from .views import index, vista_productos, detalle_producto, ver_carrito, pagar
from . import views
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', index, name='inicio'),
    path('productos/', vista_productos, name='productos'),
    path('productos/', views.vista_productos, name='vista_productos'),
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('pagar/', pagar, name='pagar'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('tiendas/', views.tiendas_cercanas, name='tiendas_cercanas'),

]