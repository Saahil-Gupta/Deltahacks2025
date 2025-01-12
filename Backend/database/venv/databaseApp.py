from flask import Flask, request, render_template_string
from pymongo import MongoClient
from google.cloud import vision
from dotenv import load_dotenv
import cohere
import os
import re

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
        print("Sending prompt to Cohere:", prompt)
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


HTML_TEMPLATE =""" <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Support Request</title>
    <style>
        /* CSS Section */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
        }
        
        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #f5f5f5;
            padding: 20px;
        }

        .container {
            width: 100%;
            max-width: 600px;
        }

        .header {
            text-align: center;
            margin-bottom: 32px;
        }

        .header h1 {
            color: #1a1a1a;
            font-size: 24px;
            margin-bottom: 8px;
        }

        .header p {
            color: #666;
            font-size: 16px;
        }

        form {
            background: white;
            padding: 32px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .form-group {
            margin-bottom: 24px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            color: #1a1a1a;
            font-weight: 500;
            font-size: 14px;
        }

        input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            font-size: 16px;
            transition: all 0.2s ease;
            background: #fafafa;
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #2563eb;
            background: white;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }

        .upload-area {
            border: 2px dashed #e0e0e0;
            border-radius: 8px;
            padding: 24px;
            text-align: center;
            transition: all 0.2s ease;
            cursor: pointer;
        }

        .upload-area:hover {
            border-color: #2563eb;
            background: rgba(37, 99, 235, 0.02);
        }

        .upload-area.dragover {
            border-color: #2563eb;
            background: rgba(37, 99, 235, 0.05);
        }

        input[type="file"] {
            display: none;
        }

        .upload-icon {
            color: #666;
            font-size: 24px;
            margin-bottom: 12px;
        }

        .upload-text {
            color: #666;
            margin-bottom: 8px;
        }

        .upload-hint {
            color: #888;
            font-size: 14px;
        }

        .file-preview {
            display: none;
            margin-top: 16px;
            padding: 12px;
            background: #f8fafc;
            border-radius: 6px;
            font-size: 14px;
        }

        .file-preview.active {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .file-info {
            flex-grow: 1;
        }

        .file-name {
            color: #1a1a1a;
            font-weight: 500;
            margin-bottom: 4px;
        }

        .file-size {
            color: #666;
            font-size: 12px;
        }

        .remove-file {
            color: #ef4444;
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            border: 1px solid #ef4444;
            background: transparent;
            transition: all 0.2s ease;
        }

        .remove-file:hover {
            background: #fef2f2;
        }

        button[type="submit"] {
            width: 100%;
            padding: 12px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        button[type="submit"]:hover {
            background: #1d4ed8;
        }

        button[type="submit"]:disabled {
            background: #93c5fd;
            cursor: not-allowed;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Submit a Support Request</h1>
            <p>Please describe your issue and attach any relevant screenshots</p>
        </div>

        <form action="/" method="post" enctype="multipart/form-data" id="supportForm">
            <div class="form-group">
                <label for="user_input">Issue Description*</label>
                <input 
                    type="text" 
                    id="user_input" 
                    name="user_input" 
                    required
                    placeholder="Describe what's happening..."
                >
            </div>

            <div class="form-group">
                <label for="image">Attachment</label>
                <div class="upload-area" id="uploadArea">
                    <div class="upload-icon">📎</div>
                    <div class="upload-text">Click here to browse files</div>
                    <div class="upload-hint">Supported formats: PNG, JPG, GIF (max 5MB)</div>
                    <input 
                        type="file" 
                        id="image" 
                        name="image" 
                        accept="image/*"
                    >
                </div>
                <div class="file-preview" id="filePreview">
                    <div class="file-info">
                        <div class="file-name" id="fileName"></div>
                        <div class="file-size" id="fileSize"></div>
                    </div>
                    <button type="button" class="remove-file" id="removeFileButton">Remove</button>
                </div>
            </div>

            <button type="submit" id="submitButton">Submit Request</button>
        </form>
    </div>

    <script>
        // JavaScript Section
        const uploadArea = document.getElementById("uploadArea");
        const fileInput = document.getElementById("image");
        const filePreview = document.getElementById("filePreview");
        const fileName = document.getElementById("fileName");
        const fileSize = document.getElementById("fileSize");
        const removeFileButton = document.getElementById("removeFileButton");
        const submitButton = document.getElementById("submitButton");

        uploadArea.addEventListener("click", () => fileInput.click());

        fileInput.addEventListener("change", (e) => {
            const file = e.target.files[0];
            handleFile(file);
        });

        removeFileButton.addEventListener("click", () => {
            filePreview.classList.remove("active");
            fileInput.value = "";
            submitButton.disabled = false;
        });

        function handleFile(file) {
            if (file) {
                const fileSizeInMB = (file.size / (1024 * 1024)).toFixed(2);
                if (fileSizeInMB > 5) {
                    alert("File size exceeds 5MB limit!");
                    return;
                }

                fileName.textContent = file.name;
                fileSize.textContent = `Size: ${fileSizeInMB} MB`;
                filePreview.classList.add("active");

                // Create a new DataTransfer object to simulate file input
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(file);

                // Attach the file to the file input
                fileInput.files = dataTransfer.files;
            }
        }
    </script>
</body>
</html>"""



