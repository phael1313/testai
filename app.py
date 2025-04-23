# app.py
import streamlit as st
from docx import Document
import PyPDF2
from io import BytesIO
import traceback
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

def generate_html_report(test_items, filename):
    """Gera um relatório HTML completo"""
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Testes - {filename}</title>
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
        .test-item {{
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f9f9f9;
            border-left: 4px solid #4CAF50;
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
        <h1>Relatório de Testes</h1>
        <p>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        <p>Arquivo original: {filename}</p>
    </div>

    <h2>Itens de Teste</h2>
    {''.join([f'<div class="test-item">{item.replace("[ ]", "☐").replace("[x]", "✓")}</div>' for item in test_items])}

    <div class="footer">
        <p>Relatório gerado automaticamente</p>
    </div>
</body>
</html>
    """
    return html_content

def main():
    st.set_page_config(page_title="Gerador de Testes", layout="centered")
    
    st.title("📋 Transforme Documentos em Casos de Teste")
    st.markdown("""
    ### Como usar:
    1. Faça upload de um arquivo DOCX ou PDF
    2. Aguarde o processamento
    3. Baixe o relatório completo em HTML
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
                    # Processa apenas linhas relevantes
                    lines = [line.strip() for line in text_content.split('\n') if line.strip()]
                    test_items = [f"- [ ] {line[:250]}" for line in lines if len(line.split()) > 3][:100]
                    
                    if test_items:
                        html_report = generate_html_report(test_items, uploaded_file.name)
                        
                        st.success("✅ Relatório gerado com sucesso!")
                        st.balloons()
                        
                        st.download_button(
                            label="⬇️ Baixar Relatório HTML",
                            data=html_report,
                            file_name=f"relatorio_testes_{uploaded_file.name.split('.')[0]}.html",
                            mime="text/html"
                        )
                    else:
                        st.warning("Não foram identificados itens de teste no documento.")
                else:
                    st.error("Não foi possível extrair conteúdo do arquivo")
            
            except Exception as e:
                st.error("Erro durante o processamento")
                st.code(traceback.format_exc())

if __name__ == "__main__":
    main()