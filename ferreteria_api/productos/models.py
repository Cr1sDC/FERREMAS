from django.db import models

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    tipo = models.CharField(max_length=50, default='General')
    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    

