from openai import OpenAI
from dotenv import load_dotenv
from logs_func import log_event
import os
import json

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
nvidia_api_key = os.getenv("NVIDIA_API_KEY")
base_url = os.getenv("BASE_URL_NVIDIA")
org = os.getenv("ORG")
project = os.getenv("PROJ")


def is_prompt_safe(prompt):

    client = OpenAI(
        base_url=base_url,
        api_key=nvidia_api_key
    )

    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemoguard-8b-content-safety",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "None"}
        ],
        stream=False
    )

    is_safe_json = completion.choices[0].message

    json_res = is_safe_json.content
    json_res = json.loads(json_res)
    is_safe_json = json_res["User Safety"]

    if is_safe_json == "safe":
        return True
    else:
        log_event(f"In: {json_res['Safety Categories']}")
        return (False, json_res["Safety Categories"])


def is_output_safe(response:str):
    
    client = OpenAI(
        base_url=base_url,
        api_key=nvidia_api_key
    )

    completion = client.chat.completions.create(
        model="nvidia/llama-3.1-nemoguard-8b-content-safety",
        messages=[
            {
                "role": "user", 
                "content": "None"
             },
            {
                "role": "assistant", 
                "content": response
                }
        ],
        stream=False
    )    
    
    is_safe_json = completion.choices[0].message
    json_res = is_safe_json.content
    json_res = json.loads(json_res)
    is_safe_json = json_res["Response Safety"]
    
    if is_safe_json == "safe":
        return True
    else:
        log_event(f"Out: {json_res['Safety Categories']}")
        return (False, json_res["Safety Categories"])


def get_openai_response(prompt):
    # Verifica se o prompt é seguro
    safe_check = is_prompt_safe(prompt)

    if safe_check is True:
        
      client = OpenAI(
      organization=org,
      project=project,
      api_key=openai_api_key
      )

      stream = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[{"role": "user", "content": prompt}],
      stream=True,
      )
      
      result = ""
      for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            result += chunk.choices[0].delta.content        

    
    elif isinstance(safe_check, tuple) and safe_check[0] is False:

        raise ValueError(f"Prompt bloqueado: {safe_check[1]}")
    else:
        raise ValueError("Erro ao verificar a segurança do prompt.") 
    
    if is_output_safe(result):
        return result
    else:
        raise ValueError("Resposta bloqueada por conter conteúdo inapropriado.")
