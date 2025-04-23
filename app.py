
import streamlit as st
from docx import Document
from openai import OpenAI
import base64
from datetime import datetime

st.set_page_config(page_title="Testai – Gerador Inteligente de Relatórios", layout="wide")
st.title("Testai — Relatório de Controle de Testes")
st.caption("Envie um .docx e gere um checklist automatizado com base em seu conteúdo.")

uploaded_file = st.file_uploader("📄 Envie um arquivo .docx com a documentação de testes", type=["docx"])

@st.cache_data(show_spinner=False)
def extrair_texto(docx_file):
    doc = Document(docx_file)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

@st.cache_data(show_spinner=True)
def gerar_topicos_com_ia(texto):
    client = OpenAI(api_key=st.secrets["openai_key"])
    prompt = 
Você é um especialista em QA e testes manuais. Abaixo está o conteúdo de uma documentação de testes.

Extraia de forma estruturada os itens que devem ser validados, de acordo com a documentação. Retorne uma lista simples de frases curtas, diretas e claras. Apenas os itens testáveis.

Conteúdo:
"""{texto}"""

Formato de saída:
- Item 1
- Item 2
- ...
"""
    resposta = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    conteudo = resposta.choices[0].message.content
    linhas = [l.strip("-• ").strip() for l in conteudo.split("\n") if l.strip()]
    return linhas

def gerar_html(itens):
    checkboxes_html = ""
    for item in itens:
        checkboxes_html += f'<div class="item"><input type="checkbox"> {item}</div>\n'

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Controle de Testes</title>
  <style>
    body {{ font-family: Arial; margin: 20px; }}
    h1 {{ color: #1a5da0; }}
    h2 {{ color: #1a5da0; margin-top: 30px; }}
    .logo {{ text-align: center; margin-bottom: 30px; }}
    .form-section {{ display: flex; gap: 20px; margin-bottom: 20px; }}
    label {{ font-weight: bold; }}
    input[type="text"], input[type="date"] {{
        padding: 8px; border: 1px solid #ccc; border-radius: 4px; width: 250px;
    }}
    .item {{ margin: 10px 0; }}
    .progress-container {{ background: #f0f2f5; height: 20px; border-radius: 6px; }}
    .progress-bar {{ height: 100%; width: 0%; background: #1a5da0; border-radius: 6px; transition: width 0.3s; }}
    .progress-text {{ font-size: 14px; margin-top: 5px; }}
    #log {{ background: #f8fafd; border: 1px solid #cdd4da; padding: 10px; border-radius: 5px; margin-top: 15px; }}
    button {{ padding: 10px 15px; margin: 10px 5px; border: none; border-radius: 5px; cursor: pointer; }}
    .btn-blue {{ background: #1a5da0; color: white; }}
    .btn-red {{ background: #dc3545; color: white; }}
    .btn-green {{ background: #28a745; color: white; }}
  </style>
</head>
<body>

<div class="logo">
  <img src="https://inovamobil.com.br/wp-content/uploads/2023/06/Inovamobil-azul.svg" width="300">
</div>

<h1>Controle de Testes</h1>
<div><strong>Projeto:</strong> Novo Modelo de Fatura - Cliente Jaguariúna</div>

<div class="form-section">
  <div>
    <label>Responsável:</label><br>
    <input type="text" id="responsavel" placeholder="Digite seu nome">
  </div>
  <div>
    <label>Data do Teste:</label><br>
    <input type="date" id="data_teste" value="{datetime.now().date()}">
  </div>
</div>

<h2>Itens a Validar</h2>
<div id="checkboxes">
{checkboxes_html}
</div>

<h2>Progresso dos Testes:</h2>
<div class="progress-container"><div id="progress-bar" class="progress-bar"></div></div>
<div id="progress-text" class="progress-text">0% Concluído (0/{len(itens)})</div>

<h2>Log de Alterações</h2>
<div id="log">Nenhuma alteração registrada ainda.</div>

<button class="btn-blue" onclick="salvar()">Salvar</button>
<button class="btn-green" onclick="baixar()">Exportar HTML</button>
<button class="btn-red" onclick="reiniciar()">Reiniciar</button>

<script>
function atualizarProgresso() {{
  const cbs = document.querySelectorAll('input[type=checkbox]');
  const marcados = Array.from(cbs).filter(cb => cb.checked).length;
  const total = cbs.length;
  const pct = Math.round((marcados / total) * 100);
  document.getElementById("progress-bar").style.width = pct + "%";
  document.getElementById("progress-text").textContent = `${{pct}}% Concluído (${{marcados}}/${{total}})`;
}}

document.querySelectorAll('input[type=checkbox]').forEach(cb => {{
  cb.addEventListener('change', e => {{
    const texto = cb.parentElement.textContent.trim();
    const acao = cb.checked ? "marcou" : "desmarcou";
    const data = new Date().toLocaleString();
    const nova = `<div>[${{data}}] ${{texto}} - ${{acao}}</div>`;
    const log = document.getElementById("log");
    log.innerHTML = log.innerHTML === "Nenhuma alteração registrada ainda." ? nova : nova + log.innerHTML;
    atualizarProgresso();
  }});
}});

function salvar() {{
  const checks = Array.from(document.querySelectorAll('input[type=checkbox]')).map(c => c.checked);
  const log = document.getElementById("log").innerHTML;
  const nome = document.getElementById("responsavel").value;
  const data = document.getElementById("data_teste").value;
  localStorage.setItem("checks", JSON.stringify(checks));
  localStorage.setItem("log", log);
  localStorage.setItem("responsavel", nome);
  localStorage.setItem("data_teste", data);
  alert("Progresso salvo.");
}}

function carregar() {{
  const checks = JSON.parse(localStorage.getItem("checks") || "[]");
  checks.forEach((v, i) => {{
    const cb = document.querySelectorAll('input[type=checkbox]')[i];
    if (cb) cb.checked = v;
  }});
  document.getElementById("log").innerHTML = localStorage.getItem("log") || "Nenhuma alteração registrada ainda.";
  document.getElementById("responsavel").value = localStorage.getItem("responsavel") || "";
  document.getElementById("data_teste").value = localStorage.getItem("data_teste") || "";
  atualizarProgresso();
}}

function baixar() {{
  salvar();
  const blob = new Blob([document.documentElement.outerHTML], {{type: "text/html"}});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "relatorio_teste.html";
  a.click();
}}

function reiniciar() {{
  localStorage.clear();
  location.reload();
}}

carregar();
</script>

</body>
</html>"""

if uploaded_file:
    texto = extrair_texto(uploaded_file)
    with st.spinner("🔎 Gerando tópicos com GPT-4 Turbo..."):
        topicos = gerar_topicos_com_ia(texto)

    if topicos:
        st.success("✅ Checklist gerado com sucesso!")
        html_resultado = gerar_html(topicos)
        b64 = base64.b64encode(html_resultado.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="checklist_teste.html"><button>📥 Baixar Relatório HTML com IA</button></a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning("Nenhum item foi identificado no documento.")
