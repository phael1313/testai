import streamlit as st
import openai
import docx2txt
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Testai — Gerador de Checklists de Testes", layout="wide")

st.title("Testai — Gerador de Checklists de Testes")
st.markdown("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist HTML estruturado.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type=["docx"])

openai.api_key = st.secrets["openai_key"]

def gerar_html_com_ia(texto):
    prompt = f"""
Aja como um gerador de checklist de validação para testes manuais. 
Baseado na documentação abaixo, extraia os itens que devem ser testados e gere um arquivo HTML com a estrutura fixa. 
Utilize o seguinte layout visual: título do projeto, nome do cliente, data do teste, nome do responsável, progresso dos testes, log de alterações e uma lista com checkbox para cada item detectado. 

A estrutura do HTML deve conter também botões para: salvar progresso, exportar HTML com progresso, gerar relatório de controle de teste e reiniciar os testes.

Utilize o seguinte conteúdo para basear o checklist:

"""{texto}"""
"""
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Você é um gerador de relatórios em HTML de testes manuais."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )

    return response["choices"][0]["message"]["content"]

if uploaded_file is not None:
    docx_text = docx2txt.process(uploaded_file)
    with st.spinner("Gerando relatório inteligente com IA..."):
        try:
            html_output = gerar_html_com_ia(docx_text)
            html_file_path = Path("relatorio_gerado.html")
            html_file_path.write_text(html_output, encoding="utf-8")
            st.success("✅ HTML gerado com sucesso!")
            with open(html_file_path, "rb") as f:
                st.download_button("📥 Baixar Relatório HTML com IA", f, file_name="relatorio_gerado.html")
        except Exception as e:
            st.error(f"Erro ao gerar HTML: {e}")