
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
    prompt = (
        "Você receberá o conteúdo de um arquivo .docx contendo um checklist técnico. Extraia os dados relevantes como:\n"
        "- Nome do cliente\n"
        "- Data de execução\n"
        "- Lista de testes realizados (com status de aprovado/reprovado)\n"
        "- Observações finais\n"
        "- Nome do responsável\n\n"
        "Com base nesses dados, gere um arquivo HTML completo com estrutura de relatório técnico, contendo:\n"
        "- Título com o nome do cliente e data\n"
        "- Tabela dos testes com status e observações\n"
        "- Rodapé com o nome do responsável e a data\n"
        "- Use uma estrutura visual simples com cores neutras, boa leitura e responsividade.\n\n"
        "IMPORTANTE: crie o HTML do zero, com base apenas no texto abaixo:\n\n"
        f"{text_content}"
    )

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
