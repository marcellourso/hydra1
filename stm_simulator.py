from flask import Flask, request, jsonify
import threading
import time
import random
import requests

app = Flask(__name__)

# Valori di default e soglie
temperatura_soglia = 28
umidita_soglia = 48
temperatura = 0
umidita = 0
allarme_temperatura = False
allarme_umidita = False

# Funzione per simulare il microcontrollore
def simulatore_microcontrollore(host, porta):
    while True:
        temperatura = random.uniform(20, 30)
        umidita = random.uniform(40, 50)
        allarme_temperatura = temperatura > temperatura_soglia
        allarme_umidita = umidita > umidita_soglia
        
        """ print(f"Temperatura: {temperatura:.2f}°C, Umidità: {umidita:.2f}%, "
              f"Allarme Temperatura: {'ON' if allarme_temperatura else 'OFF'}, "
              f"Allarme Umidità: {'ON' if allarme_umidita else 'OFF'}") """

        
        try:
            requests.post(f'http://{host}:{porta}/invia_dati', json={
                'temperatura': temperatura,
                'umidita': umidita,
                'allarme_temperatura': allarme_temperatura,
                'allarme_umidita': allarme_umidita
            })
        except requests.exceptions.RequestException:
            pass  # Gestisci gli errori di connessione qui
        time.sleep(1)

# Endpoint per ricevere i dati dal "microcontrollore"
@app.route('/invia_dati', methods=['POST'])
def invia_dati():
    data = request.json
    return jsonify(data), 200

# Endpoint per impostare le soglie
@app.route('/imposta_soglie', methods=['POST'])
def imposta_soglie():
    global temperatura_soglia, umidita_soglia
    data = request.json
    temperatura_soglia = data.get('temperatura_soglia', temperatura_soglia)
    umidita_soglia = data.get('umidita_soglia', umidita_soglia)
    return jsonify({"temperatura_soglia": temperatura_soglia, 
                    "umidita_soglia": umidita_soglia}), 200

if __name__ == '__main__':
    host = "localhost"
    porta = 5000
    # Avvia il thread del simulatore
    threading.Thread(target=simulatore_microcontrollore, args=(host, porta), daemon=True).start()
    # Avvia il server Flask
    app.run(host=host, port=porta)