@app.route("/", methods=["GET", "POST"])
def find_service_providers():
    if request.method == "GET":
        return render_template_string(HTML_TEMPLATE)

    if request.method == "POST":
        # Get user input
        user_input = request.form.get("user_input")
        image = request.files.get("image")

        if not user_input or not image:
            return "<h2>Error: Please provide both a description and an image.</h2>"

        # Validate file type
        ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' not in image.filename or image.filename.rsplit('.', 1)[-1].lower() not in ALLOWED_EXTENSIONS:
            return "<h2>Error: Unsupported file format. Please upload an image file (PNG, JPG, JPEG, or GIF).</h2>"

        # Validate file size (ensure the file is not too large)
        image.seek(0, os.SEEK_END)  # Move the pointer to the end of the file
        file_size = image.tell()
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
        if file_size > MAX_FILE_SIZE:
            return "<h2>Error: File size exceeds 5MB. Please upload a smaller file.</h2>"

        # Reset file pointer after size check
        image.seek(0)

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
                "Respond first with the number corresponding to the most suitable category. "
                "Then provide a Quick/Temporary Fix for the problem if possible within 5 to 7 bullet points, "
                "each on a new line and with a maximum of 50 words."
            )
            
            service_list = ["Undecided", "Plumber", "Carpenter", "Mechanic", "Electrician"]
            cohere_response = send_to_cohere(cohere_prompt)
            print("Cohere Response:", cohere_response)

            # Parse the response to extract only the Quick Fix section
            response_lines = cohere_response.strip().split("\n")
            quick_fix_lines = response_lines[1:]  # Skip the first line (category number and service name)
            print("Response Lines:", response_lines)
            service = service_list[int(response_lines[0][0])]
            # Join the remaining lines as the quick fix
            quick_fix = "\n".join(line.strip() for line in quick_fix_lines if line.strip())

            print("Quick Fix:", quick_fix)

            # Format the quick fix as HTML bullet points
            fix_html = "<ul>" + "".join([f"<li>{line}</li>" for line in quick_fix.split("\n") if line.strip()]) + "</ul>"

            # Query the database for matching service providers
            providers = list(collection.find({"service": {"$regex": service, "$options": "i"}}, {"_id": 0}).sort("location", 1))

            if not providers:
                return f"""
                    <h2>No matching service providers found.</h2>
                    <h3>Quick Fix:</h3>
                    {fix_html}
                """

            # Display the results
# Generate the response HTML
            response = f"""
                <link rel="stylesheet" href="\\static\\styles.css">
                <div class="container">
                    <div class="quick-fix-section">
                        <h3>Quick Fix Suggestions</h3>
                        {fix_html}
                    </div>

                    <h2 class="section-title">Available Service Providers ({len(providers)})</h2>
            """

            # Generate service cards
            for idx, provider in enumerate(providers, start=1):
                # Create a formatted string of provider details
                details = []
                for field, value in provider.items():
                    if field not in ['_id']:  # Skip MongoDB ID field
                        details.append(f"<b>{field.capitalize()}:</b> {value}")
                person_details = " | ".join(details)
                
                # Convert the first part of details into a name (use service if name not available)
                provider_name = provider.get('name', provider.get('service', 'Service Provider'))
                
                response += f"""
                    <div class="service-card">
                        <div class="profile-image">
                            <img src="/api/placeholder/100/100" alt="Provider {idx} profile image"/>
                        </div>
                        <div class="provider-info">
                            <h2 class="provider-name">{provider_name}</h2>
                            <p class="provider-occupation">{provider['service']}</p>
                            <div class="provider-details">
                                {person_details}
                            </div>
                        </div>
                        <div class="ratings">
                            <p class="rating-label">Rating</p>
                            <div class="stars" role="img" aria-label="4 out of 5 stars">
                                ★★★★☆
                            </div>
                        </div>
                    </div>
                """

            response += "</div>"  # Close container
            return response
        
        except Exception as e:
            return f"<h2>An error occurred: {e}</h2>"


if __name__ == "__main__":
    app.run(debug=True)
