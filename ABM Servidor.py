import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime

URL_PUENTE = "http://172.20.10.13/infrasense-IOT/puente.php"
URL_GALGA = "http://172.20.10.13/infrasense-IOT/galga.php"
URL_DATOS = "http://172.20.10.13/infrasense-IOT/datos.php"

def enviar_datos_al_servidor(ubicacion, nombre_puente):
    try:
        datos = {
            "nombre_puente": nombre_puente,
            "ubicacion": ubicacion
        }
        # Send as JSON
        respuesta = requests.post(URL_PUENTE, json=datos)
        
        if respuesta.status_code == 200:
            messagebox.showinfo("Éxito", "Los datos se enviaron correctamente al servidor.")
        else:
            messagebox.showerror("Error", f"Error en la solicitud: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
# Función para abrir una nueva ventana donde se ingresan los datos
def datos_puente():
    ventana_datos = tk.Toplevel(ventana)
    ventana_datos.title("Ingresar Datos del Puente")
    ventana_datos.geometry("300x200")
    
    # Etiquetas y campos de entrada
    tk.Label(ventana_datos, text="Nombre del puente:").pack(pady=5)
    entrada_nombre_puente = tk.Entry(ventana_datos)
    entrada_nombre_puente.pack(pady=5)
    
    tk.Label(ventana_datos, text="Ubicación:").pack(pady=5)
    entrada_ubicacion = tk.Entry(ventana_datos)
    entrada_ubicacion.pack(pady=5)
    
    # Función que recoge los datos de los campos y llama a `enviar_datos_al_servidor`
    def procesar_datos():
        ubicacion = entrada_ubicacion.get()
        nombre_puente = entrada_nombre_puente.get()
        
        if ubicacion and nombre_puente:
            enviar_datos_al_servidor(ubicacion, nombre_puente)
            ventana_datos.destroy()  # Cerrar la ventana después de enviar los datos
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
    
    # Botón para enviar los datos
    tk.Button(ventana_datos, text="Enviar", command=procesar_datos).pack(pady=20)
# Función para obtener todos los puentes
def obtener_puentes():
    try:
        respuesta = requests.get(URL_PUENTE)
        if respuesta.status_code == 200:
            return respuesta.json()  
        else:
            messagebox.showerror("Error", f"Error al obtener puentes: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
    return []
# Función para obtener datos de un puente específico
def obtener_datos_puente(id_puente):
    try:
        respuesta = requests.get(URL_PUENTE, params={"id_puente": id_puente})
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            messagebox.showerror("Error", f"Error al obtener datos del puente: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
    return {}
# Función para modificar un puente
def modificar_puente():
    puentes = obtener_puentes() 
    
    ventana_modificar = tk.Toplevel(ventana)
    ventana_modificar.title("Modificar Puente")
    ventana_modificar.geometry("400x300")
    tk.Label(ventana_modificar, text="Seleccione un Puente para Modificar:").pack(pady=5)
    
    puente_seleccionado = tk.StringVar()
    opciones = [f"{p['idPuente']} - {p['nombre']}" for p in puentes]
    menu_puentes = tk.OptionMenu(ventana_modificar, puente_seleccionado, *opciones)
    menu_puentes.pack(pady=5)
    
    tk.Label(ventana_modificar, text="Nuevo Nombre del Puente:").pack(pady=5)
    entrada_nombre = tk.Entry(ventana_modificar)
    entrada_nombre.pack(pady=5)
    
    tk.Label(ventana_modificar, text="Nueva Ubicación:").pack(pady=5)
    entrada_ubicacion = tk.Entry(ventana_modificar)
    entrada_ubicacion.pack(pady=5)
    
    datos_actuales = {"nombre": "", "ubicacion": ""}
    
    def cargar_datos_puente(*args):
        seleccion = puente_seleccionado.get()
        if seleccion:
            id_puente = seleccion.split(" - ")[0]
            datos = obtener_datos_puente(id_puente)
            if datos:
                datos_actuales["nombre"] = datos.get("nombre_puente", "")
                datos_actuales["ubicacion"] = datos.get("ubicacion", "")
                entrada_nombre.delete(0, tk.END)
                entrada_ubicacion.delete(0, tk.END)
                entrada_nombre.insert(0, datos_actuales["nombre"])
                entrada_ubicacion.insert(0, datos_actuales["ubicacion"])
                
    puente_seleccionado.trace("w", cargar_datos_puente)
    
    def enviar_modificacion():
        seleccion = puente_seleccionado.get()
        if seleccion:
            id_puente = seleccion.split(" - ")[0]
            nuevo_nombre = entrada_nombre.get() or datos_actuales["nombre"]
            nueva_ubicacion = entrada_ubicacion.get() or datos_actuales["ubicacion"]
            
            if nuevo_nombre and nueva_ubicacion:
                datos = {
                    "id_puente": id_puente,
                    "nombre_puente": nuevo_nombre,
                    "ubicacion": nueva_ubicacion,
                    "accion": "modificar"
                }
                try:
                    respuesta = requests.post(URL_PUENTE, json=datos)
                    if respuesta.status_code == 200:
                        messagebox.showinfo("Éxito", "El puente se modificó correctamente.")
                        ventana_modificar.destroy()
                    else:
                        messagebox.showerror("Error", f"Error en la modificación: {respuesta.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
            else:
                messagebox.showwarning("Advertencia", "Completa todos los campos.")
    
    tk.Button(ventana_modificar, text="Guardar Cambios", command=enviar_modificacion).pack(pady=20)

# Función para eliminar un puente
def eliminar_puente():
    puentes = obtener_puentes()
    
    ventana_eliminar = tk.Toplevel(ventana)
    ventana_eliminar.title("Eliminar Puente")
    ventana_eliminar.geometry("400x200")
    tk.Label(ventana_eliminar, text="Seleccione un Puente para Eliminar:").pack(pady=5)
    
    puente_seleccionado = tk.StringVar()
    opciones = [f"{p['idPuente']} - {p['nombre']}" for p in puentes]
    menu_puentes = tk.OptionMenu(ventana_eliminar, puente_seleccionado, *opciones)
    menu_puentes.pack(pady=5)
    
    def confirmar_eliminacion():
        seleccion = puente_seleccionado.get()
        if seleccion:
            id_puente = seleccion.split(" - ")[0]
            confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este puente?")
            if confirmacion:
                datos = {
                    "id_puente": id_puente,
                    "accion": "eliminar"
                }
                try:
                    respuesta = requests.post(URL_PUENTE, json=datos)
                    if respuesta.status_code == 200:
                        messagebox.showinfo("Éxito", "El puente se eliminó correctamente.")
                        ventana_eliminar.destroy()
                    else:
                        messagebox.showerror("Error", f"Error al eliminar el puente: {respuesta.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
    
    tk.Button(ventana_eliminar, text="Eliminar", command=confirmar_eliminacion).pack(pady=20)
    
# Función para mostrar todos los puentes
def mostrar_puente():
    puentes = obtener_puentes()
    if not puentes:
        messagebox.showwarning("Advertencia", "No hay puentes disponibles.")
        return

    # Create display window with specified size and styling
    ventana_mostrar_puentes = tk.Toplevel(ventana)
    ventana_mostrar_puentes.title("Listado de Puentes")
    ventana_mostrar_puentes.geometry("315x450")
    ventana_mostrar_puentes.config(bg="#f8f9fa")

    frame_contenido = tk.Frame(ventana_mostrar_puentes, bg="#f8f9fa")
    frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    titulo = tk.Label(frame_contenido, text="Listado de Puentes", font=("Arial", 12, "bold"), bg="#f8f9fa")
    titulo.pack(pady=5)

    canvas = tk.Canvas(frame_contenido, bg="#f8f9fa", highlightthickness=0, width=290, height=350)
    scroll_y = tk.Scrollbar(frame_contenido, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f8f9fa")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    for puente in puentes:
        frame_puente = tk.Frame(scrollable_frame, bg="#e9ecef", bd=1, relief="solid", padx=5, pady=5)
        frame_puente.pack(fill="x", pady=5)

        tk.Label(frame_puente, text=f"ID: {puente['idPuente']}", font=("Arial", 10, "bold"), bg="#e9ecef").pack(anchor="w")
        tk.Label(frame_puente, text=f"Nombre: {puente['nombre']}", font=("Arial", 10), bg="#e9ecef").pack(anchor="w")
        tk.Label(frame_puente, text=f"Ubicación: {puente['ubicacion']}", font=("Arial", 10), bg="#e9ecef").pack(anchor="w")

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

#----------------------------------------------------------------------------------------------------------
def enviar_datos_galga(ubicacion, id_puente):
    fecha_instalacion = datetime.now().strftime("%Y-%m-%d")
    datos = {
        "ubicacion_galga": ubicacion,
        "fecha_instalacion": fecha_instalacion,
        "id_puente": id_puente,
        "accion": "agregar"
    }
    try:
        respuesta = requests.post(URL_GALGA, json=datos)
        if respuesta.status_code == 200:
            messagebox.showinfo("Éxito", "Los datos de la galga se enviaron correctamente al servidor.")
        else:
            messagebox.showerror("Error", f"Error en la solicitud: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
        
def datos_galga():
    puentes = obtener_puentes()
    if not puentes:
        messagebox.showwarning("Advertencia", "No hay puentes disponibles para asignar la galga.")
        return

    ventana_galga = tk.Toplevel(ventana)
    ventana_galga.title("Agregar Galga")
    ventana_galga.geometry("400x250")
    ventana_galga.config(bg="#f0f0f0")

    tk.Label(ventana_galga, text="Seleccione el Puente:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
    puente_seleccionado = tk.StringVar()
    opciones_puentes = [f"{p['idPuente']} - {p['nombre']}" for p in puentes]
    menu_puentes = tk.OptionMenu(ventana_galga, puente_seleccionado, *opciones_puentes)
    menu_puentes.pack(pady=5)

    tk.Label(ventana_galga, text="Ubicación de la Galga:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
    entrada_ubicacion_galga = tk.Entry(ventana_galga, font=("Arial", 12))
    entrada_ubicacion_galga.pack(pady=5)


    def procesar_datos_galga():
        seleccion = puente_seleccionado.get()
        ubicacion = entrada_ubicacion_galga.get()

        if seleccion and ubicacion:
            id_puente = seleccion.split(" - ")[0]
            enviar_datos_galga(ubicacion, id_puente)
            ventana_galga.destroy()
        else:
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

    tk.Button(ventana_galga, text="Enviar", command=procesar_datos_galga, font=("Arial", 12), bg="#e6e6e6", relief=tk.RAISED).pack(pady=20)

def obtener_galgas():
    try:
        respuesta = requests.get(URL_GALGA)
        if respuesta.status_code == 200:
            return respuesta.json()  
        else:
            messagebox.showerror("Error", f"Error al obtener galgas: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
    return []

def modificar_galga():
    galgas = obtener_galgas()
    if not galgas:
        messagebox.showwarning("Advertencia", "No hay galgas disponibles para modificar.")
        return

    ventana_modificar_galga = tk.Toplevel(ventana)
    ventana_modificar_galga.title("Modificar Galga")
    ventana_modificar_galga.geometry("400x300")
    ventana_modificar_galga.config(bg="#f0f0f0")

    tk.Label(ventana_modificar_galga, text="Seleccione una Galga:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
    galga_seleccionada = tk.StringVar()
    opciones_galgas = [f"{g['idGalga']} - {g['ubicacion']}" for g in galgas]
    menu_galgas = tk.OptionMenu(ventana_modificar_galga, galga_seleccionada, *opciones_galgas)
    menu_galgas.pack(pady=5)

    tk.Label(ventana_modificar_galga, text="Nueva Ubicación:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
    entrada_ubicacion = tk.Entry(ventana_modificar_galga, font=("Arial", 12))
    entrada_ubicacion.pack(pady=5)

    tk.Label(ventana_modificar_galga, text="Nueva Fecha de Instalación (YYYY-MM-DD):", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
    entrada_fecha_instalacion = tk.Entry(ventana_modificar_galga, font=("Arial", 12))
    entrada_fecha_instalacion.pack(pady=5)

    datos_actuales = {"ubicacion": "", "fecha_instalacion": ""}

    def cargar_datos_galga(*args):
        seleccion = galga_seleccionada.get()
        if seleccion:
            id_galga = seleccion.split(" - ")[0]
            galga = next((g for g in galgas if g['idGalga'] == id_galga), None)
            if galga:
                datos_actuales["ubicacion"] = galga["ubicacion"]
                datos_actuales["fecha_instalacion"] = galga["fecha_instalacion"]
                entrada_ubicacion.delete(0, tk.END)
                entrada_fecha_instalacion.delete(0, tk.END)
                entrada_ubicacion.insert(0, datos_actuales["ubicacion"])
                entrada_fecha_instalacion.insert(0, datos_actuales["fecha_instalacion"])

    galga_seleccionada.trace("w", cargar_datos_galga)

    def enviar_modificacion_galga():
        seleccion = galga_seleccionada.get()
        if seleccion:
            id_galga = seleccion.split(" - ")[0]
            nueva_ubicacion = entrada_ubicacion.get() or datos_actuales["ubicacion"]
            nueva_fecha_instalacion = entrada_fecha_instalacion.get() or datos_actuales["fecha_instalacion"]

            if nueva_ubicacion and nueva_fecha_instalacion:
                datos = {
                    "id_galga": id_galga,
                    "ubicacion_galga": nueva_ubicacion,
                    "fecha_instalacion": nueva_fecha_instalacion,
                    "accion": "modificar"
                }
                try:
                    respuesta = requests.post(URL_GALGA, json=datos)
                    if respuesta.status_code == 200:
                        messagebox.showinfo("Éxito", "La galga se modificó correctamente.")
                        ventana_modificar_galga.destroy()
                    else:
                        messagebox.showerror("Error", f"Error en la modificación: {respuesta.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
            else:
                messagebox.showwarning("Advertencia", "Completa todos los campos.")

    tk.Button(ventana_modificar_galga, text="Guardar Cambios", command=enviar_modificacion_galga, font=("Arial", 12), bg="#e6e6e6", relief=tk.RAISED).pack(pady=20)

def eliminar_galga():
    galgas = obtener_galgas()
    if not galgas:
        messagebox.showwarning("Advertencia", "No hay galgas disponibles para eliminar.")
        return

    ventana_eliminar_galga = tk.Toplevel(ventana)
    ventana_eliminar_galga.title("Eliminar Galga")
    ventana_eliminar_galga.geometry("400x200")
    ventana_eliminar_galga.config(bg="#f0f0f0")

    tk.Label(ventana_eliminar_galga, text="Seleccione una Galga para Eliminar:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
    galga_seleccionada = tk.StringVar()
    opciones_galgas = [f"{g['idGalga']} - {g['ubicacion']}" for g in galgas]
    menu_galgas = tk.OptionMenu(ventana_eliminar_galga, galga_seleccionada, *opciones_galgas)
    menu_galgas.pack(pady=5)

    def confirmar_eliminacion_galga():
        seleccion = galga_seleccionada.get()
        if seleccion:
            id_galga = seleccion.split(" - ")[0]
            confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar esta galga?")
            if confirmacion:
                datos = {
                    "id_galga": id_galga,
                    "accion": "eliminar"
                }
                try:
                    respuesta = requests.post(URL_GALGA, json=datos)
                    if respuesta.status_code == 200:
                        messagebox.showinfo("Éxito", "La galga se eliminó correctamente.")
                        ventana_eliminar_galga.destroy()
                    else:
                        messagebox.showerror("Error", f"Error al eliminar la galga: {respuesta.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione una galga.")

    tk.Button(ventana_eliminar_galga, text="Eliminar", command=confirmar_eliminacion_galga, font=("Arial", 12), bg="#e6e6e6", relief=tk.RAISED).pack(pady=20)

def mostrar_galga():
    galgas = obtener_galgas()
    if not galgas:
        messagebox.showwarning("Advertencia", "No hay galgas disponibles.")
        return
    ventana_mostrar_galgas = tk.Toplevel(ventana)
    ventana_mostrar_galgas.title("Listado de Galgas")
    ventana_mostrar_galgas.geometry("315x450")
    ventana_mostrar_galgas.config(bg="#f8f9fa")

    frame_contenido = tk.Frame(ventana_mostrar_galgas, bg="#f8f9fa")
    frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    titulo = tk.Label(frame_contenido, text="Listado de Galgas", font=("Arial", 14, "bold"), bg="#f8f9fa")
    titulo.pack(pady=5)

    canvas = tk.Canvas(frame_contenido, bg="#f8f9fa", highlightthickness=0, width=290, height=350)
    scroll_y = tk.Scrollbar(frame_contenido, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f8f9fa")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    for galga in galgas:
        frame_galga = tk.Frame(scrollable_frame, bg="#e9ecef", bd=1, relief="solid")
        frame_galga.pack(fill="x", pady=5, padx=5)

        tk.Label(frame_galga, text=f"ID: {galga['idGalga']}", font=("Arial", 11, "bold"), bg="#e9ecef").pack(anchor="w", padx=10, pady=2)
        tk.Label(frame_galga, text=f"Ubicación: {galga['ubicacion']}", font=("Arial", 11), bg="#e9ecef").pack(anchor="w", padx=10)
        tk.Label(frame_galga, text=f"Fecha de Instalación: {galga['fecha_instalacion']}", font=("Arial", 11), bg="#e9ecef").pack(anchor="w", padx=10)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="left", fill="y")
#-----------------------------------------------------------------------------------------------------------------------
def obtener_datos():
    try:
        respuesta = requests.get(URL_DATOS)
        if respuesta.status_code == 200:
            return respuesta.json()  
        else:
            messagebox.showerror("Error", f"Error al obtener datos: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
    return []

def modificar_dato():
    datos = obtener_datos()
    if not datos:
        messagebox.showwarning("Advertencia", "No hay datos disponibles para modificar.")
        return

    ventana_modificar_dato = tk.Toplevel(ventana)
    ventana_modificar_dato.title("Modificar Dato")
    ventana_modificar_dato.geometry("400x400")
    ventana_modificar_dato.config(bg="#f8f9fa")

    tk.Label(ventana_modificar_dato, text="Modificar Dato", font=("Arial", 14, "bold"), bg="#f8f9fa").pack(pady=10)

    tk.Label(ventana_modificar_dato, text="Seleccione el Dato:", bg="#f8f9fa", font=("Arial", 12)).pack(pady=5)
    dato_seleccionado = tk.StringVar()
    opciones_datos = [
        f"{p['idDato']} - Cos Taylor: {p['Cos_Taylor']} - Cos Trig: {p['Cos_Trig']} - Error: {p['Error']} - Fecha: {p['fecha_hora']}"
        for p in datos
    ]
    menu_datos = tk.OptionMenu(ventana_modificar_dato, dato_seleccionado, *opciones_datos)
    menu_datos.pack(pady=5)

    tk.Label(ventana_modificar_dato, text="Nuevo valor Taylor:", bg="#f8f9fa", font=("Arial", 12)).pack(pady=5)
    entrada_taylor = tk.Entry(ventana_modificar_dato, font=("Arial", 12))
    entrada_taylor.pack(pady=5)

    tk.Label(ventana_modificar_dato, text="Nuevo valor Trig:", bg="#f8f9fa", font=("Arial", 12)).pack(pady=5)
    entrada_trig = tk.Entry(ventana_modificar_dato, font=("Arial", 12))
    entrada_trig.pack(pady=5)

    tk.Label(ventana_modificar_dato, text="Nuevo valor Error:", bg="#f8f9fa", font=("Arial", 12)).pack(pady=5)
    entrada_error = tk.Entry(ventana_modificar_dato, font=("Arial", 12))
    entrada_error.pack(pady=5)

    datos_actuales = {"Cos_Taylor": "", "Cos_Trig": "", "Error": ""}

    def cargar_datos_dato(*args):
        seleccion = dato_seleccionado.get()
        if seleccion:
            id_dato = seleccion.split(" - ")[0]
            dato = next((p for p in datos if str(p['idDato']) == id_dato), None)
            if dato:
                datos_actuales["Cos_Taylor"] = dato["Cos_Taylor"]
                datos_actuales["Cos_Trig"] = dato["Cos_Trig"]
                datos_actuales["Error"] = dato["Error"]

                entrada_taylor.delete(0, tk.END)
                entrada_taylor.insert(0, datos_actuales["Cos_Taylor"])

                entrada_trig.delete(0, tk.END)
                entrada_trig.insert(0, datos_actuales["Cos_Trig"])

                entrada_error.delete(0, tk.END)
                entrada_error.insert(0, datos_actuales["Error"])

    dato_seleccionado.trace("w", cargar_datos_dato)

    def enviar_modificacion_dato():
        seleccion = dato_seleccionado.get()
        if seleccion:
            id_dato = seleccion.split(" - ")[0]
            nuevo_taylor = entrada_taylor.get() or datos_actuales["Cos_Taylor"]
            nuevo_trig = entrada_trig.get() or datos_actuales["Cos_Trig"]
            nuevo_error = entrada_error.get() or datos_actuales["Error"]

            datos_modificados = {
                "id_dato": id_dato,
                "nuevo_taylor": nuevo_taylor,
                "nuevo_trig": nuevo_trig,
                "nuevo_error": nuevo_error,
                "accion": "modificar"
            }
            try:
                respuesta = requests.post(URL_DATOS, json=datos_modificados)
                if respuesta.status_code == 200:
                    messagebox.showinfo("Éxito", "El dato se modificó correctamente.")
                    ventana_modificar_dato.destroy()
                else:
                    messagebox.showerror("Error", f"Error en la modificación: {respuesta.status_code}")
            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un dato.")

    tk.Button(ventana_modificar_dato, text="Guardar Cambios", command=enviar_modificacion_dato, font=("Arial", 12), bg="#e6e6e6", relief=tk.RAISED).pack(pady=20)

def eliminar_dato():
    datos = obtener_datos()
    if not datos:
        messagebox.showwarning("Advertencia", "No hay datos disponibles para eliminar.")
        return

    ventana_eliminar_dato = tk.Toplevel(ventana)
    ventana_eliminar_dato.title("Eliminar Dato")
    ventana_eliminar_dato.geometry("400x300")
    ventana_eliminar_dato.config(bg="#f8f9fa")

    tk.Label(ventana_eliminar_dato, text="Eliminar Dato", font=("Arial", 14, "bold"), bg="#f8f9fa").pack(pady=10)

    tk.Label(ventana_eliminar_dato, text="Seleccione el Dato a Eliminar:", bg="#f8f9fa", font=("Arial", 12)).pack(pady=5)
    dato_seleccionado = tk.StringVar()
    opciones_datos = [
        f"{p['idDato']} - Cos Taylor: {p['Cos_Taylor']} - Cos Trig: {p['Cos_Trig']} - Error: {p['Error']} - Fecha: {p['fecha_hora']}"
        for p in datos
    ]
    menu_datos = tk.OptionMenu(ventana_eliminar_dato, dato_seleccionado, *opciones_datos)
    menu_datos.pack(pady=10)

    def confirmar_eliminacion_dato():
        seleccion = dato_seleccionado.get()
        if seleccion:
            id_dato = seleccion.split(" - ")[0]
            confirmacion = messagebox.askyesno("Confirmación", "¿Está seguro de que desea eliminar este dato?")
            if confirmacion:
                datos_a_enviar = {
                    "id_dato": id_dato,
                    "accion": "eliminar"
                }
                try:
                    respuesta = requests.post(URL_DATOS, json=datos_a_enviar)
                    if respuesta.status_code == 200:
                        messagebox.showinfo("Éxito", "El dato se eliminó correctamente.")
                        ventana_eliminar_dato.destroy()
                    else:
                        messagebox.showerror("Error", f"Error al eliminar el dato: {respuesta.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un dato.")

    tk.Button(ventana_eliminar_dato, text="Eliminar", command=confirmar_eliminacion_dato, font=("Arial", 12), bg="#e6e6e6", relief=tk.RAISED).pack(pady=20)

def mostrar_dato():
    datos = obtener_datos()
    if not datos:
        messagebox.showwarning("Advertencia", "No hay datos para mostrar.")
        return

    ventana_mostrar_datos = tk.Toplevel(ventana)
    ventana_mostrar_datos.title("Listado de Datos")
    ventana_mostrar_datos.geometry("315x450")
    ventana_mostrar_datos.config(bg="#f8f9fa")

    frame_contenido = tk.Frame(ventana_mostrar_datos, bg="#f8f9fa")
    frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)

    titulo = tk.Label(frame_contenido, text="Listado de Datos", font=("Arial", 14, "bold"), bg="#f8f9fa")
    titulo.pack(pady=5)

    canvas = tk.Canvas(frame_contenido, bg="#f8f9fa", highlightthickness=0, width=290, height=350)
    scroll_y = tk.Scrollbar(frame_contenido, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f8f9fa")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    for dato in datos:
        frame_dato = tk.Frame(scrollable_frame, bg="#e9ecef", bd=1, relief="solid", padx=5, pady=5)
        frame_dato.pack(fill="x", pady=5)

        tk.Label(frame_dato, text=f"ID: {dato['idDato']}", font=("Arial", 11, "bold"), bg="#e9ecef").pack(anchor="w")
        tk.Label(frame_dato, text=f"Cos Taylor: {dato['Cos_Taylor']}", font=("Arial", 11), bg="#e9ecef").pack(anchor="w", padx=10)
        tk.Label(frame_dato, text=f"Cos Trig: {dato['Cos_Trig']}", font=("Arial", 11), bg="#e9ecef").pack(anchor="w", padx=10)
        tk.Label(frame_dato, text=f"Error: {dato['Error']}", font=("Arial", 11), bg="#e9ecef").pack(anchor="w", padx=10)
        tk.Label(frame_dato, text=f"Fecha Hora: {dato['fecha_hora']}", font=("Arial", 11), bg="#e9ecef").pack(anchor="w", padx=10)
        tk.Label(frame_dato, text=f"idGalga: {dato['idGalga']}", font=("Arial", 11), bg="#e9ecef").pack(anchor="w", padx=10)

    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

#-----------------------------------------------------------------------------------------------------------------------
def abrir_ventana_puente():
    ventana_puente = tk.Toplevel(ventana)
    ventana_puente.title("Opciones de Puente")
    ventana_puente.geometry("300x250")
    ventana_puente.config(bg="#f0f0f0")
    ventana_puente.resizable(False, False)
    # Definir estilo de los botones
    button_style = {
        "font": ("Arial", 12),
        "bg": "#e6e6e6",
        "relief": tk.RAISED,
        "bd": 2,
        "width": 15,
        "height": 2
    }
    
    botones = [
        ("Agregar Puente", datos_puente),
        ("Modificar Puente", modificar_puente),
        ("Eliminar Puente", eliminar_puente),
        ("Mostrar Puente", mostrar_puente)
    ]
    for i, (text, command) in enumerate(botones):
        tk.Button(ventana_puente, text=text, command=command, **button_style).place(relx=0.5, rely=0.2 + i * 0.2, anchor="center")

def abrir_ventana_galga():
    ventana_galga = tk.Toplevel(ventana)
    ventana_galga.title("Opciones de Galga")
    ventana_galga.geometry("300x250")
    ventana_galga.config(bg="#f0f0f0")
    ventana_galga.resizable(False, False)
    # Definir estilo de los botones
    button_style = {
        "font": ("Arial", 12),
        "bg": "#e6e6e6",
        "relief": tk.RAISED,
        "bd": 2,
        "width": 15,
        "height": 2
    }
    
    botonesg = [
        ("Agregar Galga", datos_galga),
        ("Modificar Galga", modificar_galga),
        ("Eliminar Galga", eliminar_galga),
        ("Mostrar Galga", mostrar_galga)
    ]
    for i, (text, command) in enumerate(botonesg):
        tk.Button(ventana_galga, text=text, command=command, **button_style).place(relx=0.5, rely=0.2 + i * 0.2, anchor="center")


def abrir_ventana_datos():
    ventana_datos = tk.Toplevel(ventana)
    ventana_datos.title("Opciones de Datos")
    ventana_datos.geometry("300x250")
    ventana_datos.resizable(False, False)
    # Definir estilo de los botones
    button_style = {
        "font": ("Arial", 12),
        "bg": "#e6e6e6",
        "relief": tk.RAISED,
        "bd": 2,
        "width": 15,
        "height": 2
    }
    
    botonesd = [
        ("Modificar Dato", modificar_dato),
        ("Eliminar Dato", eliminar_dato),
        ("Mostrar Dato", mostrar_dato)
    ]
    for i, (text, command) in enumerate(botonesd):
        tk.Button(ventana_datos, text=text, command=command, **button_style).place(relx=0.5, rely=0.2 + i * 0.2, anchor="center")
# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Interfaz ABM")
ventana.geometry("300x250")
ventana.config(bg="#f0f0f0")
ventana.resizable(False, False)
# Definir estilo de los botones
button_style = {
    "font": ("Arial", 12, "bold"),
    "bg": "#e6e6e6",
    "relief": tk.RAISED,
    "bd": 2,
    "width": 15,
    "height": 2
}
# Colocar los botones centrados en la ventana principal
tk.Button(ventana, text="Puente", command=abrir_ventana_puente, **button_style).place(relx=0.5, rely=0.25, anchor="center")
tk.Button(ventana, text="Galga", command=abrir_ventana_galga, **button_style).place(relx=0.5, rely=0.5, anchor="center")
tk.Button(ventana, text="Datos", command=abrir_ventana_datos, **button_style).place(relx=0.5, rely=0.75, anchor="center")
ventana.mainloop()
