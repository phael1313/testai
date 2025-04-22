import streamlit as st
from docx import Document
from openai import OpenAI

# Conectando ao cliente da OpenAI v1
client = OpenAI(api_key=st.secrets["openai_key"])

def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])

def gerar_html_com_ia(texto_docx):
    prompt = f"""
    Abaixo está uma documentação de testes manuais de software extraída de um arquivo .docx:

    {texto_docx}

    Gere um código HTML completo com:
    - Checkbox para cada item de teste
    - Campo para nome do responsável
    - Campo para data/hora
    - Log de ações com espaço para observações
    - Botão fictício 'Exportar Relatório'
    """

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return resposta.choices[0].message.content

st.set_page_config(page_title="Testai — Checklist de Testes", layout="wide")
st.title("✅ Testai — Gerador de Checklists de Testes")

uploaded_file = st.file_uploader("📎 Envie um arquivo .docx de testes manuais", type=["docx"])

if uploaded_file:
    texto = extrair_texto_docx(uploaded_file)
    st.success("Arquivo lido com sucesso!")

    if st.button("🧠 Gerar HTML com IA"):
        with st.spinner("Gerando HTML com IA..."):
            html_gerado = gerar_html_com_ia(texto)
            st.download_button("📥 Baixar HTML Gerado", data=html_gerado, file_name="checklist_teste.html", mime="text/html")
            st.code(html_gerado, language="html")
