import streamlit as st
from docx import Document
from openai import OpenAI

st.set_page_config(page_title="Testai — Gerador de Checklists de Testes", layout="wide")

st.title("Testai — Gerador de Checklists de Testes")
st.markdown("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist em HTML baseado nele.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type="docx")

if uploaded_file:
    st.success("Arquivo lido com sucesso!")

    if st.button("Gerar HTML via IA"):
        with st.spinner("Gerando relatório inteligente com IA..."):
            # Extrair texto do .docx
            doc = Document(uploaded_file)
            texto_extraido = "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])

            # Nova API do OpenAI
            client = OpenAI(api_key=st.secrets["openai_key"])

            prompt = f"""Você é um gerador de relatórios HTML. 
Crie um relatório HTML com base no conteúdo abaixo, mantendo o layout padrão de checklist com campos editáveis, barra de progresso, nome do cliente e responsável, e botões funcionais:

{texto_extraido}"""

            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "Você é um gerador de relatórios HTML."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            html_output = response.choices[0].message.content

            # Salvar o HTML em arquivo
            with open("relatorio_gerado.html", "w", encoding="utf-8") as f:
                f.write(html_output)

            st.success("✅ HTML gerado com sucesso!")
            with open("relatorio_gerado.html", "rb") as file:
                st.download_button("📥 Baixar HTML Gerado", file, file_name="relatorio_gerado.html", mime="text/html")