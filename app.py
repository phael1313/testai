
import streamlit as st
import requests
from docx import Document
from io import BytesIO
import os

# Configurar título
st.set_page_config(page_title="Testai - Geração de Relatório HTML")
st.title("📄 Geração de Relatório HTML via IA")

# Upload do arquivo DOCX
uploaded_file = st.file_uploader("Envie o arquivo .docx com os testes", type=["docx"])

if uploaded_file:
    # Extrair texto do arquivo
    doc = Document(uploaded_file)
    text_content = "\n".join([p.text for p in doc.paragraphs])

    st.subheader("📑 Conteúdo Extraído")
    st.text_area("Texto do Documento:", text_content, height=200)

    # Chave da API (você pode definir no ambiente ou direto aqui)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "SUA_CHAVE_AQUI"
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

    # Gerar HTML
    if st.button("🔮 Gerar HTML via IA"):
        with st.spinner("Gerando HTML..."):
            prompt = (
                "Você receberá o conteúdo de um arquivo .docx contendo um checklist técnico. "
                "Extraia os dados relevantes como: nome do cliente, data de execução, lista de testes com status, "
                "observações finais e nome do responsável. Em seguida, gere um HTML completo com estrutura visual clara, "
                "com título, tabela de testes e rodapé com dados do responsável. Use apenas os dados abaixo:\n\n"
                f"{text_content}"
            )

            response = requests.post(
                OPENAI_API_URL,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                },
            )

            result = response.json()
            html_output = result["choices"][0]["message"]["content"]

            st.subheader("📄 HTML Gerado")
            st.code(html_output, language="html")

            # Baixar HTML como arquivo
            st.download_button(
                label="📥 Baixar HTML",
                data=html_output,
                file_name="relatorio_gerado.html",
                mime="text/html"
            )
