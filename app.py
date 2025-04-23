# app.py
import streamlit as st
from docx import Document
import PyPDF2
from io import BytesIO
import json
from datetime import datetime

def extract_text(uploaded_file):
    """Extrai texto de arquivos DOCX ou PDF com tratamento robusto de erros"""
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
        st.error(f"Erro ao processar arquivo: {str(e)}")
        return None

def generate_html_report(test_items, filename):
    """Gera um relatório HTML interativo completo"""
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Testes - {filename}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
            background-color: #f9f9f9;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background-color: #2c3e50;
            color: white;
            border-radius: 5px;
        }}
        .logo {{
            height: 60px;
            margin-bottom: 15px;
        }}
        .info-section {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .info-row {{
            display: flex;
            margin-bottom: 15px;
            align-items: center;
        }}
        .info-label {{
            width: 120px;
            font-weight: bold;
        }}
        .info-input {{
            flex: 1;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }}
        .progress-container {{
            margin: 25px 0;
            background-color: #ecf0f1;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
        }}
        .progress-bar {{
            height: 100%;
            background-color: #27ae60;
            width: 0%;
            transition: width 0.3s ease;
        }}
        .progress-text {{
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
            color: #2c3e50;
        }}
        .test-section {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .test-item {{
            margin-bottom: 10px;
            padding: 15px;
            background-color: #f8f9fa;
            border-radius: 5px;
            display: flex;
            align-items: center;
            transition: background-color 0.2s;
        }}
        .test-item:hover {{
            background-color: #e9ecef;
        }}
        .test-item input {{
            margin-right: 15px;
            transform: scale(1.3);
            cursor: pointer;
        }}
        .test-item label {{
            flex: 1;
            cursor: pointer;
        }}
        .action-buttons {{
            display: flex;
            justify-content: center;
            gap: 10px;
            margin: 25px 0;
        }}
        .button {{
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.2s;
        }}
        .button:hover {{
            background-color: #2980b9;
        }}
        .button.reset {{
            background-color: #e74c3c;
        }}
        .button.reset:hover {{
            background-color: #c0392b;
        }}
        .log-section {{
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-top: 30px;
        }}
        .log-entries {{
            max-height: 200px;
            overflow-y: auto;
            margin-bottom: 15px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 5px;
        }}
        .log-entry {{
            margin-bottom: 5px;
            padding: 5px;
            font-size: 0.9em;
            border-bottom: 1px solid #eee;
        }}
        textarea {{
            width: 100%;
            min-height: 80px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            color: #7f8c8d;
            font-size: 0.9em;
            border-top: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <div class="header">
        <img src="https://inovamobil.com.br/wp-content/uploads/2023/06/Inovamobil-azul.svg" alt="Logo Inovamobil" class="logo">
        <h1>Controle de Testes</h1>
        <p>Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>

    <div class="info-section">
        <div class="info-row">
            <div class="info-label">Cliente/Projeto:</div>
            <input type="text" id="projectName" class="info-input" placeholder="Digite o nome do cliente/projeto">
        </div>
        <div class="info-row">
            <div class="info-label">Responsável:</div>
            <input type="text" id="responsibleName" class="info-input" placeholder="Digite seu nome">
        </div>
        <div class="info-row">
            <div class="info-label">Data do Teste:</div>
            <input type="date" id="testDate" class="info-input" value="{datetime.now().strftime('%Y-%m-%d')}">
        </div>
    </div>

    <div class="progress-container">
        <div class="progress-bar" id="progressBar"></div>
    </div>
    <div class="progress-text" id="progressText">0% Concluído (0/{len(test_items)})</div>

    <div class="test-section">
        <h2>Itens de Teste</h2>
        <div id="testItemsContainer">
            {''.join([
                f'<div class="test-item"><input type="checkbox" id="item{i}">'
                f'<label for="item{i}">{item.replace("[ ]", "").replace("[x]", "")}</label></div>'
                for i, item in enumerate(test_items)
            ])}
        </div>
    </div>

    <div class="action-buttons">
        <button class="button" onclick="saveProgress()">Salvar Progresso</button>
        <button class="button" onclick="exportReport()">Exportar Relatório</button>
        <button class="button reset" onclick="resetTests()">Reiniciar Testes</button>
    </div>

    <div class="log-section">
        <h2>Registro de Atividades</h2>
        <div class="log-entries" id="logEntries"></div>
        <textarea id="logInput" placeholder="Adicione uma observação..."></textarea>
        <button class="button" onclick="addLogEntry()">Adicionar ao Log</button>
    </div>

    <div class="footer">
        <p>Relatório gerado automaticamente - Inovamobil</p>
    </div>

    <script>
        // Inicialização
        const totalItems = {len(test_items)};
        let testState = Array(totalItems).fill(false);
        let logEntries = [];
        
        // Elementos importantes
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const testItemsContainer = document.getElementById('testItemsContainer');
        const logEntriesContainer = document.getElementById('logEntries');
        const logInput = document.getElementById('logInput');
        
        // Atualiza a barra de progresso
        function updateProgress() {{
            const checkedCount = testState.filter(Boolean).length;
            const percentage = Math.round((checkedCount / totalItems) * 100);
            
            progressBar.style.width = percentage + '%';
            progressText.textContent = percentage + '% Concluído (' + checkedCount + '/' + totalItems + ')';
            
            // Atualiza cores conforme progresso
            if (percentage < 30) {{
                progressBar.style.backgroundColor = '#e74c3c';
            }} else if (percentage < 70) {{
                progressBar.style.backgroundColor = '#f39c12';
            }} else {{
                progressBar.style.backgroundColor = '#27ae60';
            }}
        }}
        
        // Adiciona entrada no log
        function addLogEntry(text) {{
            const now = new Date();
            const timestamp = now.toLocaleString('pt-BR');
            const entryText = text || logInput.value;
            
            if (!entryText.trim()) return;
            
            const entry = {{
                timestamp: timestamp,
                text: entryText,
                progress: testState.filter(Boolean).length + '/' + totalItems
            }};
            
            logEntries.push(entry);
            renderLogEntries();
            
            if (!text) {{
                logInput.value = '';
                alert('Entrada adicionada ao log!');
            }}
        }}
        
        // Renderiza as entradas do log
        function renderLogEntries() {{
            logEntriesContainer.innerHTML = logEntries.map(entry => `
                <div class="log-entry">
                    <strong>[${entry.timestamp}]</strong> (${entry.progress}) - ${entry.text}
                </div>
            `).join('');
        }}
        
        // Salva o progresso no localStorage
        function saveProgress() {{
            const projectName = document.getElementById('projectName').value;
            const responsibleName = document.getElementById('responsibleName').value;
            const testDate = document.getElementById('testDate').value;
            
            const data = {{
                testState: testState,
                logEntries: logEntries,
                projectName: projectName,
                responsibleName: responsibleName,
                testDate: testDate,
                lastSaved: new Date().toISOString()
            }};
            
            localStorage.setItem('testReportData', JSON.stringify(data));
            addLogEntry('Progresso salvo com sucesso');
        }}
        
        // Carrega o progresso salvo
        function loadProgress() {{
            const savedData = localStorage.getItem('testReportData');
            if (!savedData) return;
            
            try {{
                const data = JSON.parse(savedData);
                
                // Carrega estado dos checkboxes
                if (data.testState && data.testState.length === totalItems) {{
                    testState = data.testState;
                    document.querySelectorAll('#testItemsContainer input').forEach((checkbox, i) => {{
                        checkbox.checked = testState[i];
                    }});
                }}
                
                // Carrega log de atividades
                if (data.logEntries) {{
                    logEntries = data.logEntries;
                    renderLogEntries();
                }}
                
                // Carrega informações adicionais
                if (data.projectName) document.getElementById('projectName').value = data.projectName;
                if (data.responsibleName) document.getElementById('responsibleName').value = data.responsibleName;
                if (data.testDate) document.getElementById('testDate').value = data.testDate;
                
                updateProgress();
                addLogEntry('Progresso anterior carregado');
            }} catch (e) {{
                console.error('Erro ao carregar dados salvos:', e);
            }}
        }}
        
        // Exporta relatório completo
        function exportReport() {{
            const projectName = document.getElementById('projectName').value || 'Não informado';
            const responsibleName = document.getElementById('responsibleName').value || 'Não informado';
            const testDate = document.getElementById('testDate').value || 'Não informada';
            
            const reportData = {{
                metadata: {{
                    title: 'Relatório de Testes',
                    project: projectName,
                    responsible: responsibleName,
                    date: testDate,
                    generated: new Date().toISOString(),
                    progress: testState.filter(Boolean).length + '/' + totalItems
                }},
                testItems: Array.from(document.querySelectorAll('.test-item label')).map(el => ({{
                    text: el.textContent.trim(),
                    checked: el.previousElementSibling.checked
                }})),
                logEntries: logEntries
            }};
            
            const blob = new Blob([JSON.stringify(reportData, null, 2)], {{ type: 'application/json' }});
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = `relatorio_testes_${{projectName.replace(/[^a-z0-9]/gi, '_')}}_${{new Date().toISOString().slice(0,10)}}.json`;
            a.click();
            
            addLogEntry('Relatório exportado para JSON');
        }}
        
        // Reinicia todos os testes
        function resetTests() {{
            if (!confirm('Tem certeza que deseja reiniciar todos os testes?')) return;
            
            testState = Array(totalItems).fill(false);
            document.querySelectorAll('#testItemsContainer input').forEach(checkbox => {{
                checkbox.checked = false;
            }});
            
            updateProgress();
            addLogEntry('Todos os testes foram reiniciados');
        }}
        
        // Configura eventos
        function setupEventListeners() {{
            // Eventos dos checkboxes
            document.querySelectorAll('#testItemsContainer input').forEach((checkbox, i) => {{
                checkbox.addEventListener('change', () => {{
                    testState[i] = checkbox.checked;
                    updateProgress();
                    addLogEntry(`Item ${{i+1}} ${{checkbox.checked ? 'marcado' : 'desmarcado'}}`);
                }});
            }});
            
            // Evento para adicionar log com Enter
            logInput.addEventListener('keypress', (e) => {{
                if (e.key === 'Enter') {{
                    addLogEntry();
                }}
            }});
        }}
        
        // Inicialização completa
        function init() {{
            setupEventListeners();
            loadProgress();
            updateProgress();
        }}
        
        // Inicia quando o DOM estiver pronto
        document.addEventListener('DOMContentLoaded', init);
    </script>
</body>
</html>
    """
    return html_content

def main():
    st.set_page_config(
        page_title="Gerador de Relatórios de Teste",
        page_icon="✅",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    
    st.title("📋 Gerador de Relatórios de Teste")
    st.markdown("""
    **Como usar:**
    1. Faça upload de um documento (DOCX ou PDF)
    2. O sistema extrairá o conteúdo automaticamente
    3. Baixe o relatório HTML interativo
    4. Abra no navegador e comece a testar!
    """)
    
    with st.expander("Configurações avançadas", expanded=False):
        max_items = st.slider("Número máximo de itens a extrair", 10, 100, 50)
        min_words = st.slider("Mínimo de palavras por item", 1, 10, 3)
    
    uploaded_file = st.file_uploader(
        "Arraste e solte seu arquivo aqui",
        type=['docx', 'pdf'],
        accept_multiple_files=False,
        help="Formatos suportados: DOCX, PDF (até 200MB)"
    )
    
    if uploaded_file is not None:
        with st.spinner("Processando documento..."):
            try:
                text_content = extract_text(uploaded_file)
                
                if text_content:
                    # Processa o conteúdo para extrair itens de teste
                    lines = [line.strip() for line in text_content.split('\n') if line.strip()]
                    test_items = [
                        f"- {line[:250]}" 
                        for line in lines 
                        if len(line.split()) >= min_words
                    ][:max_items]
                    
                    if test_items:
                        html_report = generate_html_report(test_items, uploaded_file.name)
                        
                        st.success("✅ Relatório gerado com sucesso!")
                        st.balloons()
                        
                        st.download_button(
                            label="⬇️ Baixar Relatório HTML",
                            data=html_report,
                            file_name=f"relatorio_testes_{datetime.now().strftime('%Y%m%d_%H%M')}.html",
                            mime="text/html",
                            help="Clique para baixar o relatório interativo"
                        )
                        
                        st.markdown("""
                        **Instruções pós-download:**
                        1. Abra o arquivo HTML em qualquer navegador
                        2. Preencha as informações do projeto
                        3. Marque os itens conforme for testando
                        4. Use o botão 'Salvar Progresso' para guardar seu trabalho
                        """)
                    else:
                        st.warning("⚠️ Não foram encontrados itens testáveis no documento.")
                        st.info("Tente ajustar os parâmetros de extração na seção 'Configurações avançadas'")
                else:
                    st.error("❌ Não foi possível extrair texto do documento.")
            
            except Exception as e:
                st.error(f"Erro durante o processamento: {str(e)}")
                st.error("Por favor, verifique o arquivo e tente novamente.")

if __name__ == "__main__":
    main()