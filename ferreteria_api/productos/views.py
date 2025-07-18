from rest_framework import viewsets
from .models import Producto,Categoria,Subcategoria,Tienda, REGIONES
from .serializer import ProductoSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random
from rest_framework.permissions import AllowAny,IsAdminUser,SAFE_METHODS
from django.shortcuts import render,redirect, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .forms import ProductoForm
from django.contrib.admin.views.decorators import staff_member_required
from decimal import Decimal, ROUND_HALF_UP

@staff_member_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

@staff_member_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

@staff_member_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.activo = False  # ← Soft delete
    producto.save()
    return redirect('productos')



class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_fields = ['subcategoria']  # Para filtrar desde API


    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]  # Cualquiera puede hacer GET, HEAD, OPTIONS
        return [IsAdminUser()]  # Solo staff puede POST, PUT, DELETE


def index(request):
    productos_queryset = Producto.objects.all()
    productos_list = list(productos_queryset)
    productos_aleatorios = random.sample(productos_list, min(len(productos_list), 4))

    categorias = Categoria.objects.prefetch_related('subcategorias')

    return render(request, 'index.html', {
        'productos': productos_aleatorios,
        'categorias': categorias,
    })


def vista_productos(request):
    subcat_id = request.GET.get('subcategoria')
    productos_queryset = Producto.objects.filter(activo=True)

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
# Vista de detalle del producto con formulario para agregar al carrito
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    error = None

    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))

        if cantidad > producto.stock:
            error = "No hay suficiente stock disponible."
        else:
            carrito = request.session.get('carrito', {})
            if str(producto_id) in carrito:
                carrito[str(producto_id)] += cantidad
            else:
                carrito[str(producto_id)] = cantidad
            request.session['carrito'] = carrito
            return redirect('ver_carrito')

    return render(request, 'detalle_producto.html', {
        'producto': producto,
        'error': error
    })

def pagar(request):
    carrito = request.session.get('carrito', {})
    for prod_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=prod_id)
        producto.stock = max(producto.stock - cantidad, 0)
        producto.save()

    request.session['carrito'] = {}  # Limpia el carrito
    return render(request, 'compra_exitosa.html')


def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})

    producto_id_str = str(producto_id)
    if producto_id_str in carrito:
        del carrito[producto_id_str]
        request.session['carrito'] = carrito

    return redirect('ver_carrito')

# Vista para mostrar el carrito
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    subtotal = Decimal('0')

    for prod_id, cantidad in carrito.items():
        producto = get_object_or_404(Producto, id=prod_id)
        cantidad = int(cantidad)
        precio = producto.precio
        item_subtotal = (precio * cantidad).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        subtotal += item_subtotal
        productos.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': item_subtotal,
        })

    iva = (subtotal * Decimal('0.19')).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    total = subtotal + iva

    return render(request, 'carrito.html', {
        'productos_carrito': productos,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
    })

def tiendas_cercanas(request):
    region_seleccionada = request.GET.get('region')
    tiendas = []

    if region_seleccionada:
        tiendas = Tienda.objects.filter(region=region_seleccionada)

    return render(request, 'tiendas_cercanas.html', {
        'regiones': REGIONES,
        'region_seleccionada': region_seleccionada,
        'tiendas': tiendas
    })
    
    