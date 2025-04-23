import streamlit as st
from docx import Document

def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

# HTML base com checkbox interativos e botão para exportar
def gerar_html_exportavel():
    return """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório de Controle de Teste</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            color: #333;
        }
        .header {
            color: #1a5da0;
            font-size: 28px;
            margin-bottom: 30px;
        }
        .report-section {
            margin-bottom: 30px;
        }
        .report-section h2 {
            color: #1a5da0;
            font-size: 22px;
            margin-bottom: 10px;
        }
        .report-text {
            font-size: 16px;
            margin-bottom: 20px;
        }
        .item-list {
            margin-top: 10px;
        }
        .item {
            margin-bottom: 8px;
        }
        .item input[type="checkbox"] {
            margin-right: 10px;
        }
        .info-block label {
            display: block;
            font-weight: bold;
            margin-top: 10px;
        }
        .info-block input {
            width: 100%;
            padding: 5px;
            font-size: 14px;
            margin-top: 5px;
        }
    </style>
</head>
<body>

    <div class="header">Relatório de Controle de Teste</div>

    <div class="report-section info-block">
        <label>Nome do Cliente:</label>
        <input type="text" value="Não informado">

        <label>Nome do Responsável:</label>
        <input type="text" placeholder="Digite o nome do responsável">

        <label>Data do Teste:</label>
        <input type="date">
    </div>

    <div class="report-section">
        <h2>Resumo dos Testes Realizados</h2>
        <div class="report-text">
            Este relatório apresenta os principais testes realizados no sistema para validação funcional. Os resultados apresentados abaixo indicam os itens inspecionados e validados.
        </div>
    </div>

    <div class="report-section">
        <h2>Itens Testados e Validados</h2>
        <div class="item-list">
            <div class="item"><input type="checkbox"> Login com credenciais válidas</div>
            <div class="item"><input type="checkbox"> Cadastro de novo usuário</div>
            <div class="item"><input type="checkbox"> Recuperação de senha</div>
            <div class="item"><input type="checkbox"> Geração de relatórios</div>
            <div class="item"><input type="checkbox"> Logout e sessão expirada</div>
        </div>
    </div>

    <div class="report-section">
        <h2>Conclusão</h2>
        <div class="report-text">
            Todos os testes foram conduzidos conforme as especificações do projeto e critérios de aceite. O sistema demonstrou estabilidade e comportamento adequado nos cenários validados acima.
        </div>
    </div>

    <div class="report-section">
        <button onclick="baixarHTML()">📥 Exportar Relatório Preenchido</button>
    </div>

    <script>
        function baixarHTML() {
            const clone = document.documentElement.cloneNode(true);
            const doctype = "<!DOCTYPE html>";
            const blob = new Blob([doctype + "\n" + clone.outerHTML], {type: "text/html"});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "relatorio_testes_preenchido.html";
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    </script>

</body>
</html>"""

# App Streamlit
st.set_page_config(page_title="Testai — HTML com Exportação", layout="wide")
st.title("🧠 Testai — Geração de HTML com botão de exportação")

uploaded_file = st.file_uploader("📎 Envie um arquivo .docx (opcional)", type=["docx"])

if uploaded_file:
    texto = extrair_texto_docx(uploaded_file)
    st.text_area("Texto extraído do .docx", texto, height=200)

if st.button("Gerar HTML com Exportação"):
    html = gerar_html_exportavel()
    st.download_button("📥 Baixar HTML com exportação", data=html, file_name="relatorio_testes_interativo.html", mime="text/html")
    st.components.v1.html(html, height=900, scrolling=True)