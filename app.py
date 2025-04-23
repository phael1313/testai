# app.py
import streamlit as st
import os
from docx import Document
import PyPDF2
from io import BytesIO
import traceback

def extract_text(uploaded_file):
    """Extrai texto de arquivos DOCX ou PDF com tratamento robusto de erros"""
    try:
        if uploaded_file.name.endswith('.docx'):
            doc = Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])
        elif uploaded_file.name.endswith('.pdf'):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            return text
        else:
            st.error("Formato de arquivo não suportado")
            return None
    except Exception as e:
        st.error(f"Erro ao extrair texto: {str(e)}")
        st.text(traceback.format_exc())  # Log detalhado do erro
        return None

def generate_test_items(text_content):
    """Gera itens de teste básicos a partir do texto"""
    if not text_content:
        return []
    
    # Extrai linhas que parecem conter requisitos
    test_items = []
    for line in text_content.split('\n'):
        line = line.strip()
        if line and len(line.split()) > 3:  # Filtra linhas muito curtas
            test_items.append(f"- [ ] Verificar: {line[:200]}")  # Limita o tamanho
    
    return test_items[:50]  # Limita a 50 itens

def main():
    st.set_page_config(page_title="Gerador de Testes", layout="wide")
    
    st.title("📋 Transforme Documentos em Casos de Teste")
    st.markdown("""
    ### Como usar:
    1. Faça upload de um arquivo DOCX ou PDF
    2. O sistema extrairá o conteúdo automaticamente
    3. Gere os itens de teste
    """)
    
    uploaded_file = st.file_uploader(
        "Arraste e solte seu arquivo aqui",
        type=['docx', 'pdf'],
        help="Formatos suportados: DOCX, PDF"
    )
    
    if uploaded_file is not None:
        with st.spinner("Processando arquivo..."):
            try:
                # Extrai o texto
                text_content = extract_text(uploaded_file)
                
                if text_content:
                    # Gera itens de teste
                    test_items = generate_test_items(text_content)
                    
                    # Exibe resultados
                    st.success("✅ Arquivo processado com sucesso!")
                    st.subheader("Itens de Teste Gerados")
                    
                    if test_items:
                        st.markdown("\n".join(test_items))
                    else:
                        st.warning("Nenhum item de teste identificado automaticamente.")
                        
                    # Opção para download
                    st.download_button(
                        label="📥 Baixar Itens de Teste",
                        data="\n".join(test_items),
                        file_name="itens_teste.md",
                        mime="text/markdown"
                    )
                else:
                    st.error("Não foi possível extrair conteúdo do arquivo")
            
            except Exception as e:
                st.error("Ocorreu um erro durante o processamento")
                st.code(traceback.format_exc())  # Mostra o traceback completo

if __name__ == "__main__":
    main()