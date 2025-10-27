from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello from GKE CI/CD — Flask!\n"

@app.route('/info')
def info():
    return jsonify({"app":"demo-flask","version":"0.1.0"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
