### UDP client - NB-IoT device (C)

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

### NB-IoT simulation specifications
def calc_delay(signal):
   rate = 0.18 * ( float(signal) + 46 ) / 70    # bandwidth = 0.18M, tx power signals = 46 dBm and 23 dBm,divide by difference (gain) of 70dBm
   return(rate)

rate_cmd = 'iwconfig wlan0 rate %sM" % calc_delay(signal)'
os.system(rate_cmd)
###

pyRAPL.setup()
filename = 'E-IoT.csv'
if os.path.exists(filename):
    os.remove(filename)
csv_output = pyRAPL.outputs.CSVOutput(filename)
@pyRAPL.measureit(number=1,output=csv_output)


def IoT():
   # Hash using ESHA256
   ESHA = True

   serverAddressPort_d   = ("127.0.0.3", 3003)
   bufferSize          = 1024

   message1 = 'AReq'
   message2 = 'IoTData'
   nc = "%032x" % random.randrange(16**32)  #nonce - '0x' + "%032x" % random.randrange(16**32)
   tc = str(int(time.time()))  #timestamp
   UID = '0x00000000000000aa'  #ID of C
   Rep = 4
   SecretKey = '0x0000000000000011'
   LinearHashChain = []

   UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

   for i in range(1):
      ### send 3 - C to D
      SRep = str(Rep)
      hash = getESHA256(tc+nc+UID+SRep+message2+SecretKey,ESHA)
      print(f"\nHASH: {tc+nc+UID+SRep+message2+SecretKey} =  {hash} \n")
 
      bytesToSend = message1,UID,Rep,message2,hash,nc,tc
      serialized_data = pickle.dumps(bytesToSend)
      UDPClientSocket.sendto(serialized_data, serverAddressPort_d)
      print(f"\nSent tuple to Home Base Station (D) {serverAddressPort_d} - {bytesToSend}")

      ### recv 4 - D to C
      data, address = UDPClientSocket.recvfrom(bufferSize)
      received_tuple = pickle.loads(data)
      TranHash = received_tuple[0]
      Rep = received_tuple[1]

      if TranHash == "Failed":
         print(f"\nTransaction {i} Failed, Device reputation deteriorated: {received_tuple[1]} by Base Station (D)")
      else:
         print(f"\nTransaction {i} Approved, Device reputation incremented: {received_tuple[1]}, transaction hash from Base Station (D): {address} - {received_tuple[0]}")
         LinearHashChain.append(received_tuple[0])

   bytesToSend = 'Stop','Stop','Stop'
   serialized_data = pickle.dumps(bytesToSend)
   UDPClientSocket.sendto(serialized_data, serverAddressPort_d)

   print(f"\nApproved Transactions in Linear Hash Chain: {LinearHashChain}")
   UDPClientSocket.close 
   print(f"\nESHA-256: {ESHA}")
   print("\n") 

for _ in range(1001):
   IoT()
csv_output.save()
print("\nPass...")
