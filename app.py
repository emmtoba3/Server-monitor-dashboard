from flask import Flask, jsonify, render_template
import psutil
import socket
import time

app = Flask(__name__)

boot_time = psutil.boot_time()

def format_uptime(seconds):
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    return f"{days}d {hours}h {minutes}m"

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "No disponible"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/metrics")
def metrics():
    uptime_seconds = time.time() - boot_time

    return jsonify({
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(interval=1),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "status": "Activo",
        "ip": get_local_ip(),
        "uptime": format_uptime(uptime_seconds)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
