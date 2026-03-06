from flask import Flask, jsonify, render_template
import psutil
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/metrics")
def metrics():
    return jsonify({
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "status": "Activo"
    })

app.run(host="0.0.0.0", port=5050)