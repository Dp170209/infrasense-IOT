from flask import Flask, render_template, redirect, url_for
from ABMServidor import abm_bp

app = Flask(__name__, static_folder="static", template_folder="templates")

# Registrar Blueprints con prefijos
app.register_blueprint(abm_bp, url_prefix="/abm")

@app.route("/")
def index():
    # Redirige a la ruta "/abm"
    return redirect(url_for("abm"))

@app.route("/abm")
def abm():
    return render_template("abm.html")

if __name__ == "__main__":
    app.run(debug=True)
