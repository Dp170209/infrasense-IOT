import requests
import time
from datetime import datetime, timedelta
import numpy as np

# URL del servidor
url = "http://localhost/infrasense-IOT/Scripts/insertar_datos.php"

# Parámetros de simulación
inicio = datetime.now()
n_galgas = 5
intervalo = timedelta(seconds=2)  # Tiempo entre datos
peso_max = 500
duracion_subida = 15  # Número de datos en la subida
duracion_bajada = 3  # Número de datos en la bajada
n_datos_curva = duracion_subida + duracion_bajada  # Total de datos para una curva

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
    tiempo_actual = inicio  # Tiempo inicial para la primera galga
    for galga in range(2, 7):  # Galgas de 2 a 6
        print(f"Iniciando simulación y envío de datos para Galga {galga}")
        
        pesos_curva = curva_galga(duracion_subida, duracion_bajada, peso_max)
        
        for i, peso in enumerate(pesos_curva):
            fecha_hora = tiempo_actual + i * intervalo
            data = {
                "idGalga": galga,
                "Peso": round(peso, 3),
                "IoThing": f"ESP32-{galga}",
                "Fecha": fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
            }
            headers = {'Content-Type': 'application/json'}
            try:
                response = requests.post(url, json=data, headers=headers)
                print("Datos enviados:", data)
                print("Respuesta del servidor:", response.text)
                response.close()
            except Exception as e:
                print("Error al enviar datos:", e)
            
            time.sleep(intervalo.total_seconds())  # Pausar entre datos
        
        # Actualizar el tiempo para la siguiente galga
        tiempo_actual = tiempo_actual + len(pesos_curva) * intervalo
        print(f"Finalizó Galga {galga} a las {tiempo_actual.strftime('%Y-%m-%d %H:%M:%S')}.\n")

if __name__ == "__main__":
    enviar_datos_simulados()