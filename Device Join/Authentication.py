### UDP server - Authentication Server (A)

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
filename = 'E-Authentication Server.csv'
if os.path.exists(filename):
    os.remove(filename)
csv_output = pyRAPL.outputs.CSVOutput(filename)
@pyRAPL.measureit(number=1,output=csv_output)

def Authentication():
    # Hash using ESHA256
    ESHA = True

    localIP     = "127.0.0.1"
    localPort   = 1001
    bufferSize  = 1024

    serverAddressPort_b = ("127.0.0.2", 2002)

    na = "%032x" % random.randrange(16**32)
    ta = str(int(time.time()))
    A = '0x00000000000000aa'  #address of A
    C = '0x00000000000000cc'  #address of C
    OldID = '0x000000000000000a'  #old ID of C
    message5 = 'LReq'

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort)) 
    print("UDP listening")

    while(True):
        # receive - C to A
        data, address = UDPServerSocket.recvfrom(bufferSize)
        decrypted_message = decrypt_message(data, private_key)
        received_tuple = pickle.loads(decrypted_message)
        OldID = received_tuple[1]
        nc = received_tuple[2]
        tc = received_tuple[3]
        hashCNc = received_tuple[4]
        print(f"\nReceived tuple from IoT (C): {address}: {received_tuple}")
        
        ### send 2 - A to C
        hashNaNcTa = getESHA256(((na+nc+ta).encode('utf-8')).hex(),ESHA)
        bytesToSend = na,ta,hashNaNcTa
        serialized_data = pickle.dumps(bytesToSend)
        encrypted_message = encrypt_message(serialized_data, public_key)   
        UDPServerSocket.sendto(encrypted_message, address)
        print(f"\nSent tuple to IoT (C): {address} - {bytesToSend}")
        break
        ###

    ### send 3 - A to B
    hashANc = getESHA256(((A+nc).encode('utf-8')).hex(),ESHA)
    bytesToSend2 = message5,hashANc,OldID,na,nc
    serialized_data2 = pickle.dumps(bytesToSend2)    
    encrypted_message2 = encrypt_message(serialized_data2, public_key)   
    UDPServerSocket.sendto(encrypted_message2, serverAddressPort_b)
    print(f"\nSent tuple to Visiting Base Station Server (B): {serverAddressPort_b} - {bytesToSend2}")
    ###
    UDPServerSocket.close

for _ in range(1001):
   Authentication()
csv_output.save()
print("\nPass...")
