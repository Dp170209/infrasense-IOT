from flask import Blueprint, render_template, request, flash, session
import mysql.connector
import hashlib

login_bp = Blueprint('login', __name__)

db_config = {
    'host': 'localhost',
    'user': 'dom',
    'password': '',
    'database': 'puentesdb'
}

# Configuración de conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(db_config)

def hash_password(password):
    """Genera el hash de la contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Generar el hash de la contraseña proporcionada por el usuario
        hashed_password = hash_password(password)

        print(hashed_password)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Verificar credenciales con el hash
        query = "SELECT * FROM usuario WHERE correo = %s AND password = %s"
        cursor.execute(query, (email, hashed_password))
        user = cursor.fetchone()

        conn.close()

        if user:
            # Verificar si el usuario es administrador o usuario regular
            if "@ucb.edu.bo" in email:
                user['rol'] = 1  # Asignar rol de administrador si es necesario
            else:
                user['rol'] = 2  # Usuario regular

            # Guardar información del usuario en la sesión
            session['user_id'] = user['idUsuario']
            session['role'] = user['rol']
            session.permanent = True

            return render_template('home.html', logged_in=True)  # Si está autenticado, pasamos logged_in=True
        else:
            flash('Credenciales incorrectas. Intenta nuevamente.')
            print("No")
            return render_template('login.html')

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente.', 'info')
    return render_template('home.html', logged_in=False) 