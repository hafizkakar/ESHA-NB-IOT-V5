### UDP server - Base Station (D)

import socket
import os
import random
import time
import hashlib
import pickle
import pyRAPL
import pyRAPL.measurement
import pyRAPL.outputs
import pyRAPL.result
from ESHA256 import getESHA256

# NB-IoT simulation specifications
def calc_delay(signal):
    rate = 0.18 * ( float(signal) + 46 ) / 40    # bandwidth = 0.18M, rx power signals = 46 dBm and 23 dBm,divide by difference (gain) of 40dBm
    return(rate)

rate_cmd = 'iwconfig wlan0 rate %sM" % calc_delay(signal)'
os.system(rate_cmd)
###

time.sleep(1)
print("UDP listening")
pyRAPL.setup()
filename = 'E-BaseStation.csv'
if os.path.exists(filename):
    os.remove(filename)
csv_output = pyRAPL.outputs.CSVOutput(filename)
@pyRAPL.measureit(number=1,output=csv_output)


def BaseStation():
    # Hash using ESHA256
    ESHA = True

    localIP     = "127.0.0.3"
    localPort   = 3003
    bufferSize  = 1024

    Rep = 4
    SecretKey = '0x0000000000000011'
    IPFS_TranHash = "0x60d14431721375ed7347df1c21f2fee9a3bbefbb39ea470b06a614b7e1d65419"
    LinearHashChain = []

    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP, localPort)) 
    print("UDP listening")

    # Listen for incoming datagrams
    while(True):
        ### recv 3 - C to D
        data, address = UDPServerSocket.recvfrom(bufferSize)
        received_tuple = pickle.loads(data)
        message1 = received_tuple[0]
        
        if 'Stop' in received_tuple: 
            break    
        UID = received_tuple[1]
        RepC = received_tuple[2]
        message2 = received_tuple[3]
        hashC = received_tuple[4]
        nc = received_tuple[5]
        tc = received_tuple[6]
        print(f"\nReceived tuple from IoT (C): {address}: {received_tuple}")
        ###
        SRep = str(Rep)
        hashD = getESHA256(tc+nc+UID+SRep+message2+SecretKey,ESHA)
        print(f"\nHASH: {tc+nc+UID+SRep+message2+SecretKey} =  {hashD} \n")
        ### send 4 - D to C
        if RepC == Rep and Rep >= 4 and hashC == hashD: 
            Rep +=1           
            bytesToSend = IPFS_TranHash, Rep   
            LinearHashChain.append(received_tuple[0])            
        else:
            Rep -=1
            bytesToSend = "Failed", Rep     

        print(f"\nSent tuple to IoT (C): {address} - {bytesToSend}")
        serialized_data = pickle.dumps(bytesToSend)
        UDPServerSocket.sendto(serialized_data, address)

    UDPServerSocket.close
    print(f"\nESHA-256: {ESHA}")
    print("\n")

for _ in range(1001):
    BaseStation()
csv_output.save()
print("\nPass...")
