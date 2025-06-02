from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Producto
from .serializer import ProductoSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]  # 👈 Permite acceso sin autenticación
