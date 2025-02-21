import base64
import json
import os
import sys
import time

import requests
from pdf2image import convert_from_path

# Ollama API Spec:
# https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion


OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
OLLAMA_API_MODEL_TAGS_URL = OLLAMA_API_URL + "/api/tags"
OLLAMA_API_GENERATE_URL = OLLAMA_API_URL + "/api/generate"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == "__main__":
    # Vision models: can handle both images and text. They accept images as input and can describe, analyze, or reason
    # about their content
    model = os.getenv("OLLAMA_MODEL", "llama3.2-vision:11b")

    response = requests.get(OLLAMA_API_MODEL_TAGS_URL)
    response.raise_for_status()

    supported_model_names = [model["name"] for model in response.json()["models"]]

    if model not in supported_model_names:
        print(
            f"Model {model} is not supported. Supported models: {supported_model_names}"
        )
        sys.exit(1)

    file_path = os.getenv("FILE_PATH", "data/eMediplan_de.pdf")

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

    Format the information found in the input document as a JSON object with the following structure:
    {
        "prescription": {
            "issueDate": "",
        },
        "prescribingDoctor": {
            "academicTitle": "",
            "givenName": "",
            "familyName": "",
            "medicalPracticeName": "",
            "addressLine": "",
            "zsrNumber": "",
            "gln": ""
        },
        "patient": {
            "givenName": "",
            "familyName": "",
            "birthDate": "",
            "sex": "",
            "addressLine": "",
            "postalCode": "",
            "city": ""
        },
        "medication": [
            {
                "prescribedQuantity": "",
                "name": "",
                "unit": "",
                "intakeInstruction": "",
                "remark": ""
            }
        ]
    }

    Some additional information about patterns and numbers expected in the input document:

    The prescriptions issue date (issueDate) is in the format DD.MM.YYYY.


    The prescribing doctor's academic title (academicTitle) is a string.
    Example: Dr. med. dent.

    The prescribing doctor's GLN (gln) is a 13-digit number that uniquely identifies a company or part of a company worldwide.

    The prescribing doctor's ZSR number (zsrNumber) is a 7-digit number.
    Example: A123456 (compact), A 1234.56 (extended)


    The patients birth date (birthDate) is in the format DD.MM.YYYY.

    The patients postal code (postalCode) and the city (city) are related to each other.
    The postal code format is a number with 4 digits.


    The medicaments are often listend in tabular form in the input document.

    The medicament intake instruction (intakeInstruction) instruct the patient how to take the medication.
    The instructions refer to daytime signs such as morning, noon, evening and night.
    The format of the intake instruction in German is
     - Mo (short form for German Morgen) for English morning
     - Mi (short form for German Mittag) for English midday
     - Ab (short form for German Abends) for English evening
     - Na (short form for German zur Nacht) for English night
    For each time of day, a numerical value defines how much of a medication a patient must take.
    Blank in the medication table means 0 (zero) units.

    The short format is 0-0-0-0.

    An example would be 1-0-0.5-0.
    This means one unit in the morning, 0.5 unit in the evening.

    If the intake instruction found does not match the specified format, the information should be returned as remark (remark).
    """

    prompt = instruction + details

    print(f"Prompt: {prompt}")
    print(f"Processing file: {file_path}")
    print(f"Model: {model}")
    print(f"Number of images (PDF pages): {len(images_base64)}")

    payload = {"model": model, "prompt": prompt, "images": images_base64}

    print(f"Calling model {model} @ {OLLAMA_API_URL}...")
    start_time = time.time()
    response = requests.post(OLLAMA_API_GENERATE_URL, json=payload)
    end_time = time.time()
    response.raise_for_status()

    call_duration = end_time - start_time
    print(f"Call duration: {call_duration} seconds")

    ndjson_data = [json.loads(line) for line in response.text.splitlines()]

    tokens = [x["response"] for x in ndjson_data]
    response = "".join(tokens)

    print(f"Response: {response}")
