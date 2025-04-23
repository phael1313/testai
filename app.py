import streamlit as st
from docx import Document
import requests

def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

def gerar_html_com_gpt4(texto):
    prompt = f"""Você é um gerador de relatórios técnicos HTML interativos. Gere sempre com a mesma estrutura visual e organizacional.

Siga exatamente esta estrutura:
- Logotipo no topo (imagem: https://inovamobil.com.br/wp-content/uploads/2023/06/Inovamobil-azul.svg)
- Título principal: "Relatório Técnico de Testes"
- Seções com subtítulos baseados no conteúdo
- Cada item validado deve conter:
  - Um checkbox
  - Uma descrição clara ao lado
- Um campo de texto chamado "Log de Alterações"
- Botões finais fixos, que funcionem via JavaScript:
  - Salvar Progresso (salva no localStorage)
  - Exportar Relatório
  - Exportar HTML com Progresso
  - Gerar Relatório de Controle de Teste
  - Limpar Log
  - Reiniciar Testes

Use sempre as mesmas classes, estrutura visual, organização de botões e layout. Inclua o CSS e JavaScript embutidos no HTML. 

Conteúdo base:
{texto}
"""  

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {st.secrets['openrouter_key']}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    resultado = response.json()
    if "choices" in resultado:
        return resultado["choices"][0]["message"]["content"]
    else:
        return "<p>Erro ao gerar relatório via IA.</p>"

st.set_page_config(page_title="Testai - HTML com GPT-4 Turbo", layout="wide")
st.title("📄 Testai — Relatório com IA Estável (GPT-4 Turbo)")

uploaded_file = st.file_uploader("📎 Envie um arquivo .docx", type=["docx"])

if uploaded_file:
    texto = extrair_texto_docx(uploaded_file)
    html = None
    with st.spinner("🧠 Gerando relatório com GPT-4 Turbo..."):
        html = gerar_html_com_gpt4(texto)

    if html:
        st.download_button("📥 Baixar Relatório HTML com IA", data=html, file_name="relatorio_gpt4.html", mime="text/html")
        st.components.v1.html(html, height=1000, scrolling=True)