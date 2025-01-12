import os
import cohere

# Initialize the Cohere client using ClientV2

co = cohere.ClientV2("FfzfGriLQELxRINyB2dBDsWxFgEetEeIu3fcjhbA")

# Set up Google Cloud Vision credentials (Ensure the path is correct)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Backend/stoked-energy-447522-h9-283c4b94d4b9.json'

def detect_labels(path):
    """Detects labels in the file using Google Cloud Vision API."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    detected_labels = [label.description.lower() for label in labels]

    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )

    return detected_labels

def create_cohere_prompt(labels, user_input):
    """Creates a structured prompt for Cohere to classify a job."""
    prompt = (
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
    return prompt

def send_prompt_to_cohere(prompt):
    """Sends the generated prompt to Cohere for classification."""
    try:
        response = co.chat(
            model="command-r-plus",  
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract and return the assistant's message correctly
        if response.message and response.message.content:
            return response.message.content[0].text.strip()
        else:
            raise Exception("No valid response received from Cohere.")
    except Exception as e:
        return f"An error occurred: {e}"

# ✅ Example usage combining both functions
path1 = 'Backend/image1.jpeg'
user_text = input("Describe the problem in your own words: ")

try:
    # Step 1: Detect labels from the image using Google Cloud Vision
    labels1 = detect_labels(path1)
    print("Labels for photo1:", labels1)

    # Step 2: Create a structured prompt for Cohere
    prompt1 = create_cohere_prompt(labels1, user_text)

    # Step 3: Send the prompt to Cohere and get the classification
    cohere_response = send_prompt_to_cohere(prompt1)
    print("Cohere's Response:", cohere_response)

except Exception as e:
    print("An error occurred:", e)