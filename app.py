import streamlit as st
from docx import Document
import requests
import datetime

# Função para extrair texto puro de um .docx
def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return [p.text.strip() for p in doc.paragraphs if p.text.strip()]

# Geração da seção HTML de testes com checkbox
def gerar_html_testes(lista_testes):
    blocos = []
    for item in lista_testes:
        linha = f"<p><input type='checkbox'> {item}</p>"
        blocos.append(linha)
    return "\n".join(blocos)

# Função principal que monta o HTML com base no template
def gerar_html_final(responsavel, testes):
    with open("template_testai_base.html", "r", encoding="utf-8") as f:
        template = f.read()
    html_testes = gerar_html_testes(testes)
    hoje = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    final = template.replace("{{responsavel}}", responsavel)
    final = final.replace("{{data}}", hoje)
    final = final.replace("{{testes_html}}", html_testes)
    return final

st.set_page_config(page_title="Testai — Checklist com Template Fixo", layout="wide")
st.title("✅ Testai — Gerador com Layout Fixo")

uploaded_file = st.file_uploader("📎 Envie um arquivo .docx com os itens de teste", type=["docx"])
responsavel = st.text_input("👤 Nome do responsável pelo teste")

if uploaded_file and responsavel:
    lista_testes = extrair_texto_docx(uploaded_file)
    if st.button("🧠 Gerar HTML com base no modelo"):
        with st.spinner("Gerando relatório..."):
            html_gerado = gerar_html_final(responsavel, lista_testes)
            st.download_button("📥 Baixar HTML", data=html_gerado, file_name="relatorio_testes.html", mime="text/html")
            st.code(html_gerado, language="html")