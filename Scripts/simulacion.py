import requests
import time
from datetime import datetime, timedelta
import numpy as np

# URL del servidor
url = "http://localhost/infrasense-IOT/Scripts/insertar_datos.php"

# Parámetros de simulación
inicio = datetime.now()
n_galgas = 5
intervalo = timedelta(seconds=2)
peso_max = 500
duracion_subida = 15
duracion_bajada = 3
n_datos_curva = duracion_subida + duracion_bajada
desplazamiento = n_datos_curva // 2

def curva_galga(duracion_subida, duracion_bajada, peso_max):
    pesos = []
    for t in range(duracion_subida + duracion_bajada):
        if t < duracion_subida:
            peso = (1 - np.cos(np.pi * t / duracion_subida)) * (peso_max / 2)
        else:
            peso = peso_max * np.exp(-(t - duracion_subida) / (duracion_bajada / 5))
        pesos.append(peso)
    return pesos

def enviar_datos_simulados():
    for galga in range(2, 7):  # Galgas de 2 a 6
        print(f"Iniciando simulación y envío de datos para Galga {galga}")
        
        pesos_curva = curva_galga(duracion_subida, duracion_bajada, peso_max)
        inicio_galga = inicio + (galga - 2) * desplazamiento * intervalo
        
        for i, peso in enumerate(pesos_curva):
            fecha_hora = inicio_galga + i * intervalo
            data = {
                "idGalga": galga,
                "Peso": round(peso, 3),  # Usar "Peso" en mayúscula
                "IoThing": f"ESP32-{galga}",  # Usar "IoThing" en lugar de "ioThing"
                "Fecha": fecha_hora.strftime("%Y-%m-%d %H:%M:%S")  # Usar "Fecha" en lugar de "fecha_hora"
            }
            headers = {'Content-Type': 'application/json'}
            try:
                response = requests.post(url, json=data, headers=headers)
                print("Datos enviados:", data)
                print("Respuesta del servidor:", response.text)
                response.close()
            except Exception as e:
                print("Error al enviar datos:", e)
            
            time.sleep(intervalo.total_seconds())

if __name__ == "__main__":
    enviar_datos_simulados()
