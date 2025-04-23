import streamlit as st
from docx import Document
import requests

def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

def gerar_html_completo_via_ia(texto):
    prompt = f"""Você é um gerador de relatórios técnicos interativos. Com base no conteúdo abaixo, crie um código HTML completo que contenha:

- Títulos, seções e subtópicos com base no conteúdo
- Cada item validado/testado deve conter:
  - Um checkbox ao lado esquerdo
  - Um texto explicativo/descritivo do item
- Campo "Log de Alterações" editável
- Botões funcionais no final da página:
  - "Salvar Progresso" (salva marcações no navegador com localStorage)
  - "Exportar Relatório" (baixa versão sem progresso)
  - "Exportar HTML com Progresso" (baixa com checkboxes marcados e log)
  - "Gerar Relatório de Controle de Teste"
  - "Limpar Log"
  - "Reiniciar Testes"

Inclua estilos CSS e scripts JS no próprio HTML. O layout deve ser bonito, organizado e totalmente funcional.

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
            "model": "openchat/openchat-7b",
            "messages": [{"role": "user", "content": prompt}]
        }
    )
    resultado = response.json()
    if "choices" in resultado:
        return resultado["choices"][0]["message"]["content"]
    else:
        return "<p>Erro ao gerar relatório via IA.</p>"

st.set_page_config(page_title="Testai - IA HTML Dinâmico", layout="wide")
st.title("📄 Testai — Relatório HTML com IA Dinâmica")

uploaded_file = st.file_uploader("📎 Envie um arquivo .docx", type=["docx"])

if uploaded_file:
    texto = extrair_texto_docx(uploaded_file)
    html = None
    with st.spinner("🧠 Gerando relatório inteligente com IA..."):
        html = gerar_html_completo_via_ia(texto)

    if html:
        st.download_button("📥 Baixar Relatório HTML com IA", data=html, file_name="relatorio_completo_ia.html", mime="text/html")
        st.components.v1.html(html, height=1000, scrolling=True)