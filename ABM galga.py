import requests
from datetime import datetime

URL_PUENTE = "http://127.0.0.1/infrasense-IOT/puente.php"  # URL para manejar puentes
URL_GALGA = "http://127.0.0.1/infrasense-IOT/galga.php"  # URL para manejar galgas

# Funciones para Puentes

def enviar_datos_al_servidor(ubicacion, nombre_puente):
    try:
        datos = {
            "nombre_puente": nombre_puente,
            "ubicacion": ubicacion
        }
        respuesta = requests.post(URL_PUENTE, data=datos)
        
        if respuesta.status_code == 200:
            print("Éxito: Los datos se enviaron correctamente al servidor.")
        else:
            print(f"Error en la solicitud: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: No se pudo conectar con el servidor: {e}")

def obtener_puentes():
    try:
        respuesta = requests.get(URL_PUENTE)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print(f"Error al obtener puentes: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: No se pudo conectar con el servidor: {e}")
    return []

def modificar_puente():
    puentes = obtener_puentes()
    if not puentes:
        print("No hay puentes disponibles para modificar.")
        return

    print("Seleccione un Puente para Modificar:")
    for i, puente in enumerate(puentes, start=1):
        print(f"{i}. ID: {puente['idPuente']}, Nombre: {puente['nombre']}")
    
    seleccion = int(input("Seleccione el número del puente a modificar: ")) - 1
    id_puente = puentes[seleccion]['idPuente']
    
    nuevo_nombre = input("Nuevo Nombre del Puente: ")
    nueva_ubicacion = input("Nueva Ubicación: ")
    
    if nuevo_nombre and nueva_ubicacion:
        datos = {
            "id_puente": id_puente,
            "nombre_puente": nuevo_nombre,
            "ubicacion": nueva_ubicacion
        }
        try:
            respuesta = requests.post(URL_PUENTE, data=datos)
            if respuesta.status_code == 200:
                print("Éxito: El puente se modificó correctamente.")
            else:
                print(f"Error en la modificación: {respuesta.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: No se pudo conectar con el servidor: {e}")

def eliminar_puente():
    puentes = obtener_puentes()
    if not puentes:
        print("No hay puentes disponibles para eliminar.")
        return

    print("Seleccione un Puente para Eliminar:")
    for i, puente in enumerate(puentes, start=1):
        print(f"{i}. ID: {puente['idPuente']}, Nombre: {puente['nombre']}")
    
    seleccion = int(input("Seleccione el número del puente a eliminar: ")) - 1
    id_puente = puentes[seleccion]['idPuente']
    
    confirmacion = input("¿Está seguro de que desea eliminar este puente? (s/n): ")
    if confirmacion.lower() == 's':
        datos = {
            "id_puente": id_puente,
            "accion": "eliminar"
        }
        try:
            respuesta = requests.post(URL_PUENTE, data=datos)
            if respuesta.status_code == 200:
                print("Éxito: El puente se eliminó correctamente.")
            else:
                print(f"Error al eliminar el puente: {respuesta.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: No se pudo conectar con el servidor: {e}")

def mostrar_puentes():
    puentes = obtener_puentes()
    if not puentes:
        print("No hay puentes disponibles.")
        return
    
    print("Listado de Puentes:")
    for puente in puentes:
        print(f"ID: {puente['idPuente']}")
        print(f"Nombre: {puente['nombre']}")
        print(f"Ubicación: {puente['ubicacion']}")
        print("-" * 30)

# Funciones para Galgas

def enviar_datos_galga(ubicacion, id_puente):
    fecha_instalacion = datetime.now().strftime("%Y-%m-%d")  # Fecha actual en formato YYYY-MM-DD
    try:
        datos = {
            "ubicacion_galga": ubicacion,
            "fecha_instalacion": fecha_instalacion,  # Usar la fecha actual del sistema
            "id_puente": id_puente
        }
        respuesta = requests.post(URL_GALGA, data=datos)
        
        if respuesta.status_code == 200:
            print("Éxito: Los datos de la galga se enviaron correctamente al servidor.")
        else:
            print(f"Error en la solicitud: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: No se pudo conectar con el servidor: {e}")

def obtener_galgas():
    try:
        respuesta = requests.get(URL_GALGA)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print(f"Error al obtener galgas: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: No se pudo conectar con el servidor: {e}")
    return []

def modificar_galga():
    galgas = obtener_galgas()
    if not galgas:
        print("No hay galgas disponibles para modificar.")
        return

    print("Seleccione una Galga para Modificar:")
    for i, galga in enumerate(galgas, start=1):
        print(f"{i}. ID: {galga['idGalga']}, Ubicación: {galga['ubicacion']}")
    
    seleccion = int(input("Seleccione el número de la galga a modificar: ")) - 1
    id_galga = galgas[seleccion]['idGalga']
    
    nueva_ubicacion = input("Nueva Ubicación de la Galga: ")
    nueva_fecha_instalacion = input("Nueva Fecha de Instalación (YYYY-MM-DD): ")
    
    if nueva_ubicacion and nueva_fecha_instalacion:
        datos = {
            "id_galga": id_galga,
            "ubicacion_galga": nueva_ubicacion,
            "fecha_instalacion": nueva_fecha_instalacion,
            "accion": "modificar"  # Añadido para indicar que se trata de una modificación
        }
        
        try:
            respuesta = requests.post(URL_GALGA, data=datos)
            if respuesta.status_code == 200:
                print("Éxito: La galga se modificó correctamente.")
            else:
                print(f"Error en la modificación: {respuesta.status_code}")
                print("Respuesta del servidor:", respuesta.text)
        except requests.exceptions.RequestException as e:
            print(f"Error: No se pudo conectar con el servidor: {e}")
    else:
        print("Error: Por favor, complete todos los campos.")


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
        try:
            respuesta = requests.post(URL_GALGA, data=datos)
            if respuesta.status_code == 200:
                print("Éxito: La galga se eliminó correctamente.")
            else:
                print(f"Error al eliminar la galga: {respuesta.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: No se pudo conectar con el servidor: {e}")

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
    print("Funcionalidad para gestionar datos aún no implementada.")

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
menu_principal()
