from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import os


# Generar un par de claves RSA para el servidor
server_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

server_public_key = server_private_key.public_key()

# Serializar y guardar la clave privada del servidor en PEM
pem_server_private_key = server_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)

with open('server_private_key.pem', 'wb') as f:
    f.write(pem_server_private_key)

# Serializar y guardar la clave pública del servidor en PEM
pem_server_public_key = server_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open('server_public_key.pem', 'wb') as f:
    f.write(pem_server_public_key)

def get_public_client_key():

    with open('../client_public_key.pem', 'rb') as f:

        pem_client_public_key = f.read()

    return load_pem_public_key(pem_client_public_key, backend=default_backend())

def get_private_server_key():
    with open('server_private_key.pem', 'rb') as f:

        pem_server_private_key = f.read()

    return load_pem_private_key(pem_server_private_key, password=None, backend=default_backend())

def get_encrypted_session_key(session_key):

    return encrypt_data(base64.b64encode(session_key).decode('utf-8'), get_public_client_key())

def encrypt_data(data, public_key):
    encrypted = public_key.encrypt(
        data.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode('utf-8')


def decrypt_data(encrypted_data, private_key):
    encrypted_data = base64.b64decode(encrypted_data)
    decrypted = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64decode(decrypted)

def decrypt_with_session_key(encrypted_data, session_key):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    
    unpadder = sym_padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data.decode('utf-8')

def encrypt_with_session_key(data, session_key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(session_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padder = sym_padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_data).decode('utf-8')