### UDP client - NB-IoT device (C)

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
filename = 'E-IoT Client.csv'
if os.path.exists(filename):
    os.remove(filename)
csv_output = pyRAPL.outputs.CSVOutput(filename)
@pyRAPL.measureit(number=1,output=csv_output)

def IoT():
    # Hash using ESHA256
    ESHA = True

    serverAddressPort_a   = ("127.0.0.1", 1001)
    serverAddressPort_b   = ("127.0.0.2", 2002)
    bufferSize          = 1024

    message1 = 'NReq'
    message2 = "IDReq"
    nc = "%032x" % random.randrange(16**32)  #nonce - '0x' + "%032x" % random.randrange(16**32)
    tc = str(int(time.time()))  #timestamp
    OldID = '0x000000000000000a'  #old ID of C
    C = '0x00000000000000cc'  #address of C
    Rep = '6'

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    ### send - C to A
    bytesToSend = message1,OldID,nc,tc
    serialized_data = pickle.dumps(bytesToSend)
    encrypted_message = encrypt_message(serialized_data, public_key)
    UDPClientSocket.sendto(encrypted_message, serverAddressPort_a)
    print(f"\nSent tuple to Authentication Server (A): {serverAddressPort_a} - {bytesToSend}")

    ### receive - A to C
    data, address = UDPClientSocket.recvfrom(bufferSize)
    decrypted_message = decrypt_message(data, private_key)
    received_tuple = pickle.loads(decrypted_message)
    na = received_tuple[0]
    ta = received_tuple[1]
    hashNaNc = received_tuple[2]
    hashNaTa = received_tuple[3]
    print(f"\nReceived tuple from Authentication Server (A): {address} - {received_tuple}")

    ### send 4 - C to B
    #***
    hashCNc = getESHA256(C+nc,ESHA)
    bytesToSend2 = message2,Rep,OldID,hashCNc,nc,ta,na,hashNaTa
    serialized_data2 = pickle.dumps(bytesToSend2)
    encrypted_message = encrypt_message(serialized_data2, public_key)
    UDPClientSocket.sendto(encrypted_message, serverAddressPort_b)
    print(f"\nSent tuple to Data Server (B): {serverAddressPort_b} - {bytesToSend2}")
    ###

    ### recv 5 - B to C
    data, address = UDPClientSocket.recvfrom(bufferSize)
    decrypted_message = decrypt_message(data, private_key)
    received_tuple = pickle.loads(decrypted_message)
    NewID = received_tuple[0]
    nb = received_tuple[1]
    tb = received_tuple[2]
    print(f"\nReceived tuple from Data Server (B): {address} - {received_tuple}")
    print(f"\nNew Unique ID received from Data Server = {NewID}")
    ###

    UDPClientSocket.close

for _ in range(1001):
   IoT()
csv_output.save()
print("\nPass...")
