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

# Clase para detectar tipo de tarjeta
class Board:
    class BoardType:
        PICO_W = 'Raspberry Pi Pico W'
        ESP32 = 'ESP32-1'
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

# Clase para manejar el módulo HX711
class HX711:
    def __init__(self, data_pin, clock_pin):
        self.data_pin = Pin(data_pin, Pin.IN, pull=Pin.PULL_DOWN)
        self.clock_pin = Pin(clock_pin, Pin.OUT)
        self.clock_pin.value(0)

    def read_raw(self):
        count = 0
        while self.data_pin.value() == 1:
            pass  # Espera a que el pin de datos sea bajo
        
        for i in range(24):  # Leer 24 bits de datos
            self.clock_pin.value(1)
            count = (count << 1) | self.data_pin.value()
            self.clock_pin.value(0)
        
        # Ajuste del bit de signo (para valores negativos)
        self.clock_pin.value(1)
        count ^= 0x800000
        self.clock_pin.value(0)
        return count

    def read_weight(self, offset=0, scale=1):
        # Calcular el peso en función de la lectura y la escala
        raw_value = self.read_raw()
        return (raw_value - offset) / scale

# Detectar tipo de placa
BOARD_TYPE = Board().type
print("Tarjeta Detectada:", BOARD_TYPE)

# Configuración inicial
url = "http://192.168.0.15/infrasense-IOT/Scripts/insertar_datos.php"  # Reemplaza con la URL correcta

def obtener_fecha_hora():
    tm = utime.localtime()
    return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(tm[0], tm[1], tm[2], tm[3], tm[4], tm[5])

# Bucle principal para generar datos y enviarlos
def enviar_datos(id_puente, id_galga, hx711, offset, scale):
    while True:
        # Leer el peso desde HX711
        weight = hx711.read_weight(offset, scale)
        
        # Validar si el peso es negativo
        if weight < 0:
            weight = 0  # Si es negativo, asignar 0

        fecha_actual = obtener_fecha_hora()

        # Crear el JSON para enviar
        data = {
            "idGalga": id_galga,
            "Peso": weight,
            "Fecha": fecha_actual,
            "IoThing": BOARD_TYPE
        }

        # Convertir el JSON en una cadena y enviarlo al servidor
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(url, data=ujson.dumps(data), headers=headers)
            print("Peso:", weight, "Data:", data)
            print("Respuesta del servidor:", response.text)
            response.close()
        except Exception as e:
            print("Error al enviar datos:", e)

        # Pausar entre envíos
        time.sleep(1)   # Pausa de 1 segundo entre envíos para evitar envíos rápidos

# Programa principal
def main():
    # Definir los IDs directamente
    id_puente = "4"  # Reemplaza con el ID del puente deseado
    id_galga = "24"   # Reemplaza con el ID de la galga deseada

    print(f"Iniciando envío de datos para Puente {id_puente} y Galga {id_galga}.")

    # Configurar HX711
    hx711 = HX711(data_pin=21, clock_pin=22)
    offset = hx711.read_raw()  
    scale = 2280  
    
    enviar_datos(id_puente, id_galga, hx711, offset, scale)

# Iniciar el programa
if __name__ == "__main__":
    main()
