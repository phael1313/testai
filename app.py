
import streamlit as st
from docx import Document
from datetime import datetime
import base64

st.set_page_config(page_title="Testai – Relatório com Prompt Personalizado", layout="wide")

st.title("Testai — Gerador de Checklists de Testes")
st.caption("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist interativo baseado no conteúdo.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type=["docx"])

def gerar_html_testes(itens):
    checkboxes_html = ""
    for item in itens:
        checkboxes_html += f'<div class="item"><input type="checkbox">{item.strip()}</div>\n'

    html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Controle de Testes - Inovamobil</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1 { color: #1a5da0; font-size: 28px; }
    h2 { color: #1a5da0; font-size: 22px; margin-top: 30px; }
    .header { margin-bottom: 20px; }
    .subheader { font-size: 16px; color: #444; }
    .form-section { display: flex; gap: 20px; margin: 20px 0; align-items: center; }
    label { display: block; font-weight: bold; margin-bottom: 5px; }
    input[type="text"], input[type="date"] {
        padding: 8px; width: 100%; max-width: 300px; border: 1px solid #ccc; border-radius: 4px;
    }
    .item { margin-bottom: 10px; }
    input[type="checkbox"] { margin-right: 8px; }
    .progress-container { background: #f0f2f5; border-radius: 6px; height: 20px; width: 100%; margin-top: 10px; }
    .progress-bar { height: 100%; width: 0%; background: #1a5da0; border-radius: 6px; transition: width 0.3s; }
    .progress-text { text-align: center; font-size: 14px; margin-top: 5px; }
    #log { background: #f8fafd; border: 1px solid #cdd4da; padding: 10px; margin-top: 10px; border-radius: 5px; font-size: 14px; }
    .buttons { margin-top: 30px; }
    button { margin: 5px; padding: 10px 16px; font-weight: bold; border: none; border-radius: 5px; cursor: pointer; }
    .btn-blue { background: #1a5da0; color: white; }
    .btn-green { background: #28a745; color: white; }
    .btn-gray { background: #6c757d; color: white; }
    .btn-red { background: #dc3545; color: white; }
    .logo { text-align: center; margin-bottom: 30px; }
  </style>
</head>
<body>

<div class="logo">
  <img src="https://inovamobil.com.br/wp-content/uploads/2023/06/Inovamobil-azul.svg" width="300">
</div>

<h1>Controle de Testes</h1>
<div class="subheader">Novo Modelo de Fatura - Cliente Jaguariúna</div>

<div class="form-section">
  <div>
    <label>Nome do Responsável:</label>
    <input type="text" id="responsavel" placeholder="Digite seu nome">
  </div>
  <div>
    <label>Data do Teste:</label>
    <input type="date" id="data_teste" value="{datetime.now().date()}">
  </div>
</div>

<h2>Itens a Validar</h2>

<div id="checkboxes">
  """ + checkboxes_html + """
</div>

<h2>Progresso dos Testes:</h2>
<div class="progress-container">
  <div id="progress-bar" class="progress-bar"></div>
</div>
<div id="progress-text" class="progress-text">0% Concluído (0/{len(itens)})</div>

<h2>Log de Alterações</h2>
<div id="log">Nenhuma alteração realizada ainda.</div>

<div class="buttons">
  <button class="btn-blue" onclick="salvar()">Salvar Progresso</button>
  <button class="btn-gray" onclick="baixar()">Exportar Relatório</button>
  <button class="btn-green" onclick="baixarComProgresso()">Exportar HTML com Progresso</button>
  <button class="btn-green" onclick="window.print()">Gerar Relatório de Controle de Teste</button>
  <button class="btn-red" onclick="limparLog()">Limpar Log</button>
  <button class="btn-red" onclick="reiniciar()">Reiniciar Testes</button>
</div>

<script>
function atualizarProgresso() {{
  const total = document.querySelectorAll('#checkboxes input[type=checkbox]').length;
  const marcados = document.querySelectorAll('#checkboxes input[type=checkbox]:checked').length;
  const porcentagem = Math.round((marcados / total) * 100);
  document.getElementById("progress-bar").style.width = porcentagem + "%";
  document.getElementById("progress-text").textContent = `${{porcentagem}}% Concluído (${{marcados}}/${{total}})`;
}}

document.querySelectorAll('#checkboxes input[type=checkbox]').forEach(cb => {{
  cb.addEventListener('change', e => {{
    const acao = cb.checked ? "marcou" : "desmarcou";
    const texto = cb.parentElement.textContent.trim();
    const data = new Date().toLocaleString();
    const novaLinha = `<div>[${{data}}] ${{texto}} - ${{acao}}</div>`;
    const log = document.getElementById("log");
    log.innerHTML = log.innerHTML === "Nenhuma alteração realizada ainda." ? novaLinha : novaLinha + log.innerHTML;
    atualizarProgresso();
  }});
}});

function salvar() {{
  const checks = Array.from(document.querySelectorAll('input[type=checkbox]')).map(cb => cb.checked);
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
  const nome = localStorage.getItem("responsavel") || "";
  const data = localStorage.getItem("data_teste") || "";
  const log = localStorage.getItem("log") || "Nenhuma alteração realizada ainda.";
  document.getElementById("responsavel").value = nome;
  document.getElementById("data_teste").value = data;
  document.getElementById("log").innerHTML = log;
  atualizarProgresso();
}}

function limparLog() {{
  document.getElementById("log").innerHTML = "Nenhuma alteração realizada ainda.";
}}

function baixar() {{
  const html = document.documentElement.outerHTML;
  const blob = new Blob([html], {{type: "text/html"}});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "relatorio_controle_teste.html";
  a.click();
}}

function baixarComProgresso() {{
  salvar();
  baixar();
}}

function reiniciar() {{
  localStorage.clear();
  location.reload();
}}

carregar();
</script>
</body>
</html>
"""
    return html

if uploaded_file:
    doc = Document(uploaded_file)
    texto = " ".join([p.text for p in doc.paragraphs])
    # Simulação da IA: gerando itens com base em bullet points
    linhas = [l.strip("–•- ") for l in texto.split("\n") if l.strip().startswith(("–", "-", "•"))]
    html_final = gerar_html_testes(linhas if linhas else ["Item 1", "Item 2", "Item 3"])
    st.success("✅ HTML gerado com sucesso!")
    b64 = base64.b64encode(html_final.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="relatorio_controle_teste.html"><button>📥 Baixar HTML Gerado</button></a>'
    st.markdown(href, unsafe_allow_html=True)
