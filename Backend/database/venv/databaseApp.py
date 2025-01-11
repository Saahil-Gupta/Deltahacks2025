from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB connection string from .env file
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MongoDB connection string not found in environment variables.")

client = MongoClient(MONGO_URI)
db = client["hackathon_db"]  # Replace with your database name
collection = db["service_providers"]  # Replace with your collection name

# Home route
@app.route("/")
def home():
    return "Flask and MongoDB are connected!"

# Route to fetch all service providers
@app.route("/service-providers", methods=["GET"])
def get_service_providers():
    providers = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB `_id` field
    return jsonify(providers)

# Route to add a new service provider
@app.route("/service-providers", methods=["POST"])
def add_service_provider():
    data = request.json
    if not data:
        return jsonify({"error": "Request body is missing"}), 400

    # Insert into MongoDB
    collection.insert_one(data)
    return jsonify({"message": "Service provider added successfully!"}), 201

# Route to fetch a service provider by name
@app.route("/service-providers/<name>", methods=["GET"])
def get_service_provider_by_name(name):
    provider = collection.find_one({"name": name}, {"_id": 0})  # Exclude MongoDB `_id` field
    if not provider:
        return jsonify({"error": "Service provider not found"}), 404
    return jsonify(provider)

if __name__ == "__main__":
    app.run(debug=True)
