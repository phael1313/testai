import streamlit as st
import openai
import os
from docx import Document

openai.api_key = os.getenv("OPENAI_API_KEY")

def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text for p in doc.paragraphs])

def gerar_html_com_ia(texto):
    prompt = f"""
    Gere um relatório HTML com base no seguinte conteúdo extraído de um .docx:
    
    {texto}
    
    O HTML deve conter:
    - Título principal "Controle de Testes"
    - Subtítulo com nome do cliente (extraído do texto se possível)
    - Campo para nome do responsável e data
    - Lista de itens extraídos com checkbox ao lado de cada um
    - Log de alterações
    - Barra de progresso de testes
    - Botões para exportar, salvar e reiniciar
    O layout deve ser limpo, responsivo e visualmente agradável.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            { "role": "user", "content": prompt }
        ]
    )
    return response.choices[0].message.content

st.set_page_config(page_title="Testai — Gerador de Checklists de Testes", layout="wide")

st.title("Testai — Gerador de Checklists de Testes")
st.markdown("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist interativo em HTML.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type="docx")

if uploaded_file:
    st.success("Arquivo lido com sucesso!")
    if st.button("Gerar HTML via IA"):
        with st.spinner("Gerando relatório inteligente com IA..."):
            texto = extrair_texto_docx(uploaded_file)
            html_gerado = gerar_html_com_ia(texto)
            st.download_button("Baixar Relatório HTML com IA", data=html_gerado, file_name="relatorio.html", mime="text/html")