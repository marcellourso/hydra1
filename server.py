from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/invia_dati', methods=['POST'])
def ricevi_dati():
    data = request.json
    print(f"Dati ricevuti: {data}")
    # Aggiungi qui ulteriore logica di elaborazione se necessario
    return jsonify({"status": "Successo","dati_ricevuti"
    :data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
