from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import mysql.connector
import hashlib

register_bp = Blueprint('register', __name__)

db_config = {
    'host': 'localhost',
    'user': 'iot',
    'password': '',
    'database': 'puentesdb'
}

# Configuración de conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Ruta para el registro (renderiza el formulario)
@register_bp.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Generar y enviar el código de verificación
        code = generate_verification_code()

        # Enviar el código al correo del usuario
        if send_verification_email(email, code):
            session['verification_code'] = code
            session['email'] = email
            session['password'] = password  # Guardar la contraseña temporalmente (para el registro final)
            return jsonify({"success": True, "message": "Código de verificación enviado al correo."})
        else:
            return jsonify({"success": False, "message": "Error al enviar el correo. Intenta de nuevo."})
    else:
        return render_template('register.html')  # Renderiza el formulario en GET

# Ruta para verificar el código de verificación
@register_bp.route('/verify_code', methods=['POST'])
def verify_code():
    data = request.get_json()
    entered_code = data.get('code')

    if 'verification_code' in session and entered_code == session['verification_code']:
        email = session.get('email')
        password = session.get('password')

        # Generar el rol basado en el dominio del correo
        role = get_role_from_email(email)

        # Insertar el usuario en la base de datos
        if register_user(email, password, role):
            print(f"Usuario registrado con el correo: {email} y rol: {role}")
            return jsonify({"success": True, "message": "Registro completado."})
        else:
            return jsonify({"success": False, "message": "Error al registrar el usuario en la base de datos."})

    else:
        return jsonify({"success": False, "message": "Código incorrecto. Intenta de nuevo."})

# Función para generar un código de verificación aleatorio
def generate_verification_code():
    return str(random.randint(100000, 999999))

# Función para enviar el código de verificación por correo electrónico
def send_verification_email(to_email, code):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    gmail_user = "chiques170209@gmail.com"  # Tu dirección de correo
    gmail_password = "scqb iztc imfr mgdz"  # Usa la contraseña o la de aplicación si tienes 2 pasos activados

    # Configurar el mensaje
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = "Código de Verificación"

    body = f"Tu código de verificación es: {code}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Conectar al servidor SMTP de Gmail
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Seguridad para encriptar la conexión
        server.login(gmail_user, gmail_password)  # Autenticación
        text = msg.as_string()
        server.sendmail(gmail_user, to_email, text)  # Enviar el correo
        server.quit()  # Cerrar la conexión SMTP
        print("Correo enviado con éxito")
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

# Función para obtener el rol según el dominio del correo
def get_role_from_email(email):
    domain = email.split('@')[1]
    if domain == 'ucb.edu.bo':
        return 1
    else:
        return 2

# Función para registrar al usuario en la base de datos
def register_user(email, password, role):
    # Conectar a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Consulta SQL para insertar el usuario en la base de datos
    query = """
        INSERT INTO usuario (correo, password, rol)
        VALUES (%s, %s, %s)
    """
    try:
        cursor.execute(query, (email, hashed_password, role))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al registrar el usuario: {e}")
        conn.rollback()
        conn.close()
        return False