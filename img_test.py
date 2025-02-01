import requests
import base64

OLLAMA_API_URL = "http://localhost:11434/api/generate"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == "__main__":
    image_path = "bug.jpg"
    image_base64 = encode_image(image_path)

    model = "llava:34b"
    prompt = """
    Youre master Yoda from Start Wars.
    
    Describe this image. What can you see?
    """

    payload = {"model": model, "prompt": prompt, "image": image_base64}

    response = requests.post(OLLAMA_API_URL, json=payload)

    prompt = """
    How many bugs can you see in this picture?
    """

    payload = {"model": model, "prompt": prompt, "image": image_base64}

    response = requests.post(OLLAMA_API_URL, json=payload)

    print(response.json())
