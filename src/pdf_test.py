import requests
import base64
import os
import json
from pdf2image import convert_from_path

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == "__main__":
    file_path = os.getenv("FILE_PATH")

    if not file_path:
        raise Exception("mandatory FILE_PATH environment variable is not set")

    # PDF to image
    images = convert_from_path(file_path, dpi=300)
    for i, image in enumerate(images):
        image.save(f"tmp/page_{i + 1}.png", "PNG")

    image_base64 = encode_image("tmp/page_1.png")

    model = "llama3.2:1b"
    prompt = """
    You are a health professional, a doctor or a pharmacist.

    Can you extract the medication of this medical prescription or medication plan?

    The medical prescription or medication plan can be provided is in German, French or Italian language.

    The result is expected to be in this format:
    {
        prescribingDoctor: {
            academicTitle: "",
            givenName: "",
            familyName: "",
        }
        patient: {
            givenName: "",
            familyName: "",
            addressLine: "",
            postalCode: "",
            city: ""
        }
        medication: [
            {
                "name": "",
                "intakeInstruction: "0-0-0-0"
            }
        ]
    }

    The format of the intake instruction is Mo (Morgen), Mi (Mittag), Ab (Abends), Na (zur Nacht).
    The short format is 0-0-0-0.
    """

    print("Model: {}".format(model))
    print("Prompt: {}".format(prompt))
    print("Input file: {}".format(file_path))

    payload = {"model": model, "prompt": prompt, "image": image_base64}

    print("Calling model...")
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()

    ndjson_data = [json.loads(line) for line in response.text.splitlines()]

    tokens = [x["response"] for x in ndjson_data]
    response = "".join(tokens)

    print("Response: {}".format(response))
