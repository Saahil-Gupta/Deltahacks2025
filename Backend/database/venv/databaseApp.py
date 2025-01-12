from flask import Flask, request, jsonify
from pymongo import MongoClient
from google.cloud import vision
from dotenv import load_dotenv
import cohere
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MongoDB connection string not found in environment variables.")
client = MongoClient(MONGO_URI)
db = client["hackathon_db"]
collection = db["service_providers"]

# Cohere API initialization
#COHERE_API_KEY = os.getenv("FfzfGriLQELxRINyB2dBDsWxFgEetEeIu3fcjhbA")
#if not COHERE_API_KEY:
#    raise ValueError("Cohere API key not found in environment variables.")
co = cohere.ClientV2("FfzfGriLQELxRINyB2dBDsWxFgEetEeIu3fcjhbA")

# Google Cloud Vision credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'stoked-energy-447522-h9-283c4b94d4b9.json'

def detect_labels(image_path):
    """Detects labels in the uploaded image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)

    if response.error.message:
        raise Exception(f"Google Vision API error: {response.error.message}")

    labels = [label.description.lower() for label in response.label_annotations]
    return labels

def send_to_cohere(prompt):
    """Sends the prompt to Cohere and gets the response."""
    try:
        response = co.chat(
            model="command-r-plus",
            messages=[{"role": "user", "content": prompt}]
        )
        # Extract and return the assistant's response
        if response.message and response.message.content:
            return response.message.content[0].text.strip()
        else:
            raise Exception("No valid response received from Cohere.")
    except Exception as e:
        return f"An error occurred: {e}"

@app.route("/", methods=["GET", "POST"])
def find_service_providers():
    if request.method == "GET":
        return '''
        <form action="/" method="post" enctype="multipart/form-data">
            <label for="user_input">Describe your problem:</label>
            <input type="text" id="user_input" name="user_input" required>
            <br><br>
            <label for="image">Upload an image:</label>
            <input type="file" id="image" name="image" accept="image/*" required>
            <br><br>
            <button type="submit">Submit</button>
        </form>
        '''

    if request.method == "POST":
        # Get user input
        user_input = request.form.get("user_input")
        image = request.files.get("image")

        if not user_input or not image:
            return "<h2>Error: Please provide both a description and an image.</h2>"

        # Save the uploaded image temporarily
        image_path = image.filename
        image.save(image_path)

        try:
            # Detect labels using Google Cloud Vision
            labels = detect_labels(image_path)
            print("Detected Labels:", labels)

            # Create Cohere prompt
            cohere_prompt = (
                "You are a helpful assistant tasked with categorizing a job request into one of the following categories: \n"
                "1. Plumber \n"
                "2. Carpenter \n"
                "3. Mechanic \n"
                "4. Electrician \n"
                "0. Undecided \n"
                "\n"
                f"Detected Labels: {', '.join(labels)}\n"
                f"User Input: {user_input}\n"
                "\n"
                "Respond with the number corresponding to the most suitable category."
            )

            # Get response from Cohere
            cohere_response = send_to_cohere(cohere_prompt)

            # Extract the service name from the response (remove the number)
            service = cohere_response.split(". ", 1)[-1].strip().lower()

            # Query the database for matching service providers
            providers = list(collection.find({"service": {"$regex": service, "$options": "i"}}, {"_id": 0}))

            if not providers:
                return f"<h2>No matching service providers found for: {service.capitalize()}.</h2>"

            # Display the results
            response = f"<h1>Number of service providers for '{service.capitalize()}': {len(providers)}</h1><br>"
            for idx, provider in enumerate(providers, start=1):
                person_details = " | ".join(
                    [f"<b>{field.capitalize()}:</b> {value}" for field, value in provider.items()]
                )
                response += f"Person {idx}: {person_details}<br>"

            return response

        except Exception as e:
            return f"<h2>An error occurred: {e}</h2>"

if __name__ == "__main__":
    app.run(debug=True)
