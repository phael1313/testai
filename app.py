
import streamlit as st
from docx import Document
import openai

st.set_page_config(page_title="Testai — Gerador de Checklists de Testes", layout="wide")

st.title("Testai — Gerador de Checklists de Testes")
st.markdown("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist em HTML.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type="docx")

if uploaded_file is not None:
    doc = Document(uploaded_file)
    texto_extraido = ""
    for par in doc.paragraphs:
        texto_extraido += par.text + "\n"

    st.success("Arquivo lido com sucesso!")
    if st.button("Gerar HTML via IA"):
        with st.spinner("Gerando relatório inteligente com IA..."):
            try:
                client = openai.OpenAI(api_key=st.secrets["openai_key"])
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um gerador de relatórios HTML com base em arquivos .docx. Use layout moderno, com barra de progresso, log de alterações, campos Nome do Responsável e Data, e seções de checklist com checkbox interativo. A estrutura visual deve ser limpa e responsiva."},
                        {"role": "user", "content": texto_extraido}
                    ]
                )
                html_gerado = response.choices[0].message.content

                st.markdown("### HTML gerado com sucesso!")
                st.download_button("📥 Baixar HTML Gerado", html_gerado, file_name="relatorio_teste.html", mime="text/html")
            except Exception as e:
                st.error(f"Erro ao gerar HTML: {str(e)}")
