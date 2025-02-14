import requests
import base64
import json
from pdf2image import convert_from_path
import os

# Ollama API Spec:
# https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion


OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == "__main__":
    # Vision models: can handle both images and text. They accept images as input and can describe, analyze, or reason
    # about their content
    model = os.getenv("OLLAMA_MODEL", "llama3.2-vision:11b")

    file_path = os.getenv("FILE_PATH")

    if not file_path:
        raise Exception("mandatory FILE_PATH environment variable is not set")

    # PDF to image
    pdf_page_images = convert_from_path(file_path, dpi=300)
    images_base64 = []
    for i, image in enumerate(pdf_page_images):
        file_name = f"tmp/page_{i + 1}.png"
        image.save(file_name, "PNG")
        encoded = encode_image(file_name)
        images_base64.append(encoded)

    instruction = """
    You are a health professional, a doctor or a pharmacist.

    Extract all information from this medication plan or medical prescription.

    """

    details = """
    The medical prescription or medication plan can be provided is in German, French or Italian language.

    The result is expected to be in this format:
    {
        "prescribingDoctor": {
            "academicTitle": "",
            "givenName": "",
            "familyName": "",
            "zsrNumber": "",
            "gln": "",
        }
        "patient": {
            "givenName": "",
            "familyName": "",
            "birthDate": "",
            "sex": "",
            "addressLine": "",
            "postalCode": "",
            "city": ""
        }
        "medication": [
            {
                "name": "",
                "unit": "",
                "intakeInstruction: "",
                "remark": ""
            }
        ]
    }

    The patients postal code (postalCode) and the city (city) are related to each other.
    The postal code format is a number with 4 digits.

    The medicament intake instructions instruct the patient how to take the medication.
    The instructions refer to daytime signs such as morning, noon, evening and night.
    The format of the intake instruction in German is
     - Mo (Morgen) for morning
     - Mi (Mittag) for midday
     - Ab (Abends) for evening
     - Na (zur Nacht) for night
    For each time of day, a numerical value defines how much of a medication a patient must take.

    The short format is 0-0-0-0.

    An example would be 1-0-0.5-0.
    This means one unit in the morning, 0.5 unit in the evening.

    If the intake instruction found does not match the specified format, the information should be returned as remark.
    """

    prompt = instruction + details

    print("Model: {}".format(model))
    print("Prompt: {}".format(prompt))
    print("Nubmer of images (pages): {}".format(len(images_base64)))

    payload = {"model": model, "prompt": prompt, "images": images_base64}

    print("Calling model {}...".format(model))
    response = requests.post(OLLAMA_API_URL, json=payload, verify=False)
    response.raise_for_status()

    ndjson_data = [json.loads(line) for line in response.text.splitlines()]

    tokens = [x["response"] for x in ndjson_data]
    response = "".join(tokens)

    print("Response: {}".format(response))
