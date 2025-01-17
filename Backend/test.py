import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Backend/stoked-energy-447522-h9-283c4b94d4b9.json'


def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print("Labels:")

    for label in labels:
        print(label.description)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )



# print(detect_labels('photo1.jpg'))
print("New!!!!!!!")
print(detect_labels('image2.jpg'))