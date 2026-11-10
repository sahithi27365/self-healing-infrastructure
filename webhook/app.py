

from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route("/alert", methods=["POST"])
def receive_alert():
    data = request.json or {}

    for alert in data.get("alerts", []):
        name = alert.get("labels", {}).get("alertname")
        status = alert.get("status")

        print(f"Received alert: {name}, Status: {status}", flush=True)

        if status == "firing" and name in [
            "NginxDown",
            "NginxExporterDown"
        ]:
            print("Starting Ansible recovery...", flush=True)

            result = subprocess.run(
                ["ansible-playbook", "/ansible/restart_nginx.yml"],
                capture_output=True,
                text=True
            )

            print(result.stdout, flush=True)
            print(result.stderr, flush=True)

            if result.returncode != 0:
                return jsonify({"error": result.stderr}), 500

            print("Automatic recovery completed!", flush=True)

    return jsonify({"message": "Alert processed"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)



