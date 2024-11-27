from flask import Flask, render_template, jsonify
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': '192.168.0.26',
    'user': 'root',
    'password': '',
    'database': 'puentesdb'
}

# Crear conexión con SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

@app.route('/')
def index():
    # Obtener la lista de galgas y puentes
    query_galgas = "SELECT DISTINCT idGalga FROM datos_de_lectura"
    query_puentes = "SELECT DISTINCT puente.idPuente, puente.nombre FROM galga JOIN puente ON galga.idPuente = puente.idPuente"
    galgas = pd.read_sql(query_galgas, engine)['idGalga'].tolist()
    puentes = pd.read_sql(query_puentes, engine)
    return render_template('index.html', galgas=galgas, puentes=puentes.to_dict(orient='records'))

@app.route('/api/galga/<int:id_galga>')
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

@app.route('/api/galgas')
def get_all_galgas():
    # Datos de todas las galgas
    query = """
    SELECT fecha_hora, peso, idGalga
    FROM datos_de_lectura
    ORDER BY fecha_hora
    """
    data = pd.read_sql(query, engine)
    return jsonify(data.to_dict(orient='records'))

@app.route('/api/puente/<int:id_puente>')
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

@app.route('/api/puentes')
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

@app.route('/api/quiebre/<int:id_puente>')
def simulate_quiebre(id_puente):
    # Simular quiebre para un puente específico
    query = f"""
    SELECT datos_de_lectura.fecha_hora, datos_de_lectura.peso, datos_de_lectura.idGalga
    FROM datos_de_lectura
    JOIN galga ON datos_de_lectura.idGalga = galga.idGalga
    WHERE galga.idPuente = {id_puente}
    ORDER BY datos_de_lectura.fecha_hora
    """
    data = pd.read_sql(query, engine)
    if not data.empty:
        data['peso_quiebre'] = data['peso']
        data.loc[len(data) // 2:, 'peso_quiebre'] *= 10  # Simulación de quiebre
    return jsonify(data.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
