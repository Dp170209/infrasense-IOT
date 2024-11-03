import sys
import os
import network
import ubinascii
import machine
from machine import Pin
import urequests as requests
import ujson
import time
import utime
import math
from secrets import secrets  # Archivo separado para las credenciales Wi-Fi
from Wifi_lib import wifi_init  # Librerías externas para iniciar Wi-Fi

# Inicializar la conexión Wi-Fi
wifi_init()

# Detectar el tipo de tarjeta
class Board:
    class BoardType:
        PICO_W = 'Raspberry Pi Pico W'
        ESP32 = 'ESP32'
        UNKNOWN = 'Unknown'

    def __init__(self):
        self.type = self.detect_board_type()

    def detect_board_type(self):
        sysname = os.uname().sysname.lower()
        machine_name = os.uname().machine.lower()
        if sysname == 'rp2' and 'pico w' in machine_name:
            return self.BoardType.PICO_W
        elif sysname == 'esp32' and 'esp32' in machine_name:
            return self.BoardType.ESP32
        else:
            return self.BoardType.UNKNOWN

# Detectar tipo de placa
BOARD_TYPE = Board().type
print("Tarjeta Detectada:", BOARD_TYPE)

# Configuración inicial
NTaylor = 1
angle = 0  # Ángulo en grados
url = "http://192.168.0.18/infrasense-IOT/insertar_datos.php"  # Reemplaza con la URL correcta

# Función para obtener la lista de puentes
def obtener_puentes():
    try:
        response = requests.get(url)
        print("Respuesta de puentes:", response.text)  # Depuración: imprimir respuesta completa
        if response.status_code == 200:
            return response.json()  # Intentar decodificar como JSON
        else:
            print("Error al obtener puentes:", response.status_code)
            return []
    except Exception as e:
        print("Error de conexión:", e)
        return []

# Función para obtener la lista de galgas de un puente específico
def obtener_galgas(id_puente):
    try:
        response = requests.get(f"{url}?idPuente={id_puente}")
        print("Respuesta de galgas:", response.text)  # Depuración: imprimir respuesta completa
        if response.status_code == 200:
            return response.json()  # Intentar decodificar como JSON
        else:
            print("Error al obtener galgas:", response.status_code)
            return []
    except Exception as e:
        print("Error de conexión:", e)
        return []

# Función para calcular el coseno usando la serie de Taylor
def calculate_cos_taylor(x, n):
    result = 1
    sign = -1
    factorial = 1
    power = x * x
    for i in range(1, n):
        factorial *= (2 * i) * (2 * i - 1)
        result += sign * power / factorial
        power *= x * x
        sign *= -1
    return result

# Seleccionar el puente y la galga
def seleccionar_puente_y_galga():
    # Obtener la lista de puentes
    puentes = obtener_puentes()
    if not puentes:
        print("No se encontraron puentes.")
        return None, None

    print("Lista de Puentes:")
    for puente in puentes:
        print(f"{puente['idPuente']} - {puente['nombre']}")

    id_puente = input("Seleccione el ID del puente: ").strip()

    # Obtener la lista de galgas para el puente seleccionado
    galgas = obtener_galgas(id_puente)
    if not galgas:
        print("No se encontraron galgas para el puente seleccionado.")
        return None, None

    print("Lista de Galgas:")
    for galga in galgas:
        print(f"{galga['idGalga']} - {galga['ubicacion']}")

    id_galga = input("Seleccione el ID de la galga: ").strip()
    return id_puente, id_galga

def obtener_fecha_hora():
    tm = utime.localtime()
    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])

# Bucle principal para generar datos y enviarlos
def enviar_datos(id_puente, id_galga):
    global NTaylor, angle
    while True:
        # Configurar el ángulo en radianes
        angle_rad = math.radians(angle)

        # Calcular coseno con Taylor y trigonométrico
        cos_taylor_value = calculate_cos_taylor(angle_rad, NTaylor)  # Aproximación con Taylor
        cos_trig_value = math.cos(angle_rad)                         # Valor exacto usando math.cos
        error_value = abs(cos_taylor_value - cos_trig_value)         # Error absoluto
        fecha_actual = obtener_fecha_hora()
        # Crear el JSON para enviar
        data = {
            "idGalga": id_galga,
            "Cos_Taylor": cos_taylor_value,
            "Fecha": fecha_actual
        }

        # Convertir el JSON en una cadena y enviarlo al servidor
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, data=ujson.dumps(data), headers=headers)
            print("Ángulo:", angle, "Data:", data)
            print("Respuesta del servidor:", response.text)
            response.close()
        except Exception as e:
            print("Error al enviar datos:", e)

        # Incrementar ángulo de 0 a 360
        NTaylor += 1
        angle = (angle + 1) % 360  # Incrementa en 1 grado, reinicia a 0 después de 360

        # Pausar entre envíos
        time.sleep(1)  # Pausa de 1 segundo entre envíos para evitar envíos rápidos

# Programa principal
def main():
    id_puente, id_galga = seleccionar_puente_y_galga()
    if id_puente and id_galga:
        print(f"Iniciando envío de datos para Puente {id_puente} y Galga {id_galga}.")
        enviar_datos(id_puente, id_galga)
    else:
        print("Selección de puente o galga inválida. Terminando programa.")

# Iniciar el programa
if __name__ == "__main__":
    main()
