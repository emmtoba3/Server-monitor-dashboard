from flask import Flask, jsonify, render_template
import psutil
import socket
import time
from collections import deque
from datetime import datetime

app = Flask(__name__)

boot_time = psutil.boot_time()

# Guardará las últimas 20 mediciones
history = deque(maxlen=20)

def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{days}d {hours}h {minutes}m"

def collect_metrics():
    uptime_seconds = time.time() - boot_time
    return {
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "status": "Activo",
        "uptime": format_uptime(uptime_seconds),
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/metrics")
def metrics():
    data = collect_metrics()

    history.append({
        "timestamp": data["timestamp"],
        "cpu": data["cpu"],
        "ram": data["ram"],
        "disk": data["disk"]
    })

    return jsonify(data)

@app.route("/history")
def get_history():
    return jsonify(list(history))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=False)
