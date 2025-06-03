from rest_framework import serializers
from .models import Producto
import requests
from functools import lru_cache
from decimal import Decimal

class ProductoSerializer(serializers.ModelSerializer):
    precio_clp = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'subcategoria', 'imagen', 'precio_clp']

    def get_precio_clp(self, obj):
        tasa = self.get_tasa_usd_to_clp()
        if tasa:
            return round(obj.precio * Decimal(tasa), 0)
        return None  

    @lru_cache(maxsize=1)
    def get_tasa_usd_to_clp(self):
        try:
            url = "https://v6.exchangerate-api.com/v6/a57295f4be068fee685ecb2d/latest/USD"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data['conversion_rates']['CLP']
        except Exception as e:
            print(f"Error al obtener tasa de cambio: {e}")
        return None
