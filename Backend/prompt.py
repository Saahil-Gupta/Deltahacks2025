import os
from cohere_file import co 
from google.cloud import vision

# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Backend/stoked-energy-447522-h9-283c4b94d4b9.json'

def detect_labels(path):
    """Detects labels in the file."""

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    detected_labels = [label.description.lower() for label in labels]

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    return detected_labels

def create_cohere_prompt(labels, user_input):
    """Creates a prompt for Cohere to classify the job based on image labels and user input."""
    prompt = (
        "You are a helpful assistant tasked with categorizing a job request into one of the following categories: \n"
        "1. Plumber \n"
        "2. Carpenter \n"
        "3. Mechanic \n"
        "4. Electrician \n"
        "0. Undecided \n"
        "\n"
        "Given the following detected image labels and user input, determine the most appropriate category:\n"
        f"Detected Labels: {', '.join(labels)}\n"
        f"User Input: {user_input}\n"
        "\n"
        "Respond with the number corresponding to the most suitable category."
    )
    return prompt

def get_cohere_response(prompt):
    """Sends a prompt to Cohere using an existing client instance and returns the response."""
    try:
        response = co.chat(
            model="command-r-plus", 
            messages=[{"role": "user", "content": prompt}]
        )
        return response.reply.strip()
    except Exception as e:
        print("An error occurred while calling Cohere:", e)
        return None

# Example usage
path1 = 'image1.jpeg'
path2 = 'image2.jpeg'
user_text = "I need help fixing my kitchen sink and a leaky faucet."

try:
    labels1 = detect_labels(path1)
    labels2 = detect_labels(path2)

    print("Labels for photo1:", labels1)
    print("Labels for photo2:", labels2)

    prompt1 = create_cohere_prompt(labels1, user_text)
    prompt2 = create_cohere_prompt(labels2, user_text)

    print("Prompt for photo1:", prompt1)
    print("Prompt for photo2:", prompt2)

    # Get Cohere responses
    response1 = get_cohere_response(prompt1)
    response2 = get_cohere_response(prompt2)

    print("Cohere response for photo1:", response1)
    print("Cohere response for photo2:", response2)
except Exception as e:
    print("An error occurred:", e)
