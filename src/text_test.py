import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"

if __name__ == "__main__":
    model = "llama3.2:3b"
    prompt = """
    You are master Yoda from Star Wars.
    
    What is the Python GIL?
    """

    payload = {"model": model, "prompt": prompt, "stream": False}

    print("Model: {}".format(model))
    print("Prompt: {}".format(prompt))

    print("Calling model...")
    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()

    if response.status_code != 200:
        raise Exception("Unexpected response from ollama: {}".format(response))

    print("Raw ollama response:\n", response.text)

    print(
        "Response: {}".format(response.json().get("response", "No response generated."))
    )
