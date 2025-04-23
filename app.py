# app.py
import streamlit as st
from docx import Document
import PyPDF2
from io import BytesIO
import json
from datetime import datetime

def extract_text(uploaded_file):
    """Extrai texto de arquivos DOCX ou PDF"""
    try:
        if uploaded_file.name.endswith('.docx'):
            doc = Document(BytesIO(uploaded_file.getvalue()))
            return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        elif uploaded_file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(BytesIO(uploaded_file.getvalue()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        return None
    except Exception as e:
        st.error(f"Erro na extração: {str(e)}")
        return None

def generate_html_report(test_items, filename, client_name):
    """Gera um relatório HTML interativo personalizado"""
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Controle de Testes - {client_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 20px;
            color: #333;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #eee;
        }}
        .logo {{
            height: 80px;
            margin-bottom: 20px;
        }}
        .client-info {{
            background-color: #f0f8ff;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .info-row {{
            display: flex;
            margin-bottom: 15px;
            align-items: center;
        }}
        .info-label {{
            width: 150px;
            font-weight: bold;
        }}
        .info-input {{
            flex-grow: 1;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .date-input {{
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .test-item {{
            margin-bottom: 10px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 5px;
            display: flex;
            align-items: center;
        }}
        .test-item input {{
            margin-right: 15px;
            transform: scale(1.5);
        }}
        .progress-container {{
            margin: 20px 0;
            background-color: #f0f0f0;
            border-radius: 10px;
            height: 20px;
        }}
        .progress-bar {{
            height: 100%;
            border-radius: 10px;
            background-color: #4CAF50;
            width: 0%;
            transition: width 0.3s;
        }}
        .button {{
            padding: 10px 15px;
            margin: 5px;
            background-color: #2c7be5;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
        }}
        .button:hover {{
            background-color: #1a68d1;
        }}
        .report-container {{
            margin-top: 30px;
            padding: 20px;
            background-color: #f5f8fa;
            border-radius: 5px;
            display: none;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: #777;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <img src="https://inovamobil.com.br/wp-content/uploads/2023/06/Inovamobil-azul.svg" alt="Logo Inovamobil" class="logo">
        <h1>Controle de Testes</h1>
        <h2>{client_name}</h2>
    </div>

    <div class="client-info">
        <div class="info-row">
            <div class="info-label">Nome do Responsável:</div>
            <input type="text" id="responsibleName" class="info-input" placeholder="Digite o nome do responsável">
        </div>
        <div class="info-row">
            <div class="info-label">Data do Teste:</div>
            <input type="date" id="testDate" class="date-input" value="{datetime.now().strftime('%Y-%m-%d')}">
        </div>
    </div>

    <div class="progress-container">
        <div class="progress-bar" id="progressBar"></div>
    </div>
    <div style="text-align: center; margin-bottom: 20px;">
        <span id="progressText">0% Concluído (0/{len(test_items)})</span>
    </div>

    <h3>Itens de Teste</h3>
    <div id="testItemsContainer">
        {''.join([
            f'<div class="test-item" data-id="{i}"><input type="checkbox" id="item{i}">'
            f'<label for="item{i}">{item.replace("[ ]", "").replace("[x]", "")}</label></div>'
            for i, item in enumerate(test_items)
        ])}
    </div>

    <div style="text-align: center; margin: 30px 0;">
        <button class="button" onclick="saveProgress()">Salvar Progresso</button>
        <button class="button" onclick="generateAdjustmentReport()">Relatório de Ajustes</button>
        <button class="button" onclick="resetTests()">Reiniciar Testes</button>
    </div>

    <div id="adjustmentReport" class="report-container">
        <h3>Relatório de Ajustes</h3>
        <div id="pendingItemsList"></div>
        <div style="margin-top: 15px;">
            <label for="adjustmentNotes">Observações:</label>
            <textarea id="adjustmentNotes" style="width: 100%; min-height: 80px; margin-top: 5px;"></textarea>
        </div>
        <button class="button" onclick="printAdjustmentReport()" style="margin-top: 10px;">Imprimir Relatório</button>
    </div>

    <div class="footer">
        <p>Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>

    <script>
        // Inicializa variáveis
        const totalItems = {len(test_items)};
        let testState = Array(totalItems).fill(false);
        const clientName = "{client_name}";

        // Atualiza progresso
        function updateProgress() {{
            const checkedCount = testState.filter(x => x).length;
            const percentage = Math.round((checkedCount / totalItems) * 100);
            document.getElementById('progressBar').style.width = percentage + '%';
            document.getElementById('progressText').textContent = 
                percentage + '% Concluído (' + checkedCount + '/' + totalItems + ')';
        }}

        // Gera relatório de ajustes
        function generateAdjustmentReport() {{
            const pendingItems = [];
            document.querySelectorAll('#testItemsContainer .test-item').forEach((item, index) => {{
                if (!testState[index]) {{
                    const itemText = item.querySelector('label').textContent.trim();
                    pendingItems.push('<div>- ' + itemText + '</div>');
                }}
            }});
            
            const reportContainer = document.getElementById('adjustmentReport');
            const pendingList = document.getElementById('pendingItemsList');
            
            if (pendingItems.length > 0) {{
                pendingList.innerHTML = 
                    '<p><strong>Itens pendentes de teste (' + pendingItems.length + '):</strong></p>' +
                    pendingItems.join('');
                reportContainer.style.display = 'block';
            }} else {{
                alert('Todos os itens foram testados!');
                reportContainer.style.display = 'none';
            }}
        }}

        // Imprime relatório de ajustes
        function printAdjustmentReport() {{
            const responsibleName = document.getElementById('responsibleName').value || 'Não informado';
            const testDate = document.getElementById('testDate').value;
            const notes = document.getElementById('adjustmentNotes').value || 'Nenhuma observação';
            const pendingItems = document.getElementById('pendingItemsList').innerHTML;
            
            const win = window.open('', '_blank');
            win.document.write(`
                <html>
                    <head>
                        <title>Relatório de Ajustes - ${clientName}</title>
                        <style>
                            body {{ font-family: Arial; padding: 20px; }}
                            h1 {{ color: #2c7be5; }}
                            hr {{ border: 0.5px solid #eee; }}
                        </style>
                    </head>
                    <body>
                        <h1>Relatório de Ajustes - ${clientName}</h1>
                        <p><strong>Responsável:</strong> ${responsibleName}</p>
                        <p><strong>Data:</strong> ${testDate}</p>
                        <hr>
                        ${pendingItems}
                        <hr>
                        <p><strong>Observações:</strong></p>
                        <p>${notes}</p>
                        <script>
                            window.onload = function() {{ window.print(); }};
                        <\/script>
                    </body>
                </html>
            `);
            win.document.close();
        }}

        // Salva progresso
        function saveProgress() {{
            localStorage.setItem('testProgress', JSON.stringify(testState));
            localStorage.setItem('responsibleName', document.getElementById('responsibleName').value);
            localStorage.setItem('testDate', document.getElementById('testDate').value);
            alert('Progresso salvo com sucesso!');
        }}

        // Reinicia testes
        function resetTests() {{
            if (confirm('Tem certeza que deseja reiniciar todos os testes?')) {{
                testState = Array(totalItems).fill(false);
                document.querySelectorAll('#testItemsContainer input[type="checkbox"]').forEach(cb => {{
                    cb.checked = false;
                }});
                updateProgress();
            }}
        }}

        // Carrega dados salvos
        function loadProgress() {{
            const savedProgress = localStorage.getItem('testProgress');
            const savedName = localStorage.getItem('responsibleName');
            const savedDate = localStorage.getItem('testDate');
            
            if (savedProgress) {{
                testState = JSON.parse(savedProgress);
                document.querySelectorAll('#testItemsContainer input[type="checkbox"]').forEach((cb, i) => {{
                    cb.checked = testState[i];
                }});
            }}
            
            if (savedName) document.getElementById('responsibleName').value = savedName;
            if (savedDate) document.getElementById('testDate').value = savedDate;
            
            updateProgress();
        }}

        // Configura eventos
        document.querySelectorAll('#testItemsContainer input[type="checkbox"]').forEach((cb, i) => {{
            cb.addEventListener('change', function() {{
                testState[i] = this.checked;
                updateProgress();
            }});
        }});

        // Inicializa
        window.onload = function() {{
            loadProgress();
        }};
    </script>
</body>
</html>
    """
    return html_content

def extract_client_name(content):
    """Extrai o nome do cliente do conteúdo do documento"""
    lines = content.split('\n')
    for line in lines:
        if any(keyword in line.lower() for keyword in ['cliente', 'projeto', 'jaguar']):
            return line.strip()
    return "Cliente não identificado"

def main():
    st.set_page_config(page_title="Gerador de Controle de Testes", layout="centered")
    
    st.title("📋 Gerador de Controle de Testes")
    st.markdown("""
    ### Como usar:
    1. Faça upload de um arquivo DOCX ou PDF
    2. O sistema identificará automaticamente o nome do cliente
    3. Baixe o relatório HTML personalizado
    4. Abra o HTML em qualquer navegador para usar todas as funcionalidades
    """)
    
    uploaded_file = st.file_uploader(
        "Arraste e solte seu arquivo aqui (DOCX ou PDF)",
        type=['docx', 'pdf'],
        accept_multiple_files=False,
        help="Tamanho máximo: 200MB"
    )
    
    if uploaded_file:
        with st.spinner("Processando arquivo..."):
            try:
                text_content = extract_text(uploaded_file)
                
                if text_content:
                    client_name = extract_client_name(text_content)
                    
                    lines = [line.strip() for line in text_content.split('\n') if line.strip()]
                    test_items = [f"- [ ] {line[:250]}" for line in lines if len(line.split()) > 3][:50]
                    
                    if test_items:
                        html_report = generate_html_report(test_items, uploaded_file.name, client_name)
                        
                        st.success("✅ Relatório personalizado gerado com sucesso!")
                        st.balloons()
                        
                        st.download_button(
                            label="⬇️ Baixar Controle de Testes",
                            data=html_report,
                            file_name=f"controle_testes_{client_name.replace(' ', '_')}.html",
                            mime="text/html"
                        )
                    else:
                        st.warning("Não foram identificados itens de teste no documento.")
                else:
                    st.error("Não foi possível extrair conteúdo do arquivo")
            
            except Exception as e:
                st.error(f"Erro durante o processamento: {str(e)}")

if __name__ == "__main__":
    main()