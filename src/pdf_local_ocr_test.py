import requests
import json
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

# Ollama API Spec:
# https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion


OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")


if __name__ == "__main__":
    model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

    file_path = os.getenv("FILE_PATH")

    if not file_path:
        raise Exception("mandatory FILE_PATH environment variable is not set")

    # PDF to image
    images = convert_from_path(file_path, dpi=300)
    for i, image in enumerate(images):
        image.save(f"tmp/page_{i + 1}.png", "PNG")

    image = Image.open("tmp/page_1.png")

    # Get text output
    text = pytesseract.image_to_string(image)
    # Get HOCR output
    # hocr = repr( pytesseract.image_to_pdf_or_hocr(image, extension='hocr'))
    # Get ALTO XML output
    # alto = repr(pytesseract.image_to_alto_xml(image))

    instruction = f"""
    You are a health professional, a doctor or a pharmacist.

    Extract all information from this medication plan or medical prescription from this input: 

    [INPUT]

    {text}

    [END_INPUT]

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
    print("Input file: {}".format(file_path))

    payload = {"model": model, "prompt": prompt}

    print("Calling model...")
    response = requests.post(OLLAMA_API_URL, json=payload, verify=False)
    response.raise_for_status()

    ndjson_data = [json.loads(line) for line in response.text.splitlines()]

    tokens = [x["response"] for x in ndjson_data]
    response = "".join(tokens)

    print("Response: {}".format(response))
