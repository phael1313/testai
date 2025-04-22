import streamlit as st
from docx import Document
import requests

def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])

def gerar_html_com_ia(texto_docx):
    prompt = f"""
    Gere um checklist HTML com base no seguinte texto extraído de um documento de testes:

    {texto_docx}

    Estrutura do HTML esperada:
    - Título
    - Lista com checkbox para cada item de teste
    - Campo para nome do responsável
    - Campo para data/hora
    - Log de observações
    """

    response = requests.post(
    "https://api-inference.huggingface.co/models/google/flan-t5-small",
    headers={
        "Authorization": f"Bearer {st.secrets['hf_token']}",
        "Content-Type": "application/json"
    },
    json={"inputs": prompt}
)
    
    if response.status_code != 200:
        return f"Erro: status {response.status_code} - {response.text}"

    try:
        resultado = response.json()
        return resultado[0]["generated_text"] if isinstance(resultado, list) else "Resposta inválida"
    except Exception as e:
        return f"Erro ao processar resposta da IA: {str(e)}"


st.set_page_config(page_title="Testai — Checklist com IA Gratuita", layout="wide")
st.title("✅ Testai — Gerador de Checklists (sem chave)")

uploaded_file = st.file_uploader("📎 Envie um arquivo .docx de testes manuais", type=["docx"])

if uploaded_file:
    texto = extrair_texto_docx(uploaded_file)
    st.success("Arquivo lido com sucesso!")

    if st.button("🧠 Gerar HTML com IA gratuita"):
        with st.spinner("Aguarde..."):
            html_gerado = gerar_html_com_ia(texto)
            st.download_button("📥 Baixar HTML Gerado", data=html_gerado, file_name="checklist_teste.html", mime="text/html")
            st.code(html_gerado, language="html")
