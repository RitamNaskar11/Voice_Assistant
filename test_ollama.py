import requests

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3.2:3b",
    "prompt": "What is Python? Explain in simple words.",
    "stream": False
}

response = requests.post(url, json=data, timeout=120)

result = response.json()

print(result["response"])