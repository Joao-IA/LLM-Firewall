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

