import sys
import time
import random
import requests
import threading
from flask import Flask, request, jsonify

# Valori di default e soglie
temperatura_soglia = 28
umidita_soglia = 48
nome_dispositivo = "hydra1"

app = Flask(__name__)

@app.route('/imposta_soglie', methods=['POST'])
def imposta_soglie():
    global temperatura_soglia, umidita_soglia
    data = request.json
    temperatura_soglia = data.get('temperatura_soglia', temperatura_soglia)
    umidita_soglia = data.get('umidita_soglia', umidita_soglia)
    return jsonify({"temperatura_soglia": temperatura_soglia, 
                    "umidita_soglia": umidita_soglia}), 200

def simulatore_microcontrollore(host, porta):
    while True:
        temperatura = random.uniform(20, 30)
        umidita = random.uniform(40, 50)
        allarme_temperatura = temperatura > temperatura_soglia  # Soglia di esempio
        allarme_umidita = umidita > umidita_soglia          # Soglia di esempio

        try:
            response = requests.post(f'http://{host}:{porta}/invia_dati', json={
                'nome_dispositivo': nome_dispositivo,
                'temperatura': temperatura,
                'umidita': umidita,
                'allarme_temperatura': allarme_temperatura,
                'allarme_umidita': allarme_umidita,
                'soglia_umidita': umidita_soglia,
                'soglia_temperatura': temperatura_soglia
                
            })
            print(response.json())  # Stampa la risposta del server
        except requests.exceptions.RequestException as e:
            print(f"Errore di connessione: {e}")
        time.sleep(1)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        nome_dispositivo = sys.argv[1]
    host = "localhost"  # Modifica se il server è su un altro host
    porta = 5000         # Modifica se il server ascolta su una porta diversa
    threading.Thread(target=simulatore_microcontrollore, args=(host, porta), daemon=True).start()
    app.run(host='0.0.0.0', port=5001)
