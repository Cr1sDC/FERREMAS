from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
router = DefaultRouter()
router.register(r'usuarios', UserViewSet)

from .views import registro_usuario, login_usuario, logout_usuario


urlpatterns = [
    path('registro/', registro_usuario, name='registro'),
    path('login/', login_usuario, name='login'),
    path('logout/', logout_usuario, name='logout'),

]