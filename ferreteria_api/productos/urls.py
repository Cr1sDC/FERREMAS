from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductoViewSet
from .views import index, vista_productos, detalle_producto, ver_carrito, pagar,crear_producto, editar_producto, eliminar_producto
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
    path('usuarios/', include('usuarios.urls')),
    path('crear/', crear_producto, name='crear_producto'),
    path('editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),

]