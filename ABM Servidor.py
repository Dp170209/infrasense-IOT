import requests

# URL del archivo PHP que se usará para insertar datos en la base de datos
URL = "http://192.168.0.18/ABM.php"  # Cambia esta URL por la de tu servidor

# --- Funciones de Servidor para Puentes ---

def enviar_datos_al_servidor(ubicacion, nombre_puente):
    datos = {
        "nombre_puente": nombre_puente,
        "ubicacion": ubicacion
    }
    try:
        respuesta = requests.post(URL, data=datos)
        if respuesta.status_code == 200:
            print("Éxito: Los datos se enviaron correctamente al servidor.")
        else:
            print(f"Error: No se pudo enviar los datos, código de error {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: No se pudo conectar con el servidor: {e}")

def obtener_puentes():
    try:
        respuesta = requests.get(URL)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            print(f"Error al obtener puentes: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error: No se pudo conectar con el servidor: {e}")
    return []

# --- Funciones para Manipular Puentes ---

def agregar_puente():
    nombre_puente = input("Ingrese el nombre del puente: ")
    ubicacion = input("Ingrese la ubicación: ")
    if nombre_puente and ubicacion:
        enviar_datos_al_servidor(ubicacion, nombre_puente)
    else:
        print("Advertencia: Todos los campos son obligatorios.")

def modificar_puente():
    puentes = obtener_puentes()
    if not puentes:
        print("No hay puentes disponibles para modificar.")
        return

    print("Seleccione el puente a modificar:")
    for i, p in enumerate(puentes, start=1):
        print(f"{i}. ID: {p['idPuente']} - Nombre: {p['nombre']}")
    seleccion = int(input("Número del puente: ")) - 1

    id_puente = puentes[seleccion]["idPuente"]
    nombre_actual = puentes[seleccion]["nombre"]
    ubicacion_actual = puentes[seleccion]["ubicacion"]

    nuevo_nombre = input(f"Nuevo nombre (actual: {nombre_actual}): ") or nombre_actual
    nueva_ubicacion = input(f"Nueva ubicación (actual: {ubicacion_actual}): ") or ubicacion_actual

    datos = {
        "id_puente": id_puente,
        "nombre_puente": nuevo_nombre,
        "ubicacion": nueva_ubicacion
    }
    try:
        respuesta = requests.post(URL, data=datos)
        if respuesta.status_code == 200:
            print("El puente se modificó correctamente.")
        else:
            print(f"Error en la modificación: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"No se pudo conectar con el servidor: {e}")

def eliminar_puente():
    puentes = obtener_puentes()
    if not puentes:
        print("No hay puentes disponibles para eliminar.")
        return

    print("Seleccione el puente a eliminar:")
    for i, p in enumerate(puentes, start=1):
        print(f"{i}. ID: {p['idPuente']} - Nombre: {p['nombre']}")
    seleccion = int(input("Número del puente: ")) - 1

    id_puente = puentes[seleccion]["idPuente"]

    confirmacion = input("¿Está seguro de que desea eliminar este puente? (s/n): ").lower()
    if confirmacion == "s":
        datos = {
            "id_puente": id_puente,
            "accion": "eliminar"
        }
        try:
            respuesta = requests.post(URL, data=datos)
            if respuesta.status_code == 200:
                print("El puente se eliminó correctamente.")
            else:
                print(f"Error al eliminar el puente: {respuesta.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"No se pudo conectar con el servidor: {e}")

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

# --- Menú de Puentes ---

def menu_puentes():
    while True:
        print("\n--- Menú Puentes ---")
        print("1. Agregar Puente")
        print("2. Modificar Puente")
        print("3. Eliminar Puente")
        print("4. Mostrar Puentes")
        print("5. Volver al Menú Principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_puente()
        elif opcion == "2":
            modificar_puente()
        elif opcion == "3":
            eliminar_puente()
        elif opcion == "4":
            mostrar_puentes()
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# --- Menú de Galgas (a definir funciones si existen similar a las de Puentes) ---

def menu_galgas():
    while True:
        print("\n--- Menú Galgas ---")
        print("1. Agregar Galga")
        print("2. Modificar Galga")
        print("3. Eliminar Galga")
        print("4. Mostrar Galgas")
        print("5. Volver al Menú Principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("Función para agregar Galga no implementada aún")
        elif opcion == "2":
            print("Función para modificar Galga no implementada aún")
        elif opcion == "3":
            print("Función para eliminar Galga no implementada aún")
        elif opcion == "4":
            print("Función para mostrar Galgas no implementada aún")
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# --- Menú de Datos (a definir funciones si existen similar a las de Puentes) ---

def menu_datos():
    while True:
        print("\n--- Menú Datos ---")
        print("1. Agregar Dato")
        print("2. Modificar Dato")
        print("3. Eliminar Dato")
        print("4. Mostrar Datos")
        print("5. Volver al Menú Principal")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("Función para agregar Dato no implementada aún")
        elif opcion == "2":
            print("Función para modificar Dato no implementada aún")
        elif opcion == "3":
            print("Función para eliminar Dato no implementada aún")
        elif opcion == "4":
            print("Función para mostrar Datos no implementada aún")
        elif opcion == "5":
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# --- Menú Principal ---

def menu_principal():
    while True:
        print("\n--- Menú Principal ---")
        print("1. Puentes")
        print("2. Galgas")
        print("3. Datos")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_puentes()
        elif opcion == "2":
            menu_galgas()
        elif opcion == "3":
            menu_datos()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    menu_principal()
