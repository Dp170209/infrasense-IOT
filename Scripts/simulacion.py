import requests
import time
from datetime import datetime, timedelta
import numpy as np

url = "http://localhost/infrasense-IOT/Scripts/insertar_datos.php"

# Parámetros de simulación
inicio = datetime.now()
n_galgas = 5
intervalo = timedelta(seconds=2)  # Tiempo entre datos
peso_auto = 500
peso_camion = 900
duracion_subida = 15
duracion_bajada = 5
n_datos_curva = duracion_subida + duracion_bajada  # Total de datos para una curva


def curva_galga(duracion_subida, duracion_bajada, peso_max):
    """Genera una curva de peso simulada para una galga."""
    pesos = []
    for t in range(duracion_subida + duracion_bajada):
        if t < duracion_subida:
            peso = (1 - np.cos(np.pi * t / duracion_subida)) * (peso_max / 2)
        else:
            peso = peso_max * np.exp(-(t - duracion_subida) / (duracion_bajada / 5))
        pesos.append(peso)
    return pesos


def enviar_datos_simulados(tipo_vehiculo, peso_max, id_puente):
    tiempo_actual = inicio  # Tiempo inicial para la primera galga
    if id_puente == 4:  # Si el ID del puente es 4, solo simulamos una galga
        galgas = [25]
    else:  # Para otros casos, simulamos todas las galgas
        galgas = range(2, 7)
    
    for galga in galgas:
        print(f"Iniciando simulación y envío de datos para Galga {galga} ({tipo_vehiculo}, Puente {id_puente})")
        
        pesos_curva = curva_galga(duracion_subida, duracion_bajada, peso_max)
        
        for i, peso in enumerate(pesos_curva):
            fecha_hora = tiempo_actual + i * intervalo
            data = {
                "idGalga": galga,
                "Peso": round(peso, 3),
                "IoThing": f"ESP32-{galga}",
                "Fecha": fecha_hora.strftime("%Y-%m-%d %H:%M:%S"),
                "idPuente": id_puente  # Nuevo campo para el ID del puente
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
        
        tiempo_actual = tiempo_actual + len(pesos_curva) * intervalo
        print(f"Finalizó Galga {galga} a las {tiempo_actual.strftime('%Y-%m-%d %H:%M:%S')}.\n")


if __name__ == "__main__":
    while True:
        print("\nMenú Principal")
        print("1. Seleccionar Puente")
        print("2. Salir")
        opcion_principal = input("Seleccione una opción: ")
        
        if opcion_principal == "1":
            print("\nSeleccione el Puente")
            print("1. Puente Trillizos")
            print("2. Puente de las Americas")
            opcion_puente = input("Seleccione un Puente: ")
            
            if opcion_puente == "1":
                id_puente = 2
            elif opcion_puente == "2":
                id_puente = 4
            else:
                print("Opción no válida. Intente de nuevo.")
                continue
            
            while True:
                print("\nSimulación de Pesos")
                print("1. Simular paso de Auto")
                print("2. Simular paso de Camión")
                print("3. Volver al Menú Principal")
                opcion_simulacion = input("Seleccione una opción: ")
                
                if opcion_simulacion == "1":
                    print("Simulando paso de un auto...")
                    enviar_datos_simulados("Auto", peso_auto, id_puente)
                elif opcion_simulacion == "2":
                    print("Simulando paso de un camión...")
                    enviar_datos_simulados("Camión", peso_camion, id_puente)
                elif opcion_simulacion == "3":
                    print("Volviendo al Menú Principal.")
                    break
                else:
                    print("Opción no válida. Intente de nuevo.")
        elif opcion_principal == "2":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
