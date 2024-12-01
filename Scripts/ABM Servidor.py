from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# PHP Backend URLs
URL_PUENTE = "http://192.168.1.206/infrasense-IOT/Scripts/puente.php"
URL_GALGA = "http://192.168.1.206/infrasense-IOT/Scripts/galga.php"
URL_DATOS = "http://192.168.1.206/infrasense-IOT/Scripts/datos.php"

# Routes
@app.route("/")
def index():
    return render_template("abm.html")

@app.route("/puente", methods=["POST", "GET"])
def puente():
    if request.method == "POST":
        data = request.json
        response = requests.post(URL_PUENTE, json=data)
        return jsonify({"status": response.status_code, "response": response.json()})
    else:
        id_puente = request.args.get("id_puente")
        if id_puente:
            response = requests.get(URL_PUENTE, params={"id_puente": id_puente})
        else:
            response = requests.get(URL_PUENTE)
        return jsonify(response.json())

@app.route("/galga", methods=["POST", "GET"])
def galga():
    if request.method == "POST":
        data = request.json
        response = requests.post(URL_GALGA, json=data)
        return jsonify({"status": response.status_code, "response": response.json()})
    else:
        id_galga = request.args.get("id_galga")
        if id_galga:
            response = requests.get(URL_GALGA, params={"id_galga": id_galga})
        else:
            response = requests.get(URL_GALGA)
        return jsonify(response.json())

@app.route("/datos_de_lectura", methods=["POST", "GET"])
def datos():
    if request.method == "POST":
        data = request.json
        response = requests.post(URL_DATOS, json=data)
        return jsonify({"status": response.status_code, "response": response.json()})
    else:
        id_dato = request.args.get("id_dato")
        if id_dato:
            response = requests.get(URL_DATOS, params={"idDato": id_dato}) 
        else:
            response = requests.get(URL_DATOS)
        return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
