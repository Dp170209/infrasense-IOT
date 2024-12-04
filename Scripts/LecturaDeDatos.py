<<<<<<< HEAD
from flask import Flask, render_template, jsonify
import matplotlib as plt
=======
from flask import Blueprint, Flask, render_template, jsonify
>>>>>>> origin/DominicE
import pandas as pd
import numpy as np  # Importamos numpy para cálculos numéricos
from sqlalchemy import create_engine
dashboard_bp = Blueprint('dashboard', __name__, template_folder='templates')

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
<<<<<<< HEAD
    'user': 'root',
=======
    'user': 'dom',
>>>>>>> origin/DominicE
    'password': '',
    'database': 'puentesdb'
}

# Crear conexión con SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

@dashboard_bp.route('/')
def dashboard_home():
    query_galgas = "SELECT DISTINCT idGalga FROM datos_de_lectura"
    galgas = pd.read_sql(query_galgas, engine)['idGalga'].tolist()

    query_puentes_galgas = """
    SELECT puente.idPuente, puente.nombre, galga.idGalga, datos_de_lectura.peso
    FROM puente
    LEFT JOIN galga ON galga.idPuente = puente.idPuente
    LEFT JOIN datos_de_lectura ON datos_de_lectura.idGalga = galga.idGalga
    ORDER BY puente.idPuente
    """
    puentes_galgas = pd.read_sql(query_puentes_galgas, engine)

    puentes = []
    for (idPuente, nombre), group in puentes_galgas.groupby(['idPuente', 'nombre']):
        galgas_puente = group['idGalga'].dropna().astype(int).unique().tolist()
        esfuerzo_total = group['peso'].sum()
        galgas_info = []
        for idGalga in galgas_puente:
            esfuerzo_galga = group[group['idGalga'] == idGalga]['peso'].sum()
            if esfuerzo_total > 0:
                porcentaje_esfuerzo = (esfuerzo_galga / esfuerzo_total) * 100
            else:
                porcentaje_esfuerzo = 0
            porcentaje_esfuerzo = round(porcentaje_esfuerzo, 2)
            if porcentaje_esfuerzo <= 10:
                riesgo = 'Buenas Condiciones'
            elif porcentaje_esfuerzo <= 30:
                riesgo = 'Necesita Mantenimiento'
            else:
                riesgo = 'Peligro'

            galgas_info.append({
                'idGalga': int(idGalga),
                'porcentaje_esfuerzo': porcentaje_esfuerzo,
                'riesgo': riesgo
            })
        puente = {
            'idPuente': int(idPuente),
            'nombre': nombre,
            'galgas': galgas_info
        }
        puentes.append(puente)

    return render_template('dashboard.html', galgas=galgas, puentes=puentes)

# Rutas API existentes
@dashboard_bp.route('/api/galga/<int:id_galga>')
def get_galga_data(id_galga):
    # Datos para una galga específica
    query = f"""
    SELECT fecha_hora, peso
    FROM datos_de_lectura
    WHERE idGalga = {id_galga}
    ORDER BY fecha_hora
    """
    data = pd.read_sql(query, engine)
    return jsonify(data.to_dict(orient='records'))

@dashboard_bp.route('/api/galgas')
def get_all_galgas():
    # Datos de todas las galgas
    query = """
    SELECT fecha_hora, peso, idGalga
    FROM datos_de_lectura
    ORDER BY fecha_hora
    """
    data = pd.read_sql(query, engine)
    return jsonify(data.to_dict(orient='records'))

@dashboard_bp.route('/api/puente/<int:id_puente>')
def get_puente_data(id_puente):
    # Datos para un puente específico
    query = f"""
    SELECT datos_de_lectura.fecha_hora, datos_de_lectura.peso, datos_de_lectura.idGalga
    FROM datos_de_lectura
    JOIN galga ON datos_de_lectura.idGalga = galga.idGalga
    WHERE galga.idPuente = {id_puente}
    ORDER BY datos_de_lectura.fecha_hora
    """
    data = pd.read_sql(query, engine)
    return jsonify(data.to_dict(orient='records'))

