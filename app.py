<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Testes - Novo Modelo de Fatura</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .document-info {
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .test-section {
            margin-bottom: 30px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }
        .test-item {
            margin-bottom: 15px;
            padding: 10px;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 3px;
            display: flex;
            align-items: center;
        }
        .test-item input[type="checkbox"] {
            margin-right: 10px;
            transform: scale(1.3);
        }
        .test-description {
            flex-grow: 1;
        }
        .test-category {
            font-weight: bold;
            color: #2c3e50;
            margin: 10px 0 5px 0;
        }
        .log-section {
            margin-top: 40px;
            padding: 20px;
            background-color: #f5f5f5;
            border-radius: 5px;
        }
        textarea {
            width: 100%;
            min-height: 100px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 3px;
            font-family: Arial, sans-serif;
        }
        .footer {
            margin-top: 30px;
            text-align: center;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #666;
            font-size: 0.9em;
        }
        h2 {
            color: #2c3e50;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }
        .status-badge {
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-left: 10px;
        }
        .pending {
            background-color: #fff3cd;
            color: #856404;
        }
        .completed {
            background-color: #d4edda;
            color: #155724;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Relatório de Testes - Novo Modelo de Fatura</h1>
        <p>Documentação: Jaguariúna - 350_2020</p>
        <p>Data: <span id="current-date"></span></p>
    </div>

    <div class="document-info">
        <h3>Informações do Documento Original</h3>
        <p><strong>Solicitante:</strong> Vanessa</p>
        <p><strong>Objetivo:</strong> Criar novo modelo de impressão seguindo fatura do cliente</p>
        <p><strong>Localização do Modelo:</strong> \\SRVINOVAMOBIL\geral\Desenvolvimento\Documentação\Projetos padrão\Solicitações\Jaguariúna\350_2020</p>
    </div>

    <div class="test-section">
        <h2>Testes de Conteúdo</h2>
        
        <div class="test-category">Informações do Contribuinte</div>
        <div class="test-item">
            <input type="checkbox" id="item1">
            <label for="item1" class="test-description">Verificar se o nome do contribuinte está presente e correto</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item2">
            <label for="item2" class="test-description">Verificar se o código do contribuinte está presente e correto</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item3">
            <label for="item3" class="test-description">Verificar se o endereço do contribuinte está presente e correto</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item4">
            <label for="item4" class="test-description">Verificar se o código do CPD está presente e correto (campo a definir com Raphael)</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item5">
            <label for="item5" class="test-description">Verificar se o vencimento está presente e correto</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item6">
            <label for="item6" class="test-description">Verificar se o total a pagar está presente e correto</label>
            <span class="status-badge pending">Pendente</span>
        </div>
    </div>

    <div class="test-section">
        <h2>Testes de Dados de Leitura</h2>
        
        <div class="test-item">
            <input type="checkbox" id="item7">
            <label for="item7" class="test-description">Verificar se mês/ano de referência está presente e correto</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item8">
            <label for="item8" class="test-description">Verificar se período de consumo está presente e correto</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item9">
            <label for="item9" class="test-description">Verificar se categoria está presente e correta</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item10">
            <label for="item10" class="test-description">Verificar se economia está presente e correta</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item11">
            <label for="item11" class="test-description">Verificar se leitura atual está presente e correta</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item12">
            <label for="item12" class="test-description">Verificar se leitura anterior está presente e correta</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item13">
            <label for="item13" class="test-description">Verificar se consumo real está presente e correto</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item14">
            <label for="item14" class="test-description">Verificar se hidrômetro está presente e correto</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item15">
            <label for="item15" class="test-description">Verificar se data do consumo (leitura) está presente e correta</label>
            <span class="status-badge pending">Pendente</span>
        </div>
    </div>

    <div class="test-section">
        <h2>Testes de Outras Informações</h2>
        
        <div class="test-item">
            <input type="checkbox" id="item16">
            <label for="item16" class="test-description">Verificar se ocorrência está presente e correta</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item17">
            <label for="item17" class="test-description">Verificar se data da próxima leitura está presente e correta</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item18">
            <label for="item18" class="test-description">Verificar se descrição dos serviços está presente e correta</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item19">
            <label for="item19" class="test-description">Verificar se valores dos serviços estão presentes e corretos</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item20">
            <label for="item20" class="test-description">Verificar se parâmetros da água estão presentes e corretos</label>
            <span class="status-badge pending">Pendente</span>
        </div>
    </div>

    <div class="test-section">
        <h2>Testes de Mensagens</h2>
        
        <div class="test-item">
            <input type="checkbox" id="item21">
            <label for="item21" class="test-description">Verificar se mensagem está de acordo com a regra do padrão</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item22">
            <label for="item22" class="test-description">Verificar se mensagem geral tipo 02 (instrução de pagamento) está presente</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-category">Regras de Mensagem Padrão</div>
        <div class="test-item">
            <input type="checkbox" id="item23">
            <label for="item23" class="test-description">Verificar formatação Default (Fonte nativa 7,0) - 37 caracteres, 6 linhas na mensagem 01 e 3 linhas na mensagem 02</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item24">
            <label for="item24" class="test-description">Verificar formatação Ari05Bpt.cpf - 45 caracteres, 6 linhas na mensagem 01, 3 linhas na mensagem 02</label>
            <span class="status-badge pending">Pendente</span>
        </div>
    </div>

    <div class="test-section">
        <h2>Testes de Histórico e Rodapé</h2>
        
        <div class="test-item">
            <input type="checkbox" id="item25">
            <label for="item25" class="test-description">Verificar se histórico de consumo dos últimos seis meses está presente e correto</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item26">
            <label for="item26" class="test-description">Verificar se rodapé contém código do contribuinte</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item27">
            <label for="item27" class="test-description">Verificar se rodapé contém C.A.D</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item28">
            <label for="item28" class="test-description">Verificar se rodapé contém mês/ano referência</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item29">
            <label for="item29" class="test-description">Verificar se rodapé contém número do documento</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item30">
            <label for="item30" class="test-description">Verificar se rodapé contém vencimento</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item31">
            <label for="item31" class="test-description">Verificar se rodapé contém total da fatura</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item32">
            <label for="item32" class="test-description">Verificar se rodapé contém nome</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item33">
            <label for="item33" class="test-description">Verificar se rodapé contém endereço</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item34">
            <label for="item34" class="test-description">Verificar se rodapé contém código de barras</label>
            <span class="status-badge pending">Pendente</span>
        </div>
    </div>

    <div class="test-section">
        <h2>Testes de Formatação e Layout</h2>
        
        <div class="test-item">
            <input type="checkbox" id="item35">
            <label for="item35" class="test-description">Verificar se nenhum campo ultrapassa os limites do layout</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item36">
            <label for="item36" class="test-description">Verificar se formatação está de acordo com o modelo enviado</label>
            <span class="status-badge pending">Pendente</span>
        </div>
    </div>

    <div class="test-section">
        <h2>Perguntas Pendentes com Raphael</h2>
        
        <div class="test-item">
            <input type="checkbox" id="item37" disabled>
            <label for="item37" class="test-description">Definir em qual campo será enviada a informação de Código do CPD</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item38" disabled>
            <label for="item38" class="test-description">Definir em qual campo será enviada a informação de Código do C.A.D</label>
            <span class="status-badge pending">Pendente</span>
        </div>
        
        <div class="test-item">
            <input type="checkbox" id="item39" disabled>
            <label for="item39" class="test-description">Confirmar se a mensagem de informativo de pagamento pode ser considerada a geral tipo 02</label>
            <span class="status-badge pending">Pendente</span>
        </div>
    </div>

    <div class="log-section">
        <h2>Log de Alterações</h2>
        <textarea placeholder="Registre aqui quaisquer observações, problemas encontrados ou alterações realizadas durante os testes..."></textarea>
        <button onclick="saveLog()" style="margin-top: 10px; padding: 8px 15px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;">Salvar Log</button>
    </div>

    <div class="footer">
        <p>Relatório gerado automaticamente com base na documentação do projeto</p>
        <p>© <span id="current-year"></span> - Todos os direitos reservados</p>
    </div>

    <script>
        // Atualiza a data atual
        document.getElementById('current-date').textContent = new Date().toLocaleDateString('pt-BR');
        document.getElementById('current-year').textContent = new Date().getFullYear();
        
        // Salvar estado dos checkboxes e logs no localStorage
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            const savedState = localStorage.getItem(checkbox.id);
            if (savedState) {
                checkbox.checked = savedState === 'true';
                if (checkbox.checked) {
                    const statusBadge = checkbox.parentElement.querySelector('.status-badge');
                    if (statusBadge) {
                        statusBadge.textContent = 'Concluído';
                        statusBadge.classList.remove('pending');
                        statusBadge.classList.add('completed');
                    }
                }
            }
            
            checkbox.addEventListener('change', function() {
                localStorage.setItem(this.id, this.checked);
                const statusBadge = this.parentElement.querySelector('.status-badge');
                if (statusBadge) {
                    if (this.checked) {
                        statusBadge.textContent = 'Concluído';
                        statusBadge.classList.remove('pending');
                        statusBadge.classList.add('completed');
                    } else {
                        statusBadge.textContent = 'Pendente';
                        statusBadge.classList.remove('completed');
                        statusBadge.classList.add('pending');
                    }
                }
            });
        });
        
        // Carregar log salvo
        const savedLog = localStorage.getItem('testLog');
        if (savedLog) {
            document.querySelector('.log-section textarea').value = savedLog;
        }
        
        function saveLog() {
            const logText = document.querySelector('.log-section textarea').value;
            localStorage.setItem('testLog', logText);
            alert('Log salvo com sucesso!');
        }
    </script>
</body>
</html>
Aplicação Streamlit Integrada com DeepSeek API
python
# app.py
import streamlit as st
import os
import requests
from datetime import datetime
import base64
import time

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
    Analise o seguinte documento e extraia todos os requisitos e itens que precisam ser testados.
    Retorne uma lista organizada em categorias, formatada como Markdown.
    
    Documento:
    {content}
    
    Estrutura desejada:
    ### Categoria 1
    - [ ] Item de teste 1
    - [ ] Item de teste 2
    
    ### Categoria 2
    - [ ] Item de teste 3
    """
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Você é um assistente especializado em análise de documentos técnicos e criação de planos de teste."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
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
        .test-category {{
            font-weight: bold;
            color: #2c3e50;
            margin: 10px 0 5px 0;
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
        .status-badge {{
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-left: 10px;
        }}
        .pending {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .completed {{
            background-color: #d4edda;
            color: #155724;
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
        {document_info.get('content', '')}
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
        // Atualiza a data atual
        document.getElementById('current-date').textContent = new Date().toLocaleDateString('pt-BR');
        document.getElementById('current-year').textContent = new Date().getFullYear();
        
        // Salvar estado dos checkboxes e logs no localStorage
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {{
            const savedState = localStorage.getItem(checkbox.id);
            if (savedState) {{
                checkbox.checked = savedState === 'true';
                if (checkbox.checked) {{
                    const statusBadge = checkbox.parentElement.querySelector('.status-badge');
                    if (statusBadge) {{
                        statusBadge.textContent = 'Concluído';
                        statusBadge.classList.remove('pending');
                        statusBadge.classList.add('completed');
                    }}
                }}
            }}
            
            checkbox.addEventListener('change', function() {{
                localStorage.setItem(this.id, this.checked);
                const statusBadge = this.parentElement.querySelector('.status-badge');
                if (statusBadge) {{
                    if (this.checked) {{
                        statusBadge.textContent = 'Concluído';
                        statusBadge.classList.remove('pending');
                        statusBadge.classList.add('completed');
                    }} else {{
                        statusBadge.textContent = 'Pendente';
                        statusBadge.classList.remove('completed');
                        statusBadge.classList.add('pending');
                    }}
                }}
            }});
        }});
        
        // Carregar log salvo
        const savedLog = localStorage.getItem('testLog');
        if (savedLog) {{
            document.querySelector('.log-section textarea').value = savedLog;
        }}
        
        function saveLog() {{
            const logText = document.querySelector('.log-section textarea').value;
            localStorage.setItem('testLog', logText);
            alert('Log salvo com sucesso!');
        }}
    </script>
</body>
</html>
    """
    return html_content

def markdown_to_html_test_items(markdown_content):
    """Converte markdown de itens de teste para HTML"""
    html_items = []
    current_category = ""
    
    for line in markdown_content.split('\n'):
        if line.startswith('### '):
            current_category = line[4:].strip()
            html_items.append(f'<div class="test-section"><h2>{current_category}</h2>')
        elif line.startswith('- [ ] '):
            item_text = line[6:].strip()
            item_id = f"item{len(html_items)}"
            html_items.append(f"""
            <div class="test-item">
                <input type="checkbox" id="{item_id}">
                <label for="{item_id}" class="test-description">{item_text}</label>
                <span class="status-badge pending">Pendente</span>
            </div>
            """)
    
    # Fecha a última seção se existir
    if current_category:
        html_items.append('</div>')
    
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
    content = ""
    if uploaded_file.type == "text/plain":
        content = str(uploaded_file.read(), "utf-8")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        from docx import Document
        doc = Document(uploaded_file)
        content = "\n".join([para.text for para in doc.paragraphs])
    
    return {
        "filename": uploaded_file.name,
        "content": content[:1000] + "..." if len(content) > 1000 else content,
        "full_content": content
    }

def main():
    st.title("Gerador de Relatórios de Teste")
    st.subheader("Converta documentos em relatórios de teste HTML com IA")
    
    # Upload do arquivo
    uploaded_file = st.file_uploader("Carregue seu arquivo (DOCX ou TXT)", type=['docx', 'txt'])
    
    if uploaded_file is not None:
        # Extrair informações do documento
        with st.spinner("Analisando documento..."):
            document_info = extract_document_info(uploaded_file)
            st.session_state.document_info = document_info
        
        # Exibir prévia do conteúdo
        st.subheader("Prévia do Documento")
        st.text_area("Conteúdo extraído", document_info["content"], height=200)
        
        # Botão para análise com DeepSeek
        if st.button("Analisar com DeepSeek AI"):
            if not DEEPSEEK_API_KEY:
                st.error("Chave da API DeepSeek não configurada. Por favor, configure a variável de ambiente DEEPSEEK_API_KEY.")
                return
            
            with st.spinner("Processando com DeepSeek AI..."):
                start_time = time.time()
                analysis_result = analyze_with_deepseek(document_info["full_content"])
                
                if analysis_result:
                    st.session_state.analysis_result = analysis_result
                    st.success(f"Análise concluída em {time.time() - start_time:.2f} segundos")
                    
                    # Mostrar resultados da análise
                    st.subheader("Resultados da Análise")
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
                    
                    st.markdown(get_binary_file_downloader_html(output_file, "Relatório de Testes"), unsafe_allow_html=True)
                    
                    # Limpar arquivo temporário
                    os.remove(output_file)

if __name__ == "__main__":
    main()