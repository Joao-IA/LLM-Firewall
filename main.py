from openai import OpenAI
import streamlit as st
from firewall_llm import get_openai_response


def main():
    st.title("Content Guard")
    user_input = st.text_input("Digite sua mensagem:")
    if st.button("Enviar"):
        response = get_openai_response(user_input)
        st.write("Resposta:", response)

if __name__ == "__main__":
    main()