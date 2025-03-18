from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Lista de criptomoedas que serão buscadas
CRIPTOMOEDAS = ["bitcoin", "ethereum", "dogecoin", "litecoin", "cardano", "solana", "xrp", "polkadot"]

# Função para obter os preços das criptomoedas da API CoinGecko
def obter_precos():
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(CRIPTOMOEDAS)}&vs_currencies=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta uma exceção para erros HTTP
        data = response.json()
        
        # Retorna apenas as criptomoedas disponíveis
        return {moeda: data.get(moeda, {}).get('usd', 0) for moeda in CRIPTOMOEDAS}

    except requests.RequestException as e:
        print(f"Erro ao obter preços: {e}")
        return {moeda: 0 for moeda in CRIPTOMOEDAS}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/precos", methods=["GET"])
def precos():
    precos = obter_precos()
    return jsonify(precos)

if __name__ == "__main__":
    app.run(debug=True, port=5002)