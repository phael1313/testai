# app.py
import streamlit as st
import os
import requests
from datetime import datetime
import base64
import time
from docx import Document

# Configuração da API DeepSeek (com fallback)
DEEPSEEK_API_KEY = st.secrets.get("DEEPSEEK_API_KEY", os.getenv("DEEPSEEK_API_KEY", ""))
DEEPSEEK_API_URL = "https://api.deepseek.ai/v1/chat/completions"
TIMEOUT = 30  # segundos

def check_internet_connection():
    """Verifica se há conexão com a internet"""
    try:
        requests.get("https://google.com", timeout=5)
        return True
    except:
        return False

def analyze_with_deepseek(content):
    """Envia o conteúdo para análise pela API da DeepSeek com tratamento robusto de erros"""
    if not DEEPSEEK_API_KEY:
        st.error("Chave da API DeepSeek não configurada")
        return None
    
    if not check_internet_connection():
        st.error("Sem conexão com a internet")
        return None

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    prompt = f"""
    Analise este documento técnico e liste os itens de teste em markdown:
    {content}
    
    Formato:
    ### [Categoria]
    - [ ] Item de teste 1
    - [ ] Item de teste 2
    """
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(
            DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro na API: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado: {str(e)}")
        return None

def generate_simulation(content):
    """Gera uma simulação quando a API não está disponível"""
    # Análise simplificada do conteúdo
    important_lines = [line for line in content.split('\n') 
                      if any(keyword in line.lower() for keyword in ['test', 'verif', 'valid', 'confirm'])]
    
    if not important_lines:
        important_lines = content.split('\n')[:10]
    
    markdown = "### Itens de Teste Identificados\n"
    for i, line in enumerate(important_lines[:15]):  # Limita a 15 itens
        markdown += f"- [ ] {line.strip()}\n"
    
    return markdown

def main():
    st.set_page_config(page_title="Gerador de Relatórios", layout="wide")
    
    st.title("📋 Gerador de Relatórios de Teste")
    st.caption("Transforme documentos em planos de teste automatizados")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader(
        "Carregue seu documento (DOCX ou TXT)",
        type=['docx', 'txt'],
        help="Documento com requisitos ou especificações"
    )
    
    if uploaded_file:
        # Processamento do documento
        with st.spinner("Processando documento..."):
            doc_text = extract_text(uploaded_file)
            
            # Seção de análise
            st.subheader("Análise do Documento")
            
            # Tenta usar a API ou fallback para simulação
            analysis_result = None
            if DEEPSEEK_API_KEY:
                with st.spinner("Conectando à DeepSeek AI..."):
                    analysis_result = analyze_with_deepseek(doc_text)
            
            if not analysis_result:
                st.warning("Usando modo simulado (API não disponível)")
                analysis_result = generate_simulation(doc_text)
            
            # Geração do relatório
            if analysis_result:
                html_report = create_html_report(
                    filename=uploaded_file.name,
                    content=doc_text,
                    analysis=analysis_result
                )
                
                # Visualização e download
                st.subheader("Relatório Gerado")
                st.components.v1.html(html_report, height=800, scrolling=True)
                
                st.download_button(
                    label="⬇️ Baixar Relatório HTML",
                    data=html_report,
                    file_name="relatorio_testes.html",
                    mime="text/html"
                )

if __name__ == "__main__":
    main()