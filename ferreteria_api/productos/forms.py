from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar = cleaned_data.get("confirmar_password")
        if password != confirmar:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
