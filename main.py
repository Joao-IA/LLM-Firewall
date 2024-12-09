import re
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from ollama import ollama_generate
import spacy

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

#Como se fossem os usuários autorizados

USUARIOS = {
    "admin": generate_password_hash("senha123")
}

def mascarar_ner(texto):
    doc = nlp(texto)
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG']:
            texto = texto.replace(ent.text, f"[{ent.label_}]")
    return texto


def mascarar_dados(texto):
    texto = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', texto)
    texto = re.sub(r'\b\d{3}[-.\s]??\d{2}[-.\s]??\d{4}\b', '[PHONE]', texto)
    texto = re.sub(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b', '[CPF]', texto)
    texto = re.sub(r'\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b', '[CNPJ]', texto)
    return texto

#pipeline llm
# llm_pipe = pipeline()

@app.route('/query', methods=['POST'])
def query_llm():
    auth = request.authorization
    if not auth:
        return jsonify({"message": "No authentication provided"}), 401
    if not check_password_hash(USUARIOS.get(auth.username), auth.password):
        return jsonify({"message": "Unauthorized"}), 401
    
    #Entrada do Usuário
    input_usuario = request.json.get('input', '')
    
    #dlp
    input_filtrado = mascarar_dados(input_usuario)
    
    #processamento do llm
    #llm_response = llm_pipe(input_filtrado, max_length=50)[0]['generated_text']
    
    #DLP saida
    #output_filtrado = mascarar_dados(llm_response)
    
    llm_response = ollama_generate(input_filtrado)
    
    output_filtrado = mascarar_dados(llm_response)
    
    return jsonify({"input": input_filtrado,
                    "output": output_filtrado})



if __name__ == '__main__':
    app.run(debug=True)