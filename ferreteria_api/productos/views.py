from rest_framework import viewsets
from .models import Producto
from .serializer import ProductoSerializer
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from .forms import RegistroForm, LoginForm
from rest_framework.permissions import AllowAny

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]  # 👈 Permite acceso sin autenticación

def index(request):
    return render(request, 'index.html')

def vista_productos(request):
    return render(request, 'productos.html')

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def login_usuario(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('inicio')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('inicio')

def azar(request):
    productos = list(Producto.objects.all())
    productos_aleatorios = random.sample(productos, min(len(productos), 4))  # 4 productos máximo
    return render(request, 'index.html', {'productos_aleatorios': productos_aleatorios})