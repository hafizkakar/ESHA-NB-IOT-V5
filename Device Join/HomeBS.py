### UDP server - Home/Old Base Station (D)

import socket
import os
import random
import time
import hashlib
import pickle
import pyRAPL
from ESHA256 import getESHA256

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

private_key = RSA.import_key(open('private_key.pem', 'r').read())
public_key = RSA.import_key(open('public_key.pem', 'r').read())

### NB-IoT simulation specifications
def calc_delay(signal):
   rate = 0.18 * ( float(signal) + 46 ) / 70    # bandwidth = 0.18M, tx power signals = 46 dBm and 23 dBm,divide by difference (gain) of 70dBm
   return(rate)

rate_cmd = 'iwconfig wlan0 rate %sM" % calc_delay(signal)'
os.system(rate_cmd)
###

# Encrypting with PKCS1_OAEP
def encrypt_message(message, public_key):
    # Initialize cipher for encryption
    cipher = PKCS1_OAEP.new(public_key)

    # Calculate the maximum chunk size for encryption
    max_chunk_size = (public_key.size_in_bytes() + 1) - 2 * (hashlib.sha1().digest_size + 2)

    # Encrypt the message in chunks
    encrypted_chunks = []
    for i in range(0, len(message), max_chunk_size):
        chunk = message[i:i + max_chunk_size]
        encrypted_chunks.append(cipher.encrypt(chunk))

    # Return concatenated encrypted message
    return b''.join(encrypted_chunks)

# Decrypting with PKCS1_OAEP
def decrypt_message(encrypted_message, private_key):
    # Initialize cipher for decryption
    cipher = PKCS1_OAEP.new(private_key)

    # Calculate the maximum chunk size for decryption
    max_chunk_size = private_key.size_in_bytes()

    # Decrypt the message in chunks
    decrypted_chunks = []
    for i in range(0, len(encrypted_message), max_chunk_size):
        chunk = encrypted_message[i:i + max_chunk_size]
        decrypted_chunks.append(cipher.decrypt(chunk))

    # Return concatenated decrypted message
    return b''.join(decrypted_chunks)


pyRAPL.setup()
filename = 'E-Home Base Station.csv'
if os.path.exists(filename):
    os.remove(filename)
csv_output = pyRAPL.outputs.CSVOutput(filename)
@pyRAPL.measureit(number=1,output=csv_output)

def Home():

    # Hash using ESHA256
    ESHA = True

    localIP     = "127.0.0.3"
    localPort   = 3003
    bufferSize  = 1024

    serverAddressPort_a = ("127.0.0.1", 1001)
    serverAddressPort_b = ("127.0.0.2", 2002)

    message2 = 'RApp'
    D = '0x00000000000000dd'
    nd = "%032x" % random.randrange(16**32)

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort)) 
    print("UDP listening")

    # Listen for incoming datagrams
    while(True):
        ### recv 3 - C to D
        data, address = UDPServerSocket.recvfrom(bufferSize)
        decrypted_message = decrypt_message(data, private_key)
        received_tuple = pickle.loads(decrypted_message)
        nc = received_tuple[1]
        tc = received_tuple[2]
        OldID = received_tuple[3]
        B = received_tuple[4]
        print(f"\nReceived tuple from IoT (C): {address}: {received_tuple}")
        ###
        
        ### send 4 - D to C
        hashNcNd = getESHA256(((nc+nd).encode('utf-8')).hex(),ESHA)
        bytesToSend = message2,nd,hashNcNd
        serialized_data = pickle.dumps(bytesToSend)
        encrypted_message = encrypt_message(serialized_data, public_key)   
        UDPServerSocket.sendto(encrypted_message, address)
        print(f"\nSent tuple to IoT (C): {address} - {bytesToSend}")
        ###
        break

    UDPServerSocket.close

for _ in range(1001):
   Home()
csv_output.save()
print("\nPass...")
