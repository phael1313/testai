import streamlit as st
from docx import Document
import requests
import datetime

# Extrai texto do .docx
def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

# Envia o texto do docx para a IA via OpenRouter
def obter_dados_via_ia(texto):
    prompt = f"""
    Abaixo está um conteúdo extraído de um arquivo .docx com informações sobre testes de software.

    Sua tarefa é:
    - Extrair o nome do cliente
    - Extrair o número da fatura
    - Gerar uma lista em HTML com os itens de teste, onde cada item deve ter um checkbox desmarcado
    - NÃO inclua título, apenas retorne os campos prontos para substituição.

    Responda exatamente neste formato JSON:
    {{
      "nome_cliente": "Nome aqui",
      "numero_fatura": "123456",
      "responsavel": "Responsável aqui",
      "testes_html": "<p><input type='checkbox'> Item 1</p><p><input type='checkbox'> Item 2</p>"
    }}

    Conteúdo extraído:
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
    return resultado["choices"][0]["message"]["content"]

# Preenche o template HTML com os campos retornados da IA
def preencher_template(dados_ia):
    import json
    with open("template_testai_openrouter.html", "r", encoding="utf-8") as f:
        template = f.read()

    campos = json.loads(dados_ia)
    hoje = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    final = template.replace("{{nome_cliente}}", campos.get("nome_cliente", ""))
    final = final.replace("{{numero_fatura}}", campos.get("numero_fatura", ""))
    final = final.replace("{{responsavel}}", campos.get("responsavel", ""))
    final = final.replace("{{data}}", hoje)
    final = final.replace("{{testes_html}}", campos.get("testes_html", ""))

    return final

# Streamlit App
st.set_page_config(page_title="Testai — Relatório com Layout Fixo (IA)", layout="wide")
st.title("✅ Testai — Relatório com Layout Fixo via IA")

uploaded_file = st.file_uploader("📎 Envie um arquivo .docx de testes", type=["docx"])

if uploaded_file:
    texto = extrair_texto_docx(uploaded_file)
    if st.button("🧠 Gerar HTML com IA"):
        with st.spinner("Processando via IA..."):
            dados_json = obter_dados_via_ia(texto)
            html_final = preencher_template(dados_json)
            st.download_button("📥 Baixar HTML", data=html_final, file_name="relatorio_teste_gerado.html", mime="text/html")
            st.code(html_final, language="html")