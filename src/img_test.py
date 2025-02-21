import base64
import json
import os
import requests

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

    file_path = os.getenv("FILE_PATH", "data/bug.jpg")

    if not file_path:
        raise Exception("mandatory FILE_PATH environment variable is not set")

    image_base64 = encode_image(file_path)

    prompt = """
    Describe this image. What can you see?
    """

    print("Model: {}".format(model))
    print("Prompt: {}".format(prompt))
    print("Input file: {}".format(file_path))

    payload = {"model": model, "prompt": prompt, "images": [image_base64]}

    print("Calling model...")
    response = requests.post(OLLAMA_API_GENERATE_URL, json=payload)
    response.raise_for_status()

    ndjson_data = [json.loads(line) for line in response.text.splitlines()]

    tokens = [x["response"] for x in ndjson_data]
    response = "".join(tokens)

    print("Response: {}".format(response))
