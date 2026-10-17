from flask import Flask, jsonify, render_template
import os
import platform
import socket
import time
import psutil

app = Flask(__name__)
START_TIME = time.time()

def get_metrics():
    try:
        disk_path = os.path.abspath(os.sep)
        disk = psutil.disk_usage(disk_path)
    except Exception:
        disk = psutil.disk_usage(os.getcwd())

    memory = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=0.15)
    boot_time = psutil.boot_time()

    return {
        "hostname": socket.gethostname(),
        "platform": platform.platform(),
        "cpu_percent": round(cpu, 1),
        "cpu_count": psutil.cpu_count(logical=True) or 1,
        "memory": {
            "percent": round(memory.percent, 1),
            "used_gb": round(memory.used / (1024 ** 3), 2),
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "available_gb": round(memory.available / (1024 ** 3), 2)
        },
        "disk": {
            "percent": round(disk.percent, 1),
            "used_gb": round(disk.used / (1024 ** 3), 2),
            "total_gb": round(disk.total / (1024 ** 3), 2),
            "free_gb": round(disk.free / (1024 ** 3), 2)
        },
        "uptime_seconds": max(0, int(time.time() - boot_time)),
        "app_uptime_seconds": max(0, int(time.time() - START_TIME)),
        "timestamp": int(time.time())
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/metrics")
def api_metrics():
    return jsonify(get_metrics())

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=False)
