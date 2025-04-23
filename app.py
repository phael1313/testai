
import os
import streamlit as st
from openai import OpenAI
import docx2txt
from datetime import datetime

client = OpenAI()

def extrair_texto_docx(arquivo):
    return docx2txt.process(arquivo)

def gerar_html_com_ia(texto):
    prompt = f"""A partir do conteúdo abaixo, gere um checklist interativo em HTML.
Cada item deve conter:
- Um checkbox
- Um pequeno texto explicando o que deve ser validado
- Organize os tópicos em seções, se fizer sentido.

Conteúdo:
"""{texto}"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um gerador de relatórios HTML com base em documentos .docx"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

st.set_page_config(page_title="Testai — Gerador de Checklist com IA", layout="wide")
st.title("Testai — Gerador de Checklist com IA")
st.markdown("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist interativo em HTML.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type="docx")

if uploaded_file is not None:
    texto_extraido = extrair_texto_docx(uploaded_file)
    st.success("Arquivo lido com sucesso!")
    
    if st.button("Gerar HTML via IA"):
        with st.spinner("Gerando relatório inteligente com IA..."):
            try:
                html_gerado = gerar_html_com_ia(texto_extraido)
                st.download_button("📥 Baixar Relatório HTML com IA", html_gerado, file_name="relatorio_gerado.html", mime="text/html")
            except Exception as e:
                st.error(f"Erro ao gerar HTML: {e}")
