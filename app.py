# app.py
import streamlit as st
import os
import requests
from datetime import datetime
import base64
import time
from docx import Document

# Configuração da API DeepSeek
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", os.getenv("DEEPSEEK_API_KEY"))
DEEPSEEK_API_URL = "https://api.deepseek.ai/v1/chat/completions"

def analyze_with_deepseek(content):
    """Envia o conteúdo para análise pela API da DeepSeek"""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""
    Analise o seguinte documento técnico e extraia todos os requisitos e itens que precisam ser testados.
    Retorne uma lista organizada em categorias lógicas, formatada como Markdown.
    Para cada item, identifique claramente o que precisa ser verificado.
    
    Documento:
    {content}
    
    Formato de saída esperado:
    ### [Nome da Categoria]
    - [ ] Descrição clara do item a ser testado
    - [ ] Outro item de teste
    
    ### Outra Categoria
    - [ ] Mais itens de teste
    """
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Você é um especialista em análise de requisitos e criação de planos de teste."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Erro ao chamar API DeepSeek: {str(e)}")
        return None

def generate_html_report(document_info, test_items):
    """Gera o relatório HTML com base na análise"""
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Testes</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }}
        .document-info {{
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .test-section {{
            margin-bottom: 30px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }}
        .test-item {{
            margin-bottom: 15px;
            padding: 10px;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 3px;
            display: flex;
            align-items: center;
        }}
        .test-item input[type="checkbox"] {{
            margin-right: 10px;
            transform: scale(1.3);
        }}
        .test-description {{
            flex-grow: 1;
        }}
        .log-section {{
            margin-top: 40px;
            padding: 20px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }}
        textarea {{
            width: 100%;
            min-height: 100px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 3px;
            font-family: Arial, sans-serif;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #666;
            font-size: 0.9em;
        }}
        h2 {{
            color: #2c3e50;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Testes Automático</h1>
        <p>Documentação: {document_info.get('filename', 'Desconhecido')}</p>
        <p>Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
    </div>

    <div class="document-info">
        <h3>Informações do Documento Original</h3>
        <p>{document_info.get('summary', '')}</p>
    </div>

    {test_items}

    <div class="log-section">
        <h2>Log de Alterações</h2>
        <textarea placeholder="Registre aqui quaisquer observações, problemas encontrados ou alterações realizadas durante os testes..."></textarea>
        <button onclick="saveLog()" style="margin-top: 10px; padding: 8px 15px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">Salvar Log</button>
    </div>

    <div class="footer">
        <p>Relatório gerado automaticamente com base na documentação do projeto</p>
        <p>© {datetime.now().year} - Todos os direitos reservados</p>
    </div>

    <script>
        function saveLog() {{
            const logText = document.querySelector('.log-section textarea').value;
            localStorage.setItem('testLog', logText);
            alert('Log salvo com sucesso!');
        }}
        
        // Carregar log salvo se existir
        const savedLog = localStorage.getItem('testLog');
        if (savedLog) {{
            document.querySelector('.log-section textarea').value = savedLog;
        }}
    </script>
</body>
</html>
    """
    return html_content

def markdown_to_html_test_items(markdown_content):
    """Converte markdown de itens de teste para HTML"""
    if not markdown_content:
        return "<p>Nenhum item de teste identificado.</p>"
    
    html_items = []
    lines = markdown_content.split('\n')
    current_section = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith('### '):
            if current_section:
                html_items.append("</div>")  # Fecha a seção anterior
            current_section = line[4:].strip()
            html_items.append(f'<div class="test-section"><h2>{current_section}</h2>')
        elif line.startswith('- [ ] '):
            item_text = line[6:].strip()
            item_id = f"item{len(html_items)}"
            html_items.append(f'''
            <div class="test-item">
                <input type="checkbox" id="{item_id}">
                <label for="{item_id}" class="test-description">{item_text}</label>
            </div>
            ''')
    
    if current_section:
        html_items.append("</div>")  # Fecha a última seção
    
    return '\n'.join(html_items)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Gera um link para download do arquivo"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Baixar {file_label}</a>'
    return href

def extract_document_info(uploaded_file):
    """Extrai informações básicas do documento"""
    try:
        if uploaded_file.name.endswith('.docx'):
            doc = Document(uploaded_file)
            full_content = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        else:
            full_content = str(uploaded_file.read(), "utf-8")
        
        # Resumo do documento (primeiras 10 linhas relevantes)
        summary = "\n".join([line for line in full_content.split('\n') if line.strip()][:10])
        
        return {
            "filename": uploaded_file.name,
            "full_content": full_content,
            "summary": summary
        }
    except Exception as e:
        st.error(f"Erro ao ler documento: {str(e)}")
        return None

def main():
    st.set_page_config(page_title="Gerador de Relatórios de Teste", page_icon="✅")
    
    st.title("✅ Gerador de Relatórios de Teste")
    st.subheader("Converta documentos em relatórios de teste HTML com IA")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader(
        "Carregue seu arquivo (DOCX ou TXT)", 
        type=['docx', 'txt'],
        help="Envie o documento com os requisitos para gerar o relatório de testes"
    )
    
    if uploaded_file is not None:
        # Extrair informações do documento
        with st.spinner("Analisando documento..."):
            document_info = extract_document_info(uploaded_file)
            if not document_info:
                return
            
            st.session_state.document_info = document_info
        
        # Exibir prévia do conteúdo
        with st.expander("Visualizar conteúdo extraído"):
            st.text_area(
                "Conteúdo do documento", 
                document_info["full_content"], 
                height=200,
                label_visibility="collapsed"
            )
        
        # Seção de análise com DeepSeek
        st.subheader("Análise com IA")
        
        if not DEEPSEEK_API_KEY:
            st.warning("API Key da DeepSeek não configurada. A análise será simulada.")
        
        if st.button("Gerar Relatório de Testes", type="primary"):
            with st.spinner("Processando com DeepSeek AI..."):
                start_time = time.time()
                
                # Usar API real ou simulada
                if DEEPSEEK_API_KEY:
                    analysis_result = analyze_with_deepseek(document_info["full_content"])
                else:
                    # Simulação para demonstração
                    time.sleep(2)
                    analysis_result = """
### Informações do Contribuinte
- [ ] Verificar se o nome do contribuinte está presente
- [ ] Confirmar que o código do contribuinte está correto

### Dados de Leitura
- [ ] Validar mês/ano de referência
- [ ] Verificar período de consumo
"""
                
                if analysis_result:
                    st.session_state.analysis_result = analysis_result
                    st.success(f"Análise concluída em {time.time() - start_time:.2f} segundos")
                    
                    # Mostrar resultados da análise
                    with st.expander("Visualizar itens de teste identificados"):
                        st.markdown(analysis_result)
                    
                    # Converter para HTML
                    test_items_html = markdown_to_html_test_items(analysis_result)
                    html_report = generate_html_report(document_info, test_items_html)
                    st.session_state.html_report = html_report
                    
                    # Mostrar preview
                    st.subheader("Prévia do Relatório")
                    st.components.v1.html(html_report, height=600, scrolling=True)
                    
                    # Botão de download
                    output_file = f"relatorio_testes_{os.path.splitext(uploaded_file.name)[0]}.html"
                    with open(output_file, "w", encoding='utf-8') as f:
                        f.write(html_report)
                    
                    st.download_button(
                        label="Baixar Relatório HTML",
                        data=html_report,
                        file_name=output_file,
                        mime="text/html"
                    )
                    
                    # Limpar arquivo temporário
                    if os.path.exists(output_file):
                        os.remove(output_file)

if __name__ == "__main__":
    main()