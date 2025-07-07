from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, gestionar_usuarios, eliminar_usuario, editar_usuario
router = DefaultRouter()
router.register(r'usuarios', UserViewSet)

from .views import registro_usuario, login_usuario, logout_usuario


urlpatterns = [
    path('registro/', registro_usuario, name='registro'),
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),
    path('gestionar/', gestionar_usuarios, name='gestionar_usuarios'),
    path('eliminar/<int:user_id>/', eliminar_usuario, name='eliminar_usuario'),
    path('editar/<int:user_id>/', editar_usuario, name='editar_usuario'),

]