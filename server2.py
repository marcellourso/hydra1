from flask import Flask, request, jsonify
from collections import defaultdict
import threading

app = Flask(__name__)

# Struttura dati per memorizzare i dati in arrivo
dati_simulatori = defaultdict(list)
lock = threading.Lock()

@app.route('/invia_dati', methods=['POST'])
def ricevi_dati():
    data = request.json
    id_simulatore = data.get("id_simulatore")

    with lock:
        # Aggiungi i dati alla lista corrispondente all'ID del simulatore
        dati_simulatori[id_simulatore].append(data)

    print(f"Dati ricevuti da {id_simulatore}: {data}")
    # Qui puoi aggiungere ulteriore logica di elaborazione

    return jsonify({"status": "Successo"}), 200

# Funzione per elaborare i dati (esempio)
def elabora_dati():
    while True:
        with lock:
            for id_simulatore, dati in dati_simulatori.items():
                # Elabora i dati qui
                pass

if __name__ == '__main__':
    # Avvia un thread per l'elaborazione dei dati
    thread_elaborazione = threading.Thread(target=elabora_dati)
    thread_elaborazione.start()

    app.run(host='0.0.0.0', port=5000)
