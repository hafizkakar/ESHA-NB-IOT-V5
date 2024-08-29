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
    serverAddressPort_d   = ("127.0.0.3", 3003)
    bufferSize          = 1024

    #Encrypting the message with the PKCS1_OAEP object
    message1 = 'NReq'
    message2 = 'LReq'
    message3 = 'JReq'
    nc = "%032x" % random.randrange(16**32)  #nonce - '0x' + "%032x" % random.randrange(16**32)
    tc = str(int(time.time()))  #timestamp
    OldID = '0x000000000000000a'  #old ID of C
    C = '0x00000000000000cc'  #address of C
    B = '0x00000000000000bb'  #address of B
    Rep = '6'

    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    ### send 1 - C to A
    hashCNc = getESHA256(((C+nc).encode('utf-8')).hex(),ESHA)
    bytesToSend = message1,OldID,nc,tc,hashCNc
    serialized_data = pickle.dumps(bytesToSend)
    encrypted_message = encrypt_message(serialized_data, public_key)
    UDPClientSocket.sendto(encrypted_message, serverAddressPort_a)
    print(f"\nSent tuple to Authentication Server (A) {serverAddressPort_a} - {bytesToSend}")
    ### 

    ### receive 2 - A to C
    data, address = UDPClientSocket.recvfrom(bufferSize)
    decrypted_message = decrypt_message(data, private_key)
    received_tuple = pickle.loads(decrypted_message)
    na = received_tuple[0]
    ta = received_tuple[1]
    hashNaNcTa = received_tuple[2]
    print(f"\nReceived tuple from Authentication Server (A) {address} - {received_tuple}")
    ###

    ### send 3 - C to D
    bytesToSend2 = message2,nc,tc,OldID,B
    serialized_data2 = pickle.dumps(bytesToSend2)
    encrypted_message2 = encrypt_message(serialized_data2, public_key)
    UDPClientSocket.sendto(encrypted_message2, serverAddressPort_d)
    print(f"\nSent tuple to Home Base Station (D) {serverAddressPort_d} - {bytesToSend2}")
    ###

    ### recv 4 - D to C
    data, address = UDPClientSocket.recvfrom(bufferSize)
    decrypted_message = decrypt_message(data, private_key)
    received_tuple2 = pickle.loads(decrypted_message)
    nd = received_tuple2[1]
    hashNcNd = received_tuple2[2]
    print(f"\nReceived tuple from Home Base Station (D) {address} - {received_tuple2}")
    ###

    ### send 7 - C to B
    hashCNc  = getESHA256(((C+nc).encode('utf-8')).hex(),ESHA)
    hashNaTa = getESHA256(((na+ta).encode('utf-8')).hex(),ESHA)
    bytesToSend3 = message3,Rep,OldID,hashCNc,nc,tc,ta,hashNaTa
    serialized_data3 = pickle.dumps(bytesToSend3)
    encrypted_message3 = encrypt_message(serialized_data3, public_key)
    UDPClientSocket.sendto(encrypted_message3, serverAddressPort_b)
    print(f"\nSent tuple to Visiting Base Station (B) {serverAddressPort_b} - {bytesToSend3}")
    ###

    ### recv 10 - B to C
    data, address = UDPClientSocket.recvfrom(bufferSize)
    decrypted_message = decrypt_message(data, private_key)
    received_tuple3 = pickle.loads(decrypted_message)
    NewID = received_tuple3[1]
    SecretKey = received_tuple3[2]
    nb = received_tuple3[3]
    tb = received_tuple3[4]
    print(f"\nReceived tuple from Visiting Base Station (B) {address} - {received_tuple3}")
    print(f"\nNew Unique ID received from Visiting Base Station (B) = {NewID}")
    ###

    UDPClientSocket.close

for _ in range(1001):
   IoT()
csv_output.save()
print("\nPass...")
