import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"

if __name__ == "__main__":
    model = "llama3.2:3b"
    prompt = """
    Youre master Yoda from Star Wars. 
    
    What ist the GIL in Python used for?
    """

    payload = {"model": model, "prompt": prompt, "stream": False}

    print("Model: {}".format(model))
    print("Prompt: {}".format(prompt))

    response = requests.post(OLLAMA_API_URL, json=payload)

    print("Raw ollama response:\n", response.text)

    print(
        "Response: {}".format(response.json().get("response", "No response generated."))
    )
