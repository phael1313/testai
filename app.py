import streamlit as st
import docx
import openai
from datetime import datetime

st.set_page_config(page_title="Testai — Gerador de Checklists de Testes", layout="wide")

st.title("Testai — Gerador de Checklists de Testes")
st.markdown("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist com base no conteúdo.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type=["docx"])

if uploaded_file:
    st.success("Arquivo recebido com sucesso!")
    doc = docx.Document(uploaded_file)
    texto = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

    st.info("Gerando checklist com GPT-4 Turbo...")

    openai.api_key = st.secrets["openai_key"]
    prompt = f"""
Você é um assistente de QA. Com base na documentação abaixo, extraia os pontos que devem ser validados
em formato de checklist de testes. Utilize linguagem clara e objetiva. Para cada item, forneça um título
curto e uma breve descrição. Formate como HTML com uma checkbox interativa para cada item.

Documentação:
"""
{texto}
"""
"""

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente especialista em QA e testes de software."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    resultado = response["choices"][0]["message"]["content"]

    html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Checklist de Testes</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        h1 { color: #1a5da0; }
        .item { margin-bottom: 12px; }
    </style>
</head>
<body>
    <h1>Checklist de Testes</h1>
    <p>Preencha os campos abaixo e marque os itens validados.</p>
    <label>Responsável: <input type="text" name="responsavel"></label><br><br>
    <label>Data do Teste: <input type="date" name="data_teste"></label><br><br>

    <div>
        {resultado}
    </div>
</body>
</html>
""".replace("{resultado}", resultado)

    with open("/mnt/data/relatorio_gerado.html", "w", encoding="utf-8") as f:
        f.write(html_template)

    st.success("✅ HTML gerado com sucesso!")
    st.download_button("📥 Baixar HTML Gerado", data=html_template, file_name="checklist_teste.html", mime="text/html")
