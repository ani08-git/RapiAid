import requests

def ask_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma3:1b",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )

        print("Status:", response.status_code)
        print("Response:", response.text)

        data = response.json()
        return data.get("response", "No response from Ollama")

    except Exception as e:
        return f"Error: {str(e)}"