import streamlit as st
import datetime
from docx import Document
import openai

st.set_page_config(page_title="Testai — Gerador de Checklists de Testes", layout="wide")

# Configurar a chave da OpenAI
openai.api_key = st.secrets["openai_key"]

def extrair_texto_docx(uploaded_file):
    doc = Document(uploaded_file)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip() != ""])

def gerar_html_com_ia(texto):
    prompt = f"""
Você é um gerador de HTML especializado em criar relatórios de checklist de teste.
Gere um HTML completo e funcional com base no seguinte conteúdo extraído de um .docx:

"{texto}"

O HTML deve conter:

- Título: "Controle de Testes"
- Subtítulo com o nome do projeto ou cliente (ex: "Novo Modelo de Fatura - Cliente Jaguariúna")
- Campo para nome do responsável
- Campo de data com calendário
- Lista com checkbox para cada item de teste identificado no texto
- Barra de progresso dos testes
- Log automático de alterações
- Botões funcionais no final: "Salvar Progresso", "Exportar Relatório", "Exportar HTML com Progresso", "Gerar Relatório de Ajustes", "Limpar Log", "Reiniciar Testes"

Estilo visual:
- Fonte Arial, margem de 20px
- Títulos na cor azul #1a5da0
- Estilo limpo e responsivo com CSS no <style>
- Estrutura organizada com classes: header, report-section, report-text, item-list, item, item-title

Responda somente com o código HTML final.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message["content"]

st.title("Testai — Gerador de Checklists de Testes")
st.caption("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist baseado nas informações extraídas.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type=["docx"])

if uploaded_file:
    st.success("Arquivo lido com sucesso!")
    texto = extrair_texto_docx(uploaded_file)

    if st.button("Gerar HTML via IA"):
        with st.spinner("Gerando relatório inteligente com IA..."):
            html_gerado = gerar_html_com_ia(texto)
            st.download_button("Baixar Relatório HTML com IA", html_gerado, file_name="relatorio_checklist.html", mime="text/html")