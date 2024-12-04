from flask import Blueprint, Flask, render_template, jsonify
import pandas as pd
import numpy as np  # Importamos numpy para cálculos numéricos
from sqlalchemy import create_engine

userDashboard_bp = Blueprint('userDashboard', __name__, template_folder='templates')

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'iot',
    'password': '',
    'database': 'puentesdb'
}

# Crear conexión con SQLAlchemy
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

@userDashboard_bp.route('/')
def user_dashboard():
    # Obtener la lista de galgas
    query_galgas = "SELECT DISTINCT idGalga FROM datos_de_lectura"
    galgas = pd.read_sql(query_galgas, engine)['idGalga'].tolist()

    # Obtener los puentes y sus galgas asociadas con sus datos de esfuerzo
    query_puentes_galgas = """
    SELECT puente.idPuente, puente.nombre, galga.idGalga, datos_de_lectura.peso
    FROM puente
    LEFT JOIN galga ON galga.idPuente = puente.idPuente
    LEFT JOIN datos_de_lectura ON datos_de_lectura.idGalga = galga.idGalga
    ORDER BY puente.idPuente
    """
    puentes_galgas = pd.read_sql(query_puentes_galgas, engine)

    # Convertir a un formato JSON serializable
    puentes = []
    for (idPuente, nombre), group in puentes_galgas.groupby(['idPuente', 'nombre']):
        galgas_puente = group['idGalga'].dropna().astype(int).unique().tolist()
        # Calcular el esfuerzo total del puente (suma de los pesos de sus galgas)
        esfuerzo_total = group['peso'].sum()
        galgas_info = []
        for idGalga in galgas_puente:
            # Calcular el esfuerzo de la galga (suma de sus pesos)
            esfuerzo_galga = group[group['idGalga'] == idGalga]['peso'].sum()
            # Calcular el porcentaje de esfuerzo
            if esfuerzo_total > 0:
                porcentaje_esfuerzo = (esfuerzo_galga / esfuerzo_total) * 100
            else:
                porcentaje_esfuerzo = 0
            porcentaje_esfuerzo = round(porcentaje_esfuerzo, 2)

            # Determinar el riesgo basado en el porcentaje de esfuerzo
            if porcentaje_esfuerzo <= 10:
                riesgo = 'Buenas Condiciones'
            elif porcentaje_esfuerzo <= 30:
                riesgo = 'Necesita Mantenimiento'
            else:
                riesgo = 'Peligro'

            galgas_info.append({
                'idGalga': int(idGalga),  # Convertir a int para asegurar serialización
                'porcentaje_esfuerzo': porcentaje_esfuerzo,
                'riesgo': riesgo
            })
        puente = {
            'idPuente': int(idPuente),  # Convertir a int para asegurar serialización
            'nombre': nombre,
            'galgas': galgas_info
        }
        puentes.append(puente)

    return render_template('usuario.html', galgas=galgas, puentes=puentes)

@userDashboard_bp.route('/api/puentes')
def get_puentes():
    # Obtener los puentes y sus galgas asociadas con sus datos de esfuerzo
    query_puentes_galgas = """
    SELECT puente.idPuente, puente.nombre, galga.idGalga, datos_de_lectura.peso
    FROM puente
    LEFT JOIN galga ON galga.idPuente = puente.idPuente
    LEFT JOIN datos_de_lectura ON datos_de_lectura.idGalga = galga.idGalga
    ORDER BY puente.idPuente
    """
    puentes_galgas = pd.read_sql(query_puentes_galgas, engine)

    # Convertir a un formato JSON serializable
    puentes = []
    for (idPuente, nombre), group in puentes_galgas.groupby(['idPuente', 'nombre']):
        galgas_puente = group['idGalga'].dropna().astype(int).unique().tolist()
        # Calcular el esfuerzo total del puente (suma de los pesos de sus galgas)
        esfuerzo_total = group['peso'].sum()
        galgas_info = []
        for idGalga in galgas_puente:
            # Calcular el esfuerzo de la galga (suma de sus pesos)
            esfuerzo_galga = group[group['idGalga'] == idGalga]['peso'].sum()
            # Calcular el porcentaje de esfuerzo
            if esfuerzo_total > 0:
                porcentaje_esfuerzo = (esfuerzo_galga / esfuerzo_total) * 100
            else:
                porcentaje_esfuerzo = 0
            porcentaje_esfuerzo = round(porcentaje_esfuerzo, 2)

            # Determinar el riesgo basado en el porcentaje de esfuerzo
            if porcentaje_esfuerzo <= 10:
                riesgo = 'Buenas Condiciones'
            elif porcentaje_esfuerzo <= 30:
                riesgo = 'Necesita Mantenimiento'
            else:
                riesgo = 'Peligro'

            galgas_info.append({
                'idGalga': int(idGalga),  # Convertir a int para asegurar serialización
                'porcentaje_esfuerzo': porcentaje_esfuerzo,
                'riesgo': riesgo
            })
        puente = {
            'idPuente': int(idPuente),  # Convertir a int para asegurar serialización
            'nombre': nombre,
            'galgas': galgas_info
        }
        puentes.append(puente)

    return jsonify(puentes)