
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Testai — Gerador de Checklists de Testes", layout="wide")

# Estilos CSS embutidos
st.markdown("""
    <style>
        body { font-family: Arial; margin: 20px; }
        .header { color: #1a5da0; font-size: 32px; font-weight: bold; }
        .subheader { color: #333; font-size: 18px; margin-top: -10px; margin-bottom: 20px; }
        .section-title { color: #1a5da0; font-size: 20px; font-weight: bold; margin-top: 30px; }
        .checkbox-item { margin-left: 10px; }
        .log-box { background-color: #f5f8fa; padding: 10px; border-radius: 5px; margin-top: 10px; }
        .button-row button { margin-right: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown('<div class="header">Controle de Testes</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Novo Modelo de Fatura - Cliente Jaguariúna</div>', unsafe_allow_html=True)

# Responsável e Data
col1, col2 = st.columns(2)
with col1:
    responsavel = st.text_input("Nome do Responsável:", placeholder="Digite seu nome")
with col2:
    data_teste = st.date_input("Data do Teste:", value=datetime.today())

# Itens a validar
st.markdown('<div class="section-title">Itens a Validar</div>', unsafe_allow_html=True)
itens = ["Item 1", "Item 2", "Item 3"]
checks = []
for item in itens:
    checks.append(st.checkbox(item))

# Barra de Progresso
st.markdown('<div class="section-title">Progresso dos Testes:</div>', unsafe_allow_html=True)
progresso = sum(checks) / len(itens) if itens else 0
st.progress(progresso)
st.write(f"{int(progresso * 100)}% Concluído ({sum(checks)}/{len(itens)})")

# Log de Alterações
st.markdown('<div class="section-title">Log de Alterações</div>', unsafe_allow_html=True)
log = st.empty()
log.markdown('<div class="log-box">[23/04/2025, 09:25:24] Código de Barras - marcou</div>', unsafe_allow_html=True)

# Botões Funcionais
st.markdown('<div class="section-title">Ações</div>', unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.button("Salvar Progresso")
with col2:
    st.button("Exportar Relatório")
with col3:
    st.button("Exportar HTML com Progresso")
with col4:
    st.button("Gerar Relatório de Controle de Teste")
with col5:
    st.button("Gerar Relatório de Ajustes")
with col6:
    st.button("Limpar Log")
