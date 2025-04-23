
import streamlit as st

st.set_page_config(page_title="Testai — Gerador de Checklists de Testes", layout="wide")

st.markdown("""
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .titulo { color: #1a5da0; font-size: 32px; font-weight: bold; }
        .subtitulo { font-size: 18px; color: #333; margin-bottom: 20px; }
        .section { margin-top: 30px; }
        .item { margin: 10px 0; }
        .item label { font-size: 16px; }
    </style>
    <div class="titulo">Controle de Testes</div>
    <div class="subtitulo">Novo Modelo de Fatura - Cliente Jaguariúna</div>
    <div class="section">
        <label><strong>Nome do Responsável:</strong></label><br>
        <input type="text" placeholder="Digite seu nome" style="width: 300px; padding: 6px;"><br><br>
        <label><strong>Data do Teste:</strong></label><br>
        <input type="date" style="width: 160px; padding: 6px;">
    </div>
    <div class="section">
        <h3 class="titulo" style="font-size: 20px;">Itens a Validar</h3>
        <div class="item"><input type="checkbox"> Item 1</div>
        <div class="item"><input type="checkbox"> Item 2</div>
        <div class="item"><input type="checkbox"> Item 3</div>
    </div>
""", unsafe_allow_html=True)
