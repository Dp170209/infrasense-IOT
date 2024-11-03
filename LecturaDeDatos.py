import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Configuración de la base de datos
db_config = {
    'host': 'localhost',       # Cambia esto si tu servidor MySQL está en otra dirección
    'user': 'root',            # Cambia esto por tu nombre de usuario MySQL
    'password': '',            # Cambia esto por tu contraseña MySQL
    'database': 'puentesdb'    # Usando la base de datos puentesdb
}

# Crear conexión con SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

# Obtener todos los puentes únicos junto con sus nombres de la base de datos
query_puentes = "SELECT DISTINCT puente.idPuente, puente.nombre FROM galga JOIN puente ON galga.idPuente = puente.idPuente"
puentes = pd.read_sql(query_puentes, engine)

# Generar un gráfico para cada puente
for _, row in puentes.iterrows():
    id_puente = row['idPuente']
    nombre_puente = row['nombre']
    
    # Consulta SQL para leer los datos de un puente específico
    query = f"""
    SELECT datos_de_lectura.fecha_hora, datos_de_lectura.Cos_Taylor, datos_de_lectura.Cos_Trig, datos_de_lectura.Error, datos_de_lectura.idGalga, galga.idPuente
    FROM datos_de_lectura
    JOIN galga ON datos_de_lectura.idGalga = galga.idGalga
    WHERE galga.idPuente = {id_puente}
    ORDER BY datos_de_lectura.fecha_hora
    """
    data = pd.read_sql(query, engine)
    
    # Verificar que hay datos para este puente
    if data.empty:
        print(f"No se encontraron datos para el puente {nombre_puente}.")
        continue

    # Crear el gráfico para el puente actual
    fig = plt.figure(figsize=(14, 8))
    
    # Filtrar por cada galga y trazar sus datos
    for id_galga in data['idGalga'].unique():
        galga_data = data[data['idGalga'] == id_galga]
        
        # Graficar Cos_Taylor
        plt.plot(galga_data['fecha_hora'], galga_data['Cos_Taylor'], label=f'Galga {id_galga} - Cos Taylor', linestyle='-')
        # Graficar Cos_Trig
        plt.plot(galga_data['fecha_hora'], galga_data['Cos_Trig'], label=f'Galga {id_galga} - Cos Trig', linestyle='--')
        # Graficar Error
        plt.plot(galga_data['fecha_hora'], galga_data['Error'], label=f'Galga {id_galga} - Error', linestyle=':')

    # Configuración del gráfico
    plt.title(f'Datos de Galgas para Puente {nombre_puente}')
    plt.xlabel('Fecha y Hora')
    plt.ylabel('Valores')
    plt.legend(title='ID de Galga y Tipo de Dato', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()

# Gráfico comparativo de Cos_Taylor entre puentes
fig = plt.figure(figsize=(14, 8))

# Bucle para cada puente y calcular el promedio de Cos_Taylor por marca de tiempo
for _, row in puentes.iterrows():
    id_puente = row['idPuente']
    nombre_puente = row['nombre']
    
    # Consulta SQL para obtener datos de Cos_Taylor para el puente específico
    query = f"""
    SELECT datos_de_lectura.fecha_hora, AVG(datos_de_lectura.Cos_Taylor) as avg_Cos_Taylor, galga.idPuente
    FROM datos_de_lectura
    JOIN galga ON datos_de_lectura.idGalga = galga.idGalga
    WHERE galga.idPuente = {id_puente}
    GROUP BY datos_de_lectura.fecha_hora
    ORDER BY datos_de_lectura.fecha_hora
    """
    data = pd.read_sql(query, engine)
    
    # Verificar que hay datos para este puente
    if data.empty:
        print(f"No se encontraron datos para el puente {nombre_puente}.")
        continue

    # Graficar la línea promedio de Cos_Taylor para este puente
    plt.plot(data['fecha_hora'], data['avg_Cos_Taylor'], label=f'Puente {nombre_puente}')

# Configuración del gráfico comparativo
plt.title('Comparativa de Cos Taylor Promedio entre Puentes')
plt.xlabel('Fecha y Hora')
plt.ylabel('Cos Taylor Promedio')
plt.legend(title='Nombre del Puente')
plt.grid(True)
plt.tight_layout()

# Gráfico de Líneas de Tendencia Agregado para Cada Métrica
# Consulta para calcular los promedios de Cos_Taylor, Cos_Trig y Error en el tiempo
query_tendencia = """
SELECT datos_de_lectura.fecha_hora,
       AVG(datos_de_lectura.Cos_Taylor) as avg_Cos_Taylor,
       AVG(datos_de_lectura.Cos_Trig) as avg_Cos_Trig,
       AVG(datos_de_lectura.Error) as avg_Error
FROM datos_de_lectura
GROUP BY datos_de_lectura.fecha_hora
ORDER BY datos_de_lectura.fecha_hora
"""
data_tendencia = pd.read_sql(query_tendencia, engine)

# Crear el gráfico de líneas de tendencia
plt.figure(figsize=(14, 8))
plt.plot(data_tendencia['fecha_hora'], data_tendencia['avg_Cos_Taylor'], label='Cos Taylor Promedio', color='blue')
plt.plot(data_tendencia['fecha_hora'], data_tendencia['avg_Cos_Trig'], label='Cos Trig Promedio', color='orange', linestyle='--')  # Línea segmentada
plt.plot(data_tendencia['fecha_hora'], data_tendencia['avg_Error'], label='Error Promedio', color='red')

# Configuración del gráfico de líneas de tendencia
plt.title('Tendencias de Cos Taylor, Cos Trig y Error Promedio a lo Largo del Tiempo')
plt.xlabel('Fecha y Hora')
plt.ylabel('Valores Promedio')
plt.legend(title='Métricas')
plt.grid(True)
plt.tight_layout()

# Mostrar todos los gráficos generados
plt.show()


