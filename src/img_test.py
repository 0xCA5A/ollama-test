import requests
import base64
import os
import json


OLLAMA_API_URL = "http://localhost:11434/api/generate"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == "__main__":
    file_path = os.getenv("FILE_PATH")

    if not file_path:
        raise Exception("mandatory FILE_PATH environment variable is not set")

    image_base64 = encode_image(file_path)

    model = "llava:34b"
    prompt = """
    Describe this image. What can you see?
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
