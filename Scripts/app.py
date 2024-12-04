from flask import Flask, render_template, redirect, url_for
from ABMServidor import abm_bp
from register import register_bp
from login import login_bp
from LecturaDeDatos import dashboard_bp
from UsuarioDash import userDashboard_bp
from datetime import timedelta
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

app.config['SECRET_KEY'] = 'clave'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

# Registrar Blueprints con prefijos
app.register_blueprint(abm_bp, url_prefix="/abm")
app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(register_bp, url_prefix='/register')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(userDashboard_bp, url_prefix='/userDashboard')

@app.route("/")
def index():
    return redirect(url_for("home"))

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/abm")
def abm():
    return render_template("abm.html")

if __name__ == "__main__":
    app.run(debug=True)