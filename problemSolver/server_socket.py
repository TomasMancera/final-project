import base64
import socket
import json
import signal
import os
import logging
import requests
from factory.creator_fibonacci import CreatorFibonacci
from factory.creator_fizzBuzz import CreatorFizzBuzz
from factory.creator_primeVerifier import CreatorPrimeVerifier
from util import cryptography as crypto
import util.log

class Server:
    
    def start_server(self, host, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f"--server listening on {host}:{port}\n")
            logging.info("Server socket started")
            
            flag = True
            while flag:
                conn, addr = s.accept()
                logging.info("Server connected with: %s", addr)
                with conn:
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        data_decoded = json.loads(data.decode('utf-8'))
                        logging.info("Data received from %s: %s", addr, data_decoded)
                        
                        if data_decoded.get("shutdown"):
                            response_server = requests.get("http://localhost:5000/shutdown")
                            response = {"status": "success", "message": "System will shutdown"}
                            print("Shutdown Successfully")
                            logging.info("shutdown")
                            conn.send(json.dumps(response).encode())
                            os.kill(os.getpid(), signal.SIGINT)
                        else:
                            try:
                                logging.info("Processing request")
                                
                                # Obtener la clave de sesión
                                session_key = crypto.get_session_key()
                                logging.info("Session key generated")
                                
                                # Encriptar la clave de sesión con la clave pública del servidor
                                encrypted_session = crypto.encrypt_data(base64.b64encode(session_key).decode('utf-8'), crypto.get_public_server_key())
                                logging.info("Session key encrypted")
                                
                                # Encriptar los datos con la clave de sesión
                                data_str = json.dumps(data_decoded)
                                encrypted_data = crypto.encrypt_with_session_key(data_str, session_key)
                                logging.info("Data encrypted")
                                
                                # Enviar la solicitud al DataServer
                                response = requests.post('http://localhost:5000/numbers', json={
                                    'session_key': encrypted_session,
                                    'data': encrypted_data
                                })
                                logging.info("Request sent to Data server")

                                if response.status_code == 200:
                                    logging.info("Received response from Data server")

                                    encrypted_session_key = response.json()['session_key']
                                    encrypted_data = response.json()['data']

                                    # Desencriptar la clave de sesión
                                    session_key = crypto.decrypt_data(encrypted_session_key, crypto.get_private_client_key())
                                    logging.info("Session key decrypted")

                                    # Desencriptar los datos con la clave de sesión
                                    decrypted_data = crypto.decrypt_with_session_key(encrypted_data, session_key)
                                    logging.info("Data decrypted")
                                    print("Decrypted response from server:", decrypted_data)

                                    json_decrypted_response = json.loads(decrypted_data)

                                    problem = instanceProblem(data_decoded["name"])

                                    if problem is None:
                                        json_result = {"Result": "the problem doesn't exist"}
                                        conn.sendall((json.dumps(json_result) + "\n").encode("utf-8"))
                                        logging.error("Error solving problem")
                                    else:
                                        result = problem.compute_results(json_decrypted_response)
                                        logging.info("Problem solved")

                                        result_client = {"Result": result}
                                        print(result_client)
                                        conn.sendall((json.dumps(result_client) + "\n").encode("utf-8"))
                                        logging.info("Result sent to client")
                                else:
                                    result_client = {"Result": "Numbers could not be reached"}
                                    logging.error("Failed to reach Data server")

                            except Exception as e:
                                logging.error(f"An error occurred during processing: {e}")
                                result_client = {"Result": "An error occurred during processing"}
                                conn.sendall((json.dumps(result_client) + "\n").encode("utf-8"))
                    except Exception as e:
                        logging.error(f"An error occurred: {e}")
                        conn.sendall((json.dumps({"Result": "An error occurred"}).encode("utf-8")))

def instanceProblem(problem):
    if problem == "fizzBuzz":
        return CreatorFizzBuzz()
    
    if problem == "primeVerifier":
        return CreatorPrimeVerifier()
    
    if problem == "fibonacci":
        return CreatorFibonacci()

def main():
    util.log.log()
    server = Server()
    server.start_server('localhost', 65432)

if __name__ == "__main__":
    main()
