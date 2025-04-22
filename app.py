import streamlit as st
from docx import Document
import requests

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

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {st.secrets['openrouter_key']}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistral/mistral-7b-instruct",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    if response.status_code != 200:
        return f"Erro: {response.status_code} - {response.text}"

    try:
        resultado = response.json()
        return resultado["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erro ao processar resposta da IA: {str(e)}"

st.set_page_config(page_title="Testai — Checklist com IA (OpenRouter)", layout="wide")
st.title("✅ Testai — Gerador de Checklists com IA (via OpenRouter)")

uploaded_file = st.file_uploader("📎 Envie um arquivo .docx de testes manuais", type=["docx"])

if uploaded_file:
    texto = extrair_texto_docx(uploaded_file)
    st.success("Arquivo lido com sucesso!")

    if st.button("🧠 Gerar HTML com IA"):
        with st.spinner("Aguarde..."):
            html_gerado = gerar_html_com_ia(texto)
            st.download_button("📥 Baixar HTML Gerado", data=html_gerado, file_name="checklist_teste.html", mime="text/html")
            st.code(html_gerado, language="html")