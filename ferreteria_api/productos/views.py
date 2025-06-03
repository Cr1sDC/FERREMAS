from rest_framework import viewsets
from .models import Producto,Categoria,Subcategoria
from .serializer import ProductoSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from rest_framework.permissions import AllowAny,IsAdminUser,SAFE_METHODS

from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_fields = ['subcategoria']  # Para filtrar desde API


    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]  # Cualquiera puede hacer GET, HEAD, OPTIONS
        return [IsAdminUser()]  # Solo staff puede POST, PUT, DELETE



def index(request):
    productos = list(Producto.objects.all())
    productos_aleatorios = random.sample(productos, min(len(productos), 4))
    return render(request, 'index.html', {'productos_aleatorios': productos_aleatorios})


def vista_productos(request):
    subcat_id = request.GET.get('subcategoria')
    productos_queryset = Producto.objects.all()

    if subcat_id:
        productos_queryset = productos_queryset.filter(subcategoria_id=subcat_id)

    productos_list = list(productos_queryset)
    productos_aleatorios = random.sample(productos_list, min(len(productos_list), 12))

    categorias = Categoria.objects.prefetch_related('subcategorias')

    return render(request, 'productos.html', {
        'productos': productos_aleatorios,
        'categorias': categorias,
        'subcat_id': int(subcat_id) if subcat_id else None
    })
