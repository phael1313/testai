import os
import streamlit as st
import docx2txt
import openai
from datetime import datetime

# Configurações da página
st.set_page_config(page_title="Testai — Gerador de Checklist", layout="wide")

st.title("Testai — Gerador de Checklist 📋")
st.markdown("Envie um arquivo .docx com a documentação do teste. A IA irá gerar um checklist visual em HTML com base no conteúdo.")

uploaded_file = st.file_uploader("Envie um arquivo .docx de testes manuais", type=["docx"])

if uploaded_file:
    st.success("Arquivo lido com sucesso!")
    text = docx2txt.process(uploaded_file)

    if st.button("Gerar HTML via IA"):
        with st.spinner("Gerando relatório inteligente com IA..."):
            try:
                openai.api_key = os.getenv("OPENAI_API_KEY")

                prompt = f"""
Você é um engenheiro de qualidade especializado em testes manuais.

Baseando-se no seguinte conteúdo extraído de uma documentação de teste (.docx), crie um relatório HTML com:

- Título: Controle de Testes
- Subtítulo com o nome do projeto ou cliente (deduzido do texto, se houver)
- Campo editável para "Nome do Responsável"
- Campo de data do teste (já preenchido com a data atual)
- Seção: "Itens a Validar" com uma lista de itens extraídos do texto, cada um com checkbox ao lado
- Barra de progresso (0 a 100%) de acordo com os checkboxes marcados
- Seção: "Log de Alterações" (dinâmica via JavaScript)
- Botões com as seguintes funções:
    - Salvar Progresso
    - Exportar Relatório
    - Exportar HTML com Progresso
    - Reiniciar Testes
    - Gerar Relatório de Ajustes
    - Limpar Log

Use cores elegantes e estrutura responsiva. Importe o logo da Inovamobil via link: https://inovamobil.com.br/wp-content/uploads/2023/06/Inovamobil-azul.svg

Conteúdo para análise:
{text}
"""

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2
                )

                html_output = response.choices[0].message["content"]

                html_path = Path("relatorio_gerado.html")
                html_path.write_text(html_output, encoding="utf-8")

                with open(html_path, "rb") as f:
                    st.download_button(
                        label="📥 Baixar Relatório HTML com IA",
                        data=f,
                        file_name="relatorio_gerado.html",
                        mime="text/html"
                    )
            except Exception as e:
                st.error(f"Erro ao gerar HTML: {e}")