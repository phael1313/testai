
import streamlit as st
from docx import Document
import os
from openai import OpenAI
from datetime import datetime

st.set_page_config(page_title="Testai — Gerador de Checklist", layout="wide")

st.title("Testai — Gerador de Checklist")
st.markdown("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist com base no conteúdo e exportar um HTML.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type=["docx"])

if uploaded_file:
    st.success("Arquivo lido com sucesso!")
    doc = Document(uploaded_file)
    texto = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    gerar = st.button("Gerar HTML via IA")
    if gerar:
        with st.spinner("Gerando relatório inteligente com IA..."):
            try:
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

                prompt = f"""
Você é um assistente que recebe uma documentação de teste manual no formato de texto e converte isso em um arquivo HTML estruturado com base no layout fixo da empresa.
Gere uma estrutura de relatório contendo:
- Título principal como 'Controle de Testes'
- Subtítulo com o nome do cliente e descrição do projeto, se houver
- Campo para nome do responsável (input preenchível)
- Campo para data do teste (preenchível)
- Seção 'Itens a Validar' com checkbox para cada item extraído
- Barra de progresso dinâmica
- Seção 'Log de Alterações'
- Botões fixos ao final: 'Salvar Progresso', 'Exportar HTML com Progresso', 'Gerar Relatório de Ajustes', 'Limpar Log', 'Reiniciar Testes'

O estilo visual deve seguir:
- Fonte Arial
- Títulos na cor #1a5da0
- Margem lateral de 20px
- Organização em divs com classes: header, report-section, item-list, item, log-section
- Os checkboxes devem ser gerados com base nos itens que você identificar na documentação
- Todos os botões devem funcionar via JavaScript

Retorne apenas o conteúdo HTML completo e funcional, com CSS embutido. Não inclua comentários nem explicações.
Conteúdo a ser processado:
"""
{texto}
"""
                """

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é um gerador de relatórios em HTML."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )

                html_content = response.choices[0].message.content

                filename = "relatorio_testes_gerado.html"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(html_content)

                with open(filename, "rb") as f:
                    st.download_button("📥 Baixar Relatório HTML com IA", f, file_name=filename)

            except Exception as e:
                st.error(f"Erro ao gerar HTML: {e}")
