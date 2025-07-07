from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.permissions import SAFE_METHODS
from .serializers import UserSerializer
from rest_framework import viewsets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from usuarios.forms import RegistroForm, LoginForm
from .forms import CrearUsuarioAdminForm

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]  # Cualquiera puede hacer GET, HEAD, OPTIONS
        return [IsAdminUser()]  # Solo staff puede POST, PUT, DELETE

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
# Solo accesible para superadmin
@user_passes_test(lambda u: u.is_superuser)
@login_required
def gestionar_usuarios(request):
    usuarios = User.objects.all().order_by('username')

    if request.method == 'POST':
        form = CrearUsuarioAdminForm(request.POST)
        if form.is_valid():
            nuevo_usuario = form.save(commit=False)
            nuevo_usuario.set_password(form.cleaned_data['password'])
            nuevo_usuario.save()
            return redirect('gestionar_usuarios')
    else:
        form = CrearUsuarioAdminForm()

    return render(request, 'gestionar_usuarios.html', {
        'form': form,
        'usuarios': usuarios
    })

@user_passes_test(lambda u: u.is_superuser)
@login_required
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.user != usuario:  # No te puedes borrar a ti mismo
        usuario.delete()
    return redirect('gestionar_usuarios')

@user_passes_test(lambda u: u.is_superuser)
@login_required
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = CrearUsuarioAdminForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            if 'password' in form.cleaned_data and form.cleaned_data['password']:
                usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            return redirect('gestionar_usuarios')
    else:
        form = CrearUsuarioAdminForm(instance=usuario)

    return render(request, 'editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })