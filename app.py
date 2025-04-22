import streamlit as st
from docx import Document
import requests

def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])

# IA gratuita via Hugging Face (modelo Flan-T5-Small)
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
        headers={"Content-Type": "application/json"},
        json={"inputs": prompt}
    )

    resultado = response.json()
    return resultado[0]["generated_text"] if isinstance(resultado, list) else "Erro ao gerar resposta"



# Interface Streamlit
