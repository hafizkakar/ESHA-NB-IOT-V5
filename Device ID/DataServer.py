### UDP server - Data Server (B)

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

# NB-IoT simulation specifications
def calc_delay(signal):
   rate = 0.18 * ( float(signal) + 46 ) / 40    # bandwidth = 0.18M, rx power signals = 46 dBm and 23 dBm,divide by difference (gain) of 40dBm
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
filename = 'E-Data Server.csv'
if os.path.exists(filename):
    os.remove(filename)
csv_output = pyRAPL.outputs.CSVOutput(filename)
@pyRAPL.measureit(number=1,output=csv_output)

def Data():
    # Hash using ESHA256
    ESHA = True

    localIP     = "127.0.0.2"
    localPort   = 2002
    bufferSize  = 1024

    serverAddressPort_a = ("127.0.0.1", 1001)



    NewID = '0x00000000000000aa'
    SecretKey = '0x0000000000000011'
    tb = str(int(time.time()))  #timestamp
    nb = "%032x" % random.randrange(16**32)

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort)) 
    print("UDP listening")

    while(True):
        data, address = UDPServerSocket.recvfrom(bufferSize)
        decrypted_message = decrypt_message(data, private_key)
        received_tuple = pickle.loads(decrypted_message)

        if 1001 in address:
            ### receive  - A to B 
            OldID = received_tuple[0]
            na = received_tuple[1]
            tc = received_tuple[2]
            ta = received_tuple[3]
            hashNaTa = received_tuple[4]
            print(f"\nReceived tuple from Authentication Server (A): {address}: {received_tuple}")
        else:
            ### receive - C to B 
            Rep = received_tuple[1]
            OldID = received_tuple[2]
            hashCNc = received_tuple[3]
            nc = received_tuple[4]
            ta = received_tuple[5]
            na = received_tuple[6]
            hashNaTa = received_tuple[7]
            print(f"\nReceived tuple from IoT (C): {address}: {received_tuple}")
            
            ### send  - B to C        
            bytesToSend = NewID,nb,tb
            serialized_data = pickle.dumps(bytesToSend) 
            encrypted_message = encrypt_message(serialized_data, public_key)   
            UDPServerSocket.sendto(encrypted_message, address)
            print(f"\nSent tuple to IoT (C): {address} - {bytesToSend}")
            break

    UDPServerSocket.close

for _ in range(1001):
   Data()
csv_output.save()
print("\nPass...")
