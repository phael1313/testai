import streamlit as st
from docx import Document
import requests

def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

def obter_resposta_da_ia(texto):
    prompt = f"""

Você é um especialista em gerar um relatório de testes manuais de software.
Preciso que você crie um formulário de controle de testes manuais com checklist interativo.
Cada item a ser testado, deve ser inserido junto com um checkbox para marcar, se foi ou não testado
Baseie-se no conteúdo a seguir extraído de um .docx

{texto}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {st.secrets['openrouter_key']}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openchat/openchat-7b",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    resultado = response.json()
    if "choices" in resultado:
        return resultado["choices"][0]["message"]["content"]
    else:
        return f"Erro: {resultado}"

# App Streamlit
st.set_page_config(page_title="Testai — IA com prompt livre", layout="wide")
st.title("🧠 Testai — Geração livre via OpenRouter")

uploaded_file = st.file_uploader("📎 Envie um arquivo .docx", type=["docx"])

if uploaded_file:
    texto = extrair_texto_docx(uploaded_file)

    if st.button("Enviar para IA"):
        with st.spinner("Aguarde resposta..."):
            resposta = obter_resposta_da_ia(texto)
            st.text_area("Resposta da IA", value=resposta, height=500)
            st.download_button("📥 Baixar como HTML", data=resposta, file_name="resultado.html", mime="text/html")