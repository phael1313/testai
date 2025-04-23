# app.py
import streamlit as st
from docx import Document
import os
from datetime import datetime
import base64

def docx_to_html(docx_path):
    """Converte um documento DOCX para HTML formatado como relatório de teste"""
    doc = Document(docx_path)
    
    # Extrair conteúdo do documento
    content = "\n".join([para.text for para in doc.paragraphs])
    
    # Gerar HTML base
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
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Testes Automático</h1>
        <p>Documentação: {os.path.basename(docx_path)}</p>
        <p>Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
    </div>

    <div class="test-section">
        <h2>Requisitos do Documento</h2>
        {generate_test_items(content)}
    </div>

    <div class="log-section">
        <h2>Log de Alterações</h2>
        <textarea placeholder="Registre aqui quaisquer observações, problemas encontrados ou alterações realizadas durante os testes..."></textarea>
    </div>

    <div class="footer">
        <p>Relatório gerado automaticamente com base na documentação do projeto</p>
        <p>© {datetime.now().year} - Todos os direitos reservados</p>
    </div>

    <script>
        // Atualiza a data atual
        document.getElementById('current-date').textContent = new Date().toLocaleDateString('pt-BR');
        
        // Opcional: Salvar estado dos checkboxes no localStorage
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {{
            const savedState = localStorage.getItem(checkbox.id);
            if (savedState) checkbox.checked = savedState === 'true';
            
            checkbox.addEventListener('change', function() {{
                localStorage.setItem(this.id, this.checked);
            }});
        }});
    </script>
</body>
</html>
"""
    return html_content

def generate_test_items(content):
    """Gera itens de teste baseados no conteúdo do documento"""
    # Esta é uma versão simplificada - você pode melhorar com análise mais sofisticada
    items = []
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    for i, line in enumerate(lines):
        if line.startswith(('-', '#', '**')) and len(line) > 10:  # Filtra linhas relevantes
            clean_line = line.replace('-', '').replace('#', '').replace('*', '').strip()
            items.append(f"""
            <div class="test-item">
                <input type="checkbox" id="item{i}">
                <label for="item{i}" class="test-description">{clean_line}</label>
            </div>
            """)
    
    return "\n".join(items) if items else "<p>Nenhum item de teste identificado no documento.</p>"

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Gera um link para download do arquivo"""
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Baixar {file_label}</a>'
    return href

def main():
    st.title("Gerador de Relatórios de Teste")
    st.subheader("Converta documentos DOCX em relatórios de teste HTML")
    
    uploaded_file = st.file_uploader("Carregue seu arquivo DOCX", type=['docx'])
    
    if uploaded_file is not None:
        # Salvar arquivo temporariamente
        temp_file = f"temp_{uploaded_file.name}"
        with open(temp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Converter para HTML
        html_content = docx_to_html(temp_file)
        
        # Salvar HTML
        output_file = f"relatorio_testes_{os.path.splitext(uploaded_file.name)[0]}.html"
        with open(output_file, "w", encoding='utf-8') as f:
            f.write(html_content)
        
        # Mostrar preview
        st.subheader("Prévia do Relatório")
        st.components.v1.html(html_content, height=600, scrolling=True)
        
        # Botão de download
        st.markdown(get_binary_file_downloader_html(output_file, "Relatório de Testes"), unsafe_allow_html=True)
        
        # Limpar arquivos temporários
        os.remove(temp_file)
        os.remove(output_file)

if __name__ == "__main__":
    main()