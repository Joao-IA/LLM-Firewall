import requests, json


def ollama_generate(prompt):
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": "llama3.1",  
        "prompt": prompt
    }

    response = requests.post(url, json=data, stream=True)

    if response.status_code == 200:
        full_response = ""
        try:
            for line in response.iter_lines():
                if line:
                    json_response = json.loads(line.decode('utf-8'))
                    full_response += json_response["response"]
                    if json_response.get("done"):
                        break
            return full_response
        except json.JSONDecodeError:
            raise Exception(f"Failed to parse JSON response: {response.text}")
    else:
        raise Exception(f"Failed to generate text: {response.text}")


#print(ollama_generate("Era uma vez um"))