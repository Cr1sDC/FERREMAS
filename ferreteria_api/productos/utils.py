import requests

def obtener_tipo_cambio_usd_clp():
    url = "https://api.exchangerate.host/latest?base=USD&symbols=CLP"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200 and "rates" in data:
            return data["rates"]["CLP"]
        else:
            return None
    except Exception as e:
        print("Error al obtener tipo de cambio:", e)
        return None