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
from Wifi_lib import wifi_init 

# URLs de los archivos PHP en el servidor
URL_PUENTE = "http://192.168.0.13/infrasense-IOT/puente.php"
URL_GALGA = "http://192.168.0.13/infrasense-IOT/galga.php"
URL_DATOS = "http://192.168.0.13/infrasense-IOT/datos.php"

# Funciones para manejo de errores HTTP y de red
def http_post(url, data):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=ujson.dumps(data).encode('utf-8'), headers=headers)
        if response.status_code == 200:
            return response
        else:
            print(f"Error en la solicitud: Código de estado {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la conexión con el servidor: {e}")
        return None

def http_get(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en la solicitud: Código de estado {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error en la conexión con el servidor: {e}")
        return None

# --- Funciones de Puentes ---
def enviar_datos_al_servidor(ubicacion, nombre_puente):
    datos = {
        "nombre_puente": nombre_puente,
        "ubicacion": ubicacion
    }
    respuesta = http_post(URL_PUENTE, datos)
    if respuesta:
        print("Éxito: Los datos se enviaron correctamente al servidor.")

def obtener_puentes():
    puentes = http_get(URL_PUENTE)
    if puentes:
        return puentes
    print("Error: No se pudo obtener la lista de puentes.")
    return []

def agregar_puente():
    nombre_puente = input("Ingrese el nombre del puente: ").strip()
    ubicacion = input("Ingrese la ubicación: ").strip()
    if nombre_puente and ubicacion:
        enviar_datos_al_servidor(ubicacion, nombre_puente)
    else:
        print("Advertencia: Todos los campos son obligatorios.")

def modificar_puente():
    puentes = obtener_puentes()
    if not puentes:
        print("No hay puentes disponibles para modificar.")
        return

    try:
        print("Seleccione el puente a modificar:")
        for i, p in enumerate(puentes, start=1):
            print(f"{i}. ID: {p['idPuente']} - Nombre: {p['nombre']}")
        seleccion = int(input("Número del puente: ")) - 1
        if seleccion < 0 or seleccion >= len(puentes):
            raise ValueError("Selección inválida.")

        id_puente = puentes[seleccion]["idPuente"]
        nombre_actual = puentes[seleccion]["nombre"]
        ubicacion_actual = puentes[seleccion]["ubicacion"]

        nuevo_nombre = input(f"Nuevo nombre (actual: {nombre_actual}): ").strip() or nombre_actual
        nueva_ubicacion = input(f"Nueva ubicación (actual: {ubicacion_actual}): ").strip() or ubicacion_actual

        datos_modificados = {
            "id_puente": id_puente,
            "nombre_puente": nuevo_nombre,
            "ubicacion": nueva_ubicacion,
            "accion": "modificar"
        }
        respuesta = http_post(URL_PUENTE, datos_modificados)
        if respuesta:
            print("El puente se modificó correctamente.")
    except ValueError as e:
        print(f"Error de selección: {e}")
    except Exception as e:
        print("Error inesperado:", e)

def eliminar_puente():
    puentes = obtener_puentes()
    if not puentes:
        print("No hay puentes disponibles para eliminar.")
        return

    try:
        print("Seleccione el puente a eliminar:")
        for i, p in enumerate(puentes, start=1):
            print(f"{i}. ID: {p['idPuente']} - Nombre: {p['nombre']}")
        seleccion = int(input("Número del puente: ")) - 1
        if seleccion < 0 or seleccion >= len(puentes):
            raise ValueError("Selección inválida.")

        id_puente = puentes[seleccion]["idPuente"]
        confirmacion = input("¿Está seguro de que desea eliminar este puente? (s/n): ").lower()
        if confirmacion == "s":
            datos = {"id_puente": id_puente, "accion": "eliminar"}
            respuesta = http_post(URL_PUENTE, datos)
            if respuesta:
                print("El puente se eliminó correctamente.")
    except ValueError as e:
        print(f"Error de selección: {e}")
    except Exception as e:
        print("Error inesperado:", e)

def mostrar_puentes():
    puentes = obtener_puentes()
    if not puentes:
        print("No hay puentes para mostrar.")
    else:
        print("Listado de Puentes:")
        for puente in puentes:
            print(f"ID: {puente['idPuente']}")
            print(f"Nombre: {puente['nombre']}")
            print(f"Ubicación: {puente['ubicacion']}")
            print("-" * 30)

# --- Funciones de Galgas ---
def enviar_datos_galga(ubicacion, id_puente):
    fecha_instalacion = "{:04}-{:02}-{:02}".format(utime.localtime()[0], utime.localtime()[1], utime.localtime()[2])
    datos = {
        "ubicacion_galga": ubicacion,
        "fecha_instalacion": fecha_instalacion,
        "id_puente": id_puente
    }
    respuesta = http_post(URL_GALGA, datos)
    if respuesta:
        print("Éxito: Los datos de la galga se enviaron correctamente al servidor.")

def obtener_galgas():
    galgas = http_get(URL_GALGA)
    if galgas:
        return galgas
    print("Error: No se pudo obtener la lista de galgas.")
    return []

def modificar_galga():
    galgas = obtener_galgas()
    if not galgas:
        print("No hay galgas disponibles para modificar.")
        return

    try:
        print("Seleccione una Galga para Modificar:")
        for i, galga in enumerate(galgas, start=1):
            print(f"{i}. ID: {galga['idGalga']}, Ubicación: {galga['ubicacion']}")
        seleccion = int(input("Seleccione el número de la galga a modificar: ")) - 1
        if seleccion < 0 or seleccion >= len(galgas):
            raise ValueError("Selección inválida.")

        id_galga = galgas[seleccion]['idGalga']
        galga_actual = galgas[seleccion]["ubicacion"]
        fecha_actual = galgas[seleccion]["fecha_instalacion"]

        nueva_ubicacion = input(f"Nueva Ubicación de la Galga (actual: {galga_actual}): ").strip() or galga_actual
        nueva_fecha_instalacion = input(f"Nueva Fecha de Instalación (actual: {fecha_actual}): ").strip() or fecha_actual

        datos = {
            "id_galga": id_galga,
            "ubicacion_galga": nueva_ubicacion,
            "fecha_instalacion": nueva_fecha_instalacion,
            "accion": "modificar"
        }
        respuesta = http_post(URL_GALGA, datos)
        if respuesta:
            print("Éxito: La galga se modificó correctamente.")
    except ValueError as e:
        print(f"Error de selección: {e}")
    except Exception as e:
        print("Error inesperado:", e)
        
def eliminar_galga():
    galgas = obtener_galgas()
    if not galgas:
        print("No hay galgas disponibles para eliminar.")
        return

    print("Seleccione una Galga para Eliminar:")
    for i, galga in enumerate(galgas, start=1):
        print(f"{i}. ID: {galga['idGalga']}, Ubicación: {galga['ubicacion']}")
    
    seleccion = int(input("Seleccione el número de la galga a eliminar: ")) - 1
    id_galga = galgas[seleccion]['idGalga']
    
    confirmacion = input("¿Está seguro de que desea eliminar esta galga? (s/n): ")
    if confirmacion.lower() == 's':
        datos = {
            "id_galga": id_galga,
            "accion": "eliminar"
        }
        headers = {'Content-Type': 'application/json'}
        try:
            respuesta = requests.post(URL_GALGA, data=ujson.dumps(datos).encode('utf-8'), headers=headers)
            if respuesta.status_code == 200:
                print("Éxito: La galga se eliminó correctamente.")
            else:
                print(f"Error al eliminar la galga: {respuesta.status_code}")
        except Exception as e:
            print("Error de conexión:", e)

def mostrar_galgas():
    galgas = obtener_galgas()
    if not galgas:
        print("No hay galgas disponibles.")
        return
    
    print("Listado de Galgas:")
    for galga in galgas:
        print(f"ID: {galga['idGalga']}")
        print(f"Ubicación: {galga['ubicacion']}")
        print(f"Fecha de Instalación: {galga['fecha_instalacion']}")
        print("-" * 30)
        
# --- Funciones de Servidor para datos ---
NTaylor = 1
angle = 0  # Ángulo en grados

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

def obtener_galgas_puente(id_puente):
    try:
        response = requests.get(f"{URL_DATOS}?idPuente={id_puente}")
        if response.status_code == 200:
            return response.json()  # Intentar decodificar como JSON
        else:
            print("Error al obtener galgas:", response.status_code)
            return []
    except Exception as e:
        print("Error de conexión:", e)
        return []

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
    galgas = obtener_galgas_puente(id_puente)
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
            "Cos_Trig":cos_trig_value,
            "Error":error_value,
            "Fecha": fecha_actual
        }
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(URL_DATOS, data=ujson.dumps(data), headers=headers)
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

def obtener_datos_lectura():
    try:
        response = requests.get(URL_DATOS)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener datos: {response.status_code}")
            return []
    except Exception as e:
        print("Error de conexión:", e)
    return []

def modificar_dato():
    datos = obtener_datos_lectura()
    if not datos:
        print("No hay Datos disponibles para modificar.")
        return

    print("Seleccione el dato a modificar:")
    for i, p in enumerate(datos, start=1):
        print(f"{i}. ID: {p['idDato']} - Cos Taylor: {p['Cos_Taylor']} - Cos Trig: {p['Cos_Trig']} - Error: {p['Error']} - Fecha Hora: {p['fecha_hora']}")
    seleccion = int(input("Número del dato: ")) - 1

    id_dato = datos[seleccion]["idDato"]
    taylor_actual = datos[seleccion]["Cos_Taylor"]
    trig_actual = datos[seleccion]["Cos_Trig"]
    error_actual = datos[seleccion]["Error"]

    nuevo_taylor = input(f"Nuevo valor Taylor (actual: {taylor_actual}): ") or taylor_actual
    nuevo_trig = input(f"Nuevo valor Trig (actual: {trig_actual}): ") or trig_actual
    nuevo_error = input(f"Nuevo valor Error (actual: {error_actual}): ") or error_actual

    datos = {
        "id_dato": id_dato,
        "nuevo_taylor": nuevo_taylor,
        "nuevo_trig": nuevo_trig,
        "nuevo_error": nuevo_error
    }
    headers = {'Content-Type': 'application/json'}
    try:
        respuesta = requests.post(URL_DATOS, data=ujson.dumps(datos).encode('utf-8'), headers=headers)
        if respuesta.status_code == 200:
            print("El dato se modificó correctamente.")
        else:
            print(f"Error en la modificación: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"No se pudo conectar con el servidor: {e}")

        
def mostrar_datos():
    datos = obtener_datos_lectura()
    if not datos:
        print("No hay datos para mostrar.")
    else:
        print("Listado de Datos:")
        for dato in datos:
            print(f" ID: {dato['idDato']} - Cos Taylor: {dato['Cos_Taylor']} - Cos Trig: {dato['Cos_Trig']} - Error: {dato['Error']} - Fecha Hora: {dato['fecha_hora']} -  idGalga: {dato['idGalga']}")
            
def eliminar_dato():
    datos = obtener_datos_lectura()
    if not datos:
        print("No hay datos disponibles para eliminar.")
        return

    print("Seleccione el dato a eliminar:")
    for i, p in enumerate(datos, start=1):
        print(f"{i}. ID: {p['idDato']} - Cos Taylor: {p['Cos_Taylor']} - Cos Trig: {p['Cos_Trig']} - Error: {p['Error']} - Fecha Hora: {p['fecha_hora']}")
    seleccion = int(input("Número del dato: ")) - 1

    id_dato = datos[seleccion]["idDato"]

    confirmacion = input("¿Está seguro de que desea eliminar este dato? (s/n): ").lower()
    if confirmacion == "s":
        datos = {
            "id_dato": id_dato,
            "accion": "eliminar"
        }
        headers = {'Content-Type': 'application/json'}
        try:
            respuesta = requests.post(URL_DATOS, data=ujson.dumps(datos).encode('utf-8'), headers=headers)
            if respuesta.status_code == 200:
                print("El dato se eliminó correctamente.")
            else:
                print(f"Error al eliminar el puente: {respuesta.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"No se pudo conectar con el servidor: {e}")
# Submenú para gestionar Puentes
def menu_puentes():
    while True:
        print("\nOpciones de Puente")
        print("1. Agregar Puente")
        print("2. Modificar Puente")
        print("3. Eliminar Puente")
        print("4. Mostrar Puentes")
        print("5. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            nombre_puente = input("Ingrese el Nombre del Puente: ")
            ubicacion = input("Ingrese la Ubicación: ")
            if nombre_puente and ubicacion:
                enviar_datos_al_servidor(ubicacion, nombre_puente)
            else:
                print("Error: Por favor, complete todos los campos.")
        
        elif opcion == '2':
            modificar_puente()
        
        elif opcion == '3':
            eliminar_puente()
        
        elif opcion == '4':
            mostrar_puentes()
        
        elif opcion == '5':
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

# Submenú para gestionar Galgas
def menu_galgas():
    while True:
        print("\nOpciones de Galga")
        print("1. Agregar Galga")
        print("2. Modificar Galga")
        print("3. Eliminar Galga")
        print("4. Mostrar Galgas")
        print("5. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            puentes = obtener_puentes()
            if not puentes:
                print("No hay puentes disponibles para asignar la galga.")
            else:
                print("Seleccione el Puente donde desea agregar la galga:")
                for i, puente in enumerate(puentes, start=1):
                    print(f"{i}. ID: {puente['idPuente']}, Nombre: {puente['nombre']}")
                
                seleccion = int(input("Seleccione el número del puente: ")) - 1
                id_puente = puentes[seleccion]['idPuente']
                
                ubicacion = input("Ingrese la Ubicación de la Galga: ")
                
                if ubicacion:
                    enviar_datos_galga(ubicacion, id_puente)
                else:
                    print("Error: Por favor, complete todos los campos.")
        elif opcion == '2':
            modificar_galga()
        
        elif opcion == '3':
            eliminar_galga()
        
        elif opcion == '4':
            mostrar_galgas()
        
        elif opcion == '5':
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

# Submenú para gestionar Datos (si es necesario implementar)
def menu_datos():
    while True:
        print("\nOpciones de Galga")
        print("1. Agregar Dato")
        print("2. Modificar Dato")
        print("3. Eliminar Dato")
        print("4. Mostrar Datos")
        print("5. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            id_puente, id_galga = seleccionar_puente_y_galga()
            if id_puente and id_galga:
                enviar_datos(id_puente, id_galga)
            else:
                print("Selección de puente o galga inválida. Terminando programa.")
        elif opcion == '2':
            modificar_dato()
        
        elif opcion == '3':
            eliminar_dato()
        
        elif opcion == '4':
            mostrar_datos()
        
        elif opcion == '5':
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

# Menú principal para seleccionar entre Puentes, Galgas o Datos
def menu_principal():
    while True:
        print("\nSeleccione la entidad que desea gestionar:")
        print("1. Puentes")
        print("2. Galgas")
        print("3. Datos")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            menu_puentes()
        
        elif opcion == '2':
            menu_galgas()
        
        elif opcion == '3':
            menu_datos()
        
        elif opcion == '4':
            print("Saliendo del programa.")
            break
        
        else:
            print("Opción no válida. Intente de nuevo.")

# Ejecutar el menú principal
try:
    wifi_init()
    menu_principal()
except Exception as e:
    print("Error en la ejecución del programa:", e)