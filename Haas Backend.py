# HAAS - Honeypot-as-a-Service Backend API

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
import datetime

app = Flask(__name__)

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/haas"
mongo = PyMongo(app)

db_attacks = mongo.db.attacks

def log_attack(ip, port, protocol, payload):
    db_attacks.insert_one({
        "ip": ip,
        "port": port,
        "protocol": protocol,
        "payload": payload,
        "timestamp": datetime.datetime.utcnow()
    })

@app.route("/log", methods=["POST"])
def log_event():
    data = request.json
    log_attack(data["ip"], data["port"], data["protocol"], data.get("payload", ""))
    return jsonify({"message": "Attack logged"}), 201

@app.route("/attacks", methods=["GET"])
def get_attacks():
    attacks = db_attacks.find().sort("timestamp", -1)
    return dumps(attacks)

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Backend is running"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
