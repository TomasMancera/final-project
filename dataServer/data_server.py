import base64
import os
import signal
from flask import Flask, request, jsonify
import random
from randomNumbers.normal_distribution import NormalRandomDistribution
from randomNumbers.uniform_distribution import UniformRandomDistribution
from util import cryptography as crypto
import json
import logging

app = Flask(__name__)

# Configurar el logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("data_server.log"),
        logging.StreamHandler()
    ]
)

# Función para apagar el servidor
def shutdown_server():
    pid = os.getpid()
    os.kill(pid, signal.SIGINT)

@app.route("/shutdown", methods=["GET"])
def shutdown():
    logging.info("Shutdown request received")
    shutdown_server()
    return "Server is shutting down..."

@app.route("/numbers", methods=["POST"])
def numbers():
    encrypted_session_key = request.json['session_key']
    encrypted_request_data = request.json['data']
    print(encrypted_session_key,"\n")
    print(encrypted_request_data,"\n")


    try:
        logging.info("Request received with encrypted session key and data")
        
        # Desencriptar la clave de sesión
        session_key = crypto.decrypt_data(encrypted_session_key, crypto.get_private_server_key())
        logging.info("Session key decrypted")
        
        # Desencriptar la solicitud con la clave de sesión
        request_data = crypto.decrypt_with_session_key(encrypted_request_data, session_key)
        request_data_decoded = json.loads(request_data)
        logging.info("Data decrypted: %s", request_data_decoded)

        distribution_random = random.choice((0, 1))
        if distribution_random:
            distribution = NormalRandomDistribution()
        else:
            distribution = UniformRandomDistribution()

        # Obtener los números y aplicar la distribución aleatoria
        query_numbers = distribution.get_numbers(request_data_decoded["low_limit"], request_data_decoded["max_limit"], request_data_decoded["quantity_data"])
        logging.info("Random numbers generated: %s", query_numbers)

        encrypted_session_key = crypto.get_encrypted_session_key(session_key)
        logging.info("Session key re-encrypted")

        server_response_json = {"Numbers": query_numbers}
        server_data = json.dumps(server_response_json)

        encrypted_response = crypto.encrypt_with_session_key(server_data, session_key)
        logging.info("Response data encrypted")

        return jsonify({"session_key": encrypted_session_key, "data": encrypted_response})

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