@dashboard_bp.route('/api/puentes')
def get_all_puentes():
    # Datos de todas las galgas y puentes
    query = """
    SELECT datos_de_lectura.fecha_hora, datos_de_lectura.peso, datos_de_lectura.idGalga, galga.idPuente
    FROM datos_de_lectura
    JOIN galga ON datos_de_lectura.idGalga = galga.idGalga
    ORDER BY datos_de_lectura.fecha_hora
    """
    data = pd.read_sql(query, engine)
    return jsonify(data.to_dict(orient='records'))

@dashboard_bp.route('/api/quiebre/<int:id_puente>')
def simulate_quiebre(id_puente):
    # Datos para un puente específico
    query = f"""
    SELECT datos_de_lectura.fecha_hora, datos_de_lectura.peso, datos_de_lectura.idGalga
    FROM datos_de_lectura
    JOIN galga ON datos_de_lectura.idGalga = galga.idGalga
    WHERE galga.idPuente = {id_puente}
    ORDER BY datos_de_lectura.fecha_hora
    """
    data = pd.read_sql(query, engine)
    if not data.empty:
        # Ordenar los datos por fecha y resetear el índice
        data = data.sort_values('fecha_hora').reset_index(drop=True)
        n = len(data)
        # Definir los puntos de segmentación
        idx1 = int(n * 0.4)
        idx2 = int(n * 0.5)
        idx3 = int(n * 0.6)

        # Crear una copia del peso original
        data['peso_quiebre'] = data['peso'].copy()

        # Segmento 1: Añadir pequeñas perturbaciones
        np.random.seed(0)
        perturbaciones = np.random.normal(0, data['peso'].std() * 0.01, size=idx1)
        data.loc[:idx1-1, 'peso_quiebre'] += perturbaciones

        # Segmento 2: Aumento lineal hasta la máxima tensión
        max_tension = data['peso'].max() * 1.05  # 5% más que el máximo original
        incremento = (max_tension - data.loc[idx1, 'peso_quiebre']) / (idx2 - idx1)
        data.loc[idx1:idx2, 'peso_quiebre'] = data.loc[idx1:idx2, 'peso_quiebre'] + incremento * np.arange(0, idx2 - idx1 + 1)

        # Segmento 3: Arco que sobrepasa el máximo
        arco_altura = data['peso'].max() * 0.1  # 10% más alto que max_tension
        arco = arco_altura * np.sin(np.linspace(0, np.pi, idx3 - idx2 + 1))
        data.loc[idx2:idx3, 'peso_quiebre'] = max_tension + arco

        # Segmento 4: Descenso en escalones hasta cero
        escalones = np.linspace(data.loc[idx3, 'peso_quiebre'], 0, n - idx3)
        data.loc[idx3:, 'peso_quiebre'] = escalones

<<<<<<< HEAD
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/deformacion_por_ubicacion/<int:id_puente>')
def deformacion_por_ubicacion(id_puente):
    # Consulta para obtener el peso total de cada galga agrupado por ubicación, filtrado por puente
    query = f"""
    SELECT galga.ubicacion, SUM(datos_de_lectura.peso) as peso_total
    FROM galga
    JOIN datos_de_lectura ON galga.idGalga = datos_de_lectura.idGalga
    WHERE galga.idPuente = {id_puente}
    GROUP BY galga.ubicacion
    """
    data = pd.read_sql(query, engine)
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/grafica_barras_apiladas')
def grafica_barras_apiladas():
    try:
        # Obtener los datos de los puentes y sus galgas
        query = """
        SELECT puente.nombre AS puente, galga.ubicacion, AVG(datos_de_lectura.peso) AS promedio_peso
        FROM datos_de_lectura
        JOIN galga ON datos_de_lectura.idGalga = galga.idGalga
        JOIN puente ON galga.idPuente = puente.idPuente
        GROUP BY puente.nombre, galga.ubicacion
        ORDER BY puente.nombre
        """
        df = pd.read_sql(query, engine)

        # Transformar los datos para el gráfico apilado
        pivot_df = df.pivot(index='puente', columns='ubicacion', values='promedio_peso').fillna(0)
        data = []

        for column in pivot_df.columns:
            data.append({
                'label': column,
                'data': pivot_df[column].tolist()
            })

        response_data = {
            'labels': pivot_df.index.tolist(),
            'datasets': data
        }

        return jsonify(response_data)

    except Exception as e:
        print(f"Error al generar la gráfica de barras apiladas: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
=======
    return jsonify(data.to_dict(orient='records'))
>>>>>>> origin/DominicE
