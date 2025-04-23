import streamlit as st
from docx import Document

def extrair_texto_docx(arquivo):
    doc = Document(arquivo)
    return "\n".join([p.text.strip() for p in doc.paragraphs if p.text.strip()])

def gerar_html_corrigido():
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
        button {
            font-size: 15px;
            padding: 10px 15px;
        }
    </style>
</head>
<body>

    <div class="header">Relatório de Controle de Teste</div>

    <div class="report-section info-block">
        <label>Nome do Cliente:</label>
        <input id="cliente" type="text" value="Não informado">

        <label>Nome do Responsável:</label>
        <input id="responsavel" type="text" placeholder="Digite o nome do responsável">

        <label>Data do Teste:</label>
        <input id="data" type="date">
    </div>

    <div class="report-section">
        <h2>Resumo dos Testes Realizados</h2>
        <div class="report-text">
            Este relatório documenta os principais testes realizados com o objetivo de validar o correto funcionamento das funcionalidades do sistema.
        </div>
    </div>

    <div class="report-section">
        <h2>Itens Testados e Validados</h2>
        <div class="item-list">
            <div class="item"><input type="checkbox"> Funcionalidade de login</div>
            <div class="item"><input type="checkbox"> Cadastro de usuários</div>
            <div class="item"><input type="checkbox"> Edição de dados</div>
            <div class="item"><input type="checkbox"> Exclusão de registros</div>
            <div class="item"><input type="checkbox"> Geração de relatórios</div>
        </div>
    </div>

    <div class="report-section">
        <h2>Conclusão</h2>
        <div class="report-text">
            Com base nos testes realizados, conclui-se que o sistema está operando de acordo com os critérios estabelecidos e encontra-se apto para uso. Todos os itens testados foram devidamente validados.
        </div>
    </div>

    <div class="report-section">
        <button onclick="baixarHTML()">📥 Exportar Relatório Preenchido</button>
    </div>

    <script>
        function baixarHTML() {
            const cliente = document.getElementById('cliente').value;
            const responsavel = document.getElementById('responsavel').value;
            const data = document.getElementById('data').value;
            const checkboxes = document.querySelectorAll('input[type=checkbox]');
            const estadoCheckboxes = Array.from(checkboxes).map(cb => cb.checked);

            const clone = document.documentElement.cloneNode(true);
            clone.getElementById('cliente').setAttribute('value', cliente);
            clone.getElementById('responsavel').setAttribute('value', responsavel);
            clone.getElementById('data').setAttribute('value', data);

            const clonedCheckboxes = clone.querySelectorAll('input[type=checkbox]');
            estadoCheckboxes.forEach((checked, index) => {
                if (checked) {
                    clonedCheckboxes[index].setAttribute('checked', 'checked');
                } else {
                    clonedCheckboxes[index].removeAttribute('checked');
                }
            });

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
st.set_page_config(page_title="Testai — Relatório Exportável Corrigido", layout="wide")
st.title("🧠 Testai — Relatório com Exportação Funcional")

uploaded_file = st.file_uploader("📎 Envie um arquivo .docx (opcional)", type=["docx"])

if uploaded_file:
    texto = extrair_texto_docx(uploaded_file)
    st.text_area("Texto extraído do .docx", texto, height=200)

if st.button("Gerar Relatório HTML com Exportação"):
    html = gerar_html_corrigido()
    st.download_button("📥 Baixar HTML com Exportação", data=html, file_name="relatorio_exportavel_funcional.html", mime="text/html")
    st.components.v1.html(html, height=950, scrolling=True)