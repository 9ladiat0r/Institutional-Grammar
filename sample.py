import requests
import json

def query_ollama(prompt, model="llama3.1"):
    url = 

    payload = {
        "model": model,
        "prompt": prompt
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
def main():
    result = query_ollama("Explain the concept of recursion in programming.")
    print(result)

if __name__ == "__main__":
    main()