import streamlit as st
import openai
import docx2txt
import os

st.set_page_config(page_title="Testai — Gerador de Checklists de Testes", layout="wide")
st.title("Testai — Gerador de Checklists de Testes")
st.markdown("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist com base no conteúdo.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type="docx")

if uploaded_file:
    with open("documento.docx", "wb") as f:
        f.write(uploaded_file.read())
    st.success("Arquivo lido com sucesso!")

    gerar = st.button("Gerar HTML via IA")

    if gerar:
        with st.spinner("Gerando relatório inteligente com IA..."):
            texto = docx2txt.process("documento.docx")

            prompt = f"""
Seu papel é gerar um arquivo HTML interativo com base em uma documentação de teste descrita a seguir.
A estrutura visual deve seguir este padrão fixo:

1. Título principal: "Controle de Testes"
2. Subtítulo com nome do cliente e tipo de validação
3. Campos para:
   - Nome do responsável (input editável)
   - Data do teste (input tipo date)
4. Bloco "Itens a Validar": cada item extraído deve conter:
   - Um checkbox
   - Um título (item extraído)
   - Um parágrafo explicativo simples abaixo (pode ser genérico)
5. Bloco "Progresso dos Testes" com uma barra que atualiza conforme checkboxes são marcados
6. Bloco "Log de Alterações" com textarea que registra automaticamente data/hora + ação do usuário (ex: marcou item 1)
7. Bloco final com botões:
   - Salvar Progresso
   - Exportar HTML com Progresso
   - Gerar Relatório de Controle de Teste
   - Limpar Log
   - Reiniciar Testes

Todo o layout deve ser bonito, responsivo, com CSS embutido no HTML (usando <style> no <head>).
Fonte padrão: Arial, títulos com cor azul #1a5da0, margens de 20px.

Conteúdo base extraído do .docx:
"""
{texto}
"""
            """

            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            html_output = response.choices[0].message.content

            with open("relatorio_gerado.html", "w", encoding="utf-8") as f:
                f.write(html_output)

            st.success("HTML gerado com sucesso!")
            with open("relatorio_gerado.html", "rb") as f:
                st.download_button("📥 Baixar Relatório HTML com IA", f, file_name="relatorio_gerado.html")