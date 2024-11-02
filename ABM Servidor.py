import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime  # Importar para obtener la fecha actual

# URL del archivo PHP que se usará para insertar datos en la base de datos
URL = "http://192.168.0.18/ABM.php"  # Cambia esta URL por la de tu servidor

# Función para enviar los datos al servidor mediante una solicitud HTTP POST
def enviar_datos_al_servidor(ubicacion, nombre_puente):
    try:
        datos = {
            "nombre_puente": nombre_puente,
            "ubicacion": ubicacion
        }
        respuesta = requests.post(URL, data=datos)
        
        # Verificar si la solicitud fue exitosa
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
        respuesta = requests.get(URL)
        if respuesta.status_code == 200:
            return respuesta.json()  # Devuelve la lista de puentes en formato JSON
        else:
            messagebox.showerror("Error", f"Error al obtener puentes: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
    return []

# Función para obtener datos de un puente específico
def obtener_datos_puente(id_puente):
    try:
        respuesta = requests.get(URL, params={"id_puente": id_puente})
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            messagebox.showerror("Error", f"Error al obtener datos del puente: {respuesta.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
    return {}

# Función para modificar un puente
def modificar_puente():
    puentes = obtener_puentes()  # Obtener todos los puentes desde el servidor
    
    ventana_modificar = tk.Toplevel(ventana)
    ventana_modificar.title("Modificar Puente")
    ventana_modificar.geometry("400x300")

    tk.Label(ventana_modificar, text="Seleccione un Puente para Modificar:").pack(pady=5)
    
    # Lista desplegable para seleccionar el puente
    puente_seleccionado = tk.StringVar()
    opciones = [f"{p['idPuente']} - {p['nombre']}" for p in puentes]
    menu_puentes = tk.OptionMenu(ventana_modificar, puente_seleccionado, *opciones)
    menu_puentes.pack(pady=5)
    
    # Campos de entrada para editar el puente seleccionado
    tk.Label(ventana_modificar, text="Nuevo Nombre del Puente:").pack(pady=5)
    entrada_nombre = tk.Entry(ventana_modificar)
    entrada_nombre.pack(pady=5)
    
    tk.Label(ventana_modificar, text="Nueva Ubicación:").pack(pady=5)
    entrada_ubicacion = tk.Entry(ventana_modificar)
    entrada_ubicacion.pack(pady=5)
    
    # Valores actuales para referencia
    datos_actuales = {"nombre": "", "ubicacion": ""}

    # Función para cargar datos del puente seleccionado
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

    puente_seleccionado.trace("w", cargar_datos_puente)  # Actualizar datos al seleccionar puente

    # Función que envía la actualización al servidor
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
                    "ubicacion": nueva_ubicacion
                }
                try:
                    respuesta = requests.post(URL, data=datos)
                    if respuesta.status_code == 200:
                        messagebox.showinfo("Éxito", "El puente se modificó correctamente.")
                        ventana_modificar.destroy()
                    else:
                        messagebox.showerror("Error", f"Error en la modificación: {respuesta.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
            else:
                messagebox.showwarning("Advertencia", "Completa todos los campos.")
    
    # Botón para enviar la modificación
    tk.Button(ventana_modificar, text="Guardar Cambios", command=enviar_modificacion).pack(pady=20)

# Función para eliminar un puente
def eliminar_puente():
    puentes = obtener_puentes()  # Obtener todos los puentes desde el servidor
    
    ventana_eliminar = tk.Toplevel(ventana)
    ventana_eliminar.title("Eliminar Puente")
    ventana_eliminar.geometry("400x200")

    tk.Label(ventana_eliminar, text="Seleccione un Puente para Eliminar:").pack(pady=5)
    
    # Lista desplegable para seleccionar el puente
    puente_seleccionado = tk.StringVar()
    opciones = [f"{p['idPuente']} - {p['nombre']}" for p in puentes]
    menu_puentes = tk.OptionMenu(ventana_eliminar, puente_seleccionado, *opciones)
    menu_puentes.pack(pady=5)
    
    # Función que envía la solicitud de eliminación al servidor
    def confirmar_eliminacion():
        seleccion = puente_seleccionado.get()
        if seleccion:
            id_puente = seleccion.split(" - ")[0]
            # Confirmar eliminación
            confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este puente?")
            if confirmacion:
                datos = {
                    "id_puente": id_puente,
                    "accion": "eliminar"
                }
                try:
                    respuesta = requests.post(URL, data=datos)
                    if respuesta.status_code == 200:
                        messagebox.showinfo("Éxito", "El puente se eliminó correctamente.")
                        ventana_eliminar.destroy()
                    else:
                        messagebox.showerror("Error", f"Error al eliminar el puente: {respuesta.status_code}")
                except requests.exceptions.RequestException as e:
                    messagebox.showerror("Error", f"No se pudo conectar con el servidor: {e}")
    
    # Botón para confirmar la eliminación
    tk.Button(ventana_eliminar, text="Eliminar", command=confirmar_eliminacion).pack(pady=20)
    
# Función para mostrar todos los puentes
def mostrar_puente():
    puentes = obtener_puentes()  # Obtener todos los puentes desde el servidor
    
    ventana_mostrar = tk.Toplevel(ventana)
    ventana_mostrar.title("Mostrar Todos los Puentes")
    ventana_mostrar.geometry("400x300")

    # Crear un texto de resumen de todos los puentes
    texto_puentes = tk.Text(ventana_mostrar, wrap="word")
    texto_puentes.insert(tk.END, "Listado de Puentes:\n\n")
    
    for puente in puentes:
        texto_puentes.insert(tk.END, f"ID: {puente['idPuente']}\n")
        texto_puentes.insert(tk.END, f"Nombre: {puente['nombre']}\n")
        texto_puentes.insert(tk.END, f"Ubicación: {puente['ubicacion']}\n")
        texto_puentes.insert(tk.END, "-"*30 + "\n") 
    
    texto_puentes.config(state=tk.DISABLED) 
    texto_puentes.pack(expand=True, fill='both')
    

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
    ventana_galga.geometry("250x200")
    ventana_galga.resizable(False, False)

    for i, text in enumerate(["Agregar Galga", "Modificar Galga", "Eliminar Galga", "Mostrar Galga"]):
        tk.Button(ventana_galga, text=text, width=20).grid(row=i, column=0, padx=20, pady=5)

def abrir_ventana_datos():
    ventana_datos = tk.Toplevel(ventana)
    ventana_datos.title("Opciones de Datos")
    ventana_datos.geometry("250x200")
    ventana_datos.resizable(False, False)

    for i, text in enumerate(["Agregar Dato", "Modificar Dato", "Eliminar Dato", "Mostrar Dato"]):
        tk.Button(ventana_datos, text=text, width=20).grid(row=i, column=0, padx=20, pady=5)

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
