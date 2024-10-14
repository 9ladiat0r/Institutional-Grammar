import PyPDF2
import requests
import json
import os

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

def ollama_api_request(text):
    url = "http://localhost:11434/api/generate"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # Replace with your actual API key
        "Content-Type": "application/json"
    }
    payload = {
        "text": text  # Sending the extracted text to the API
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()  # Parse the response
    else:
        raise Exception(f"API Request failed with status code {response.status_code}")
    
def generate(model_name, prompt, system=None, template=None, context=None, options=None, callback=None):
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model_name, 
            "prompt": prompt, 
            "system": system, 
            "template": template, 
            "context": context, 
            "options": options
        }
        
        # Remove keys with None values
        payload = {k: v for k, v in payload.items() if v is not None}
        
        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()
            
            # Creating a variable to hold the context history of the final chunk
            final_context = None
            
            # Variable to hold concatenated response strings if no callback is provided
            full_response = ""

            # Iterating over the response line by line and displaying the details
            for line in response.iter_lines():
                if line:
                    # Parsing each line (JSON chunk) and extracting the details
                    chunk = json.loads(line)
                    
                    # If a callback function is provided, call it with the chunk
                    if callback:
                        callback(chunk)
                    else:
                        # If this is not the last chunk, add the "response" field value to full_response and print it
                        if not chunk.get("done"):
                            response_piece = chunk.get("response", "")
                            full_response += response_piece
                            print(response_piece, end="", flush=True)
                    
                    # Check if it's the last chunk (done is true)
                    if chunk.get("done"):
                        final_context = chunk.get("context")
            
            # Return the full response and the final context
            return full_response, final_context
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None


def final_output(prompt: str, model="llama3.1", metadata={}):
    SYS_PROMPT = (
        "Your task is to give the most apt heading for the entire text. Answer should be a single sentence in less than 10 words. "
    )
    
    try:
        response, _ = generate(model_name=model, system=SYS_PROMPT, prompt=prompt)
        
        result = json.loads(response)
        result = [dict(item, **metadata) for item in result]
    except Exception as e:
        print(f"\n\nERROR ### Here is the buggy response: {response}\nError: {e}\n\n")
        result = None
    
    return result


# Example of extracting text and sending it to Ollama API
if __name__ == "__main__":
    pdf_file_path = "/Users/karan/Desktop/3-1/LOP/acts/The Air (Prevention and Control of Pollution) Act of 1981.pdf"
    text = extract_text_from_pdf(pdf_file_path)
    print(type(text))
    result = final_output(text)
    print(result)