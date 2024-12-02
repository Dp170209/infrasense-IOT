from flask import Flask, render_template
from ABMServidor import abm_bp

app = Flask(__name__)

# Registrar Blueprints con prefijos
app.register_blueprint(abm_bp, url_prefix="/abm")


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/abm")
def abm():
    return render_template("abm.html")

@app.route("/prinicpal")
def principal():
    return render_template("principal.html")

if __name__ == "__main__":
    app.run(debug=True)
