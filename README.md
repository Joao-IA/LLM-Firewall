# Autenticação e Mascaramento de Dados Sensíveis

Esta API em Flask realiza autenticação básica, processa entradas de usuários por meio de um LLM (Large Language Model) e aplica mascaramento de dados sensíveis, como e-mails e números de telefone, utilizando expressões regulares.

---

## **Funcionalidades**

1. ### **Autenticação Básica**
   A API utiliza autenticação com usuário e senha para proteger o endpoint `/query`.  
   
   - **Usuário padrão:** `admin`  
   - **Senha padrão:** `senha123` (armazenada em hash)

2. ### **Mascaramento de Dados Sensíveis**
   Substitui dados sensíveis por tokens:
   
   - **E-mails:** `[EMAIL]`  
   - **Números de telefone:** `[PHONE]`  

3. ### **Processamento com LLM**
   Os dados filtrados são processados por um modelo de linguagem via `ollama_generate`.

---

### **Instalação das Dependências:**

```bash
pip install flask requests jsonify werkzeug
```

#### O Ollama permite o uso dos modelos Llama da Meta via API local, sendo necessária a instalação do [Ollama](https://ollama.com/) para funcionar corretamente.

### Executando uma requisição de exemplo.
```bash
curl -X POST http://127.0.0.1:5000/query -u admin:senha123 -H "Content-Type: application/json" -d "{\"input\": \"Meu email é exemplo@gmail.com e meu telefone é 123-45-6789.\"}"
```

### Obtemos como resposta:

{
  "input": "Meu email \u00e9 [EMAIL] e meu telefone \u00e9 [PHONE].",

  "output": "Desculpe, mas n\u00e3o posso ajudar com pedidos de compartilhar informa\u00e7\u00f5es de contato. Posso te ajudar em alguma outra coisa?"
}
