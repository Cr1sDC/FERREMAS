# productos/models.py

from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='subcategorias')

    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, related_name='productos')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
REGIONES = [
    ("Arica y Parinacota", "Arica y Parinacota"),
    ("Tarapacá", "Tarapacá"),
    ("Antofagasta", "Antofagasta"),
    ("Atacama", "Atacama"),
    ("Coquimbo", "Coquimbo"),
    ("Valparaíso", "Valparaíso"),
    ("Metropolitana de Santiago", "Metropolitana de Santiago"),
    ("Libertador General Bernardo O'Higgins", "Libertador General Bernardo O'Higgins"),
    ("Maule", "Maule"),
    ("Ñuble", "Ñuble"),
    ("Biobío", "Biobío"),
    ("La Araucanía", "La Araucanía"),
    ("Los Ríos", "Los Ríos"),
    ("Los Lagos", "Los Lagos"),
    ("Aysén del General Carlos Ibáñez del Campo", "Aysén del General Carlos Ibáñez del Campo"),
    ("Magallanes y de la Antártica Chilena", "Magallanes y de la Antártica Chilena"),
]

class Tienda(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    region = models.CharField(max_length=100, choices=REGIONES)

    def __str__(self):
        return f"{self.nombre} - {self.region}"
