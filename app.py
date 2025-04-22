
import os
from flask import Flask, request, jsonify
import requests
from docx import Document
from io import BytesIO

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Defina sua chave como variável de ambiente
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

def extract_text_from_docx(file_stream):
    doc = Document(file_stream)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)

def generate_html_via_prompt(text_content):
    prompt = f"""
Você receberá o conteúdo de um arquivo .docx contendo um checklist técnico. Extraia os dados relevantes como:
- Nome do cliente
- Data de execução
- Lista de testes realizados (com status de aprovado/reprovado)
- Observações finais
- Nome do responsável

Com base nesses dados, gere um arquivo HTML completo com estrutura de relatório técnico, contendo:
- Título com o nome do cliente e data
- Tabela dos testes com status e observações
- Rodapé com o nome do responsável e a data
- Use uma estrutura visual simples com cores neutras, boa leitura e responsividade.

Insira um botão para permitir a exportação do arquivo preenchido. 
A tabela dos testes precisa ter um checkbox em cada item


"""{text_content}"""
    """

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        },
    )

    result = response.json()
    return result["choices"][0]["message"]["content"]

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nome de arquivo inválido."}), 400

    file_stream = BytesIO(file.read())
    text_content = extract_text_from_docx(file_stream)
    html_result = generate_html_via_prompt(text_content)

    return jsonify({"html": html_result})

if __name__ == "__main__":
    app.run(debug=True)
