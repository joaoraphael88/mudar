from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔹 Obtendo a API Key do PipeRun a partir das variáveis de ambiente do Railway
API_KEY = os.getenv("d3f346e08d0e8ba2b8e44ee7654606fe")
PIPE_RUN_URL = "https://api.pipe.run/v1/deals/"

@app.route("/", methods=["GET"])
def home():
    return "Servidor rodando no Railway 🚀"

@app.route("/webhook-piperun", methods=["POST"])
def receber_webhook():
    data = request.json

    if not data or "id" not in data:
        return jsonify({"error": "Dados inválidos"}), 400

    deal_id = data["id"]
    novo_titulo = f"Lead Facebook - {data.get('name', 'Sem Nome')}"

    # 🔹 Atualiza o título da oportunidade no PipeRun
    url = f"{PIPE_RUN_URL}{deal_id}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    payload = {"title": novo_titulo}

    response = requests.put(url, json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify({"message": "Título atualizado com sucesso"}), 200
    else:
        return jsonify({"error": "Falha ao atualizar título"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
