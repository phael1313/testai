import streamlit as st
from docx import Document
import requests
import datetime
import json

def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

def obter_dados_via_ia(texto):
    prompt = f"""
    Abaixo está o conteúdo de um arquivo .docx referente a testes manuais de software.

    Sua tarefa é extrair os seguintes dados do texto e retornar APENAS neste formato JSON:
    {{
      "nome_cliente": "Nome do cliente",
      "numero_fatura": "Número da fatura",
      "responsavel": "Nome do responsável",
      "testes": ["Item de teste 1", "Item de teste 2", "Item de teste 3"]
    }}

    Responda somente com o JSON e sem nenhum comentário extra.

    Texto extraído:
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
        return json.dumps({"erro": "A IA não retornou uma resposta válida. Detalhe: " + str(resultado)})

def gerar_html_final(dados):
    with open("template_testai_layout_fixo.html", "r", encoding="utf-8") as f:
        template = f.read()

    campos = json.loads(dados)
    hoje = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

    if "erro" in campos:
        return f"<p style='color:red;'>Erro: {campos['erro']}</p>"

    testes_html = ""
    for item in campos.get("testes", []):
        testes_html += f"<p><input type='checkbox'> {item}</p>\n"

    final = template.replace("{{nome_cliente}}", campos.get("nome_cliente", ""))
    final = final.replace("{{numero_fatura}}", campos.get("numero_fatura", ""))
    final = final.replace("{{responsavel}}", campos.get("responsavel", ""))
    final = final.replace("{{data}}", hoje)
    final = final.replace("{{testes_html}}", testes_html)

    return final

# Streamlit app
st.set_page_config(page_title="Testai — Relatório com Layout Fixo", layout="wide")
st.title("✅ Testai — Layout fixo com dados via IA")

uploaded_file = st.file_uploader("📎 Envie o arquivo .docx com os dados de teste", type=["docx"])

if uploaded_file:
    texto = extrair_texto_docx(uploaded_file)

    if st.button("🧠 Gerar HTML via IA"):
        with st.spinner("Processando..."):
            dados_json = obter_dados_via_ia(texto)
            html_final = gerar_html_final(dados_json)
            st.download_button("📥 Baixar Relatório HTML", data=html_final, file_name="relatorio_final.html", mime="text/html")
            st.code(html_final, language="html")