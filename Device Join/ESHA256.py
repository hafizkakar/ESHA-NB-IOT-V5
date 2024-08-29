import sys
import time
import ctypes

lib = ctypes.CDLL('./esha.so')
lib.maint.argtypes = [ctypes.c_int, ctypes.c_char_p]

def getESHA256(o_hex,ESHA):

    way = 7 if ESHA else 1
        
    o_hex_bytes = o_hex.encode('utf-8')
    lib.maint(way, o_hex_bytes)
    with open('output.txt','r') as file:
        result = file.read()
        print(result)
    return result
