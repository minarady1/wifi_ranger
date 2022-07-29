'''
Simple UDP/TCP client appplication for Wi-Fi ranging.


Bugwright2 Prject

Mina Rady mina.rady@inria.fr

'''

import socket
import rssi
import time
import json
from sys import getsizeof
import pdb
import sys
import os
import logging



PACKET_SIZE = 1000000   # B 
FREQ        = 0.1   # s
seqnum      = 0
USAGE = "Usage: client.py <target IP> <port> <packet rate> <packet size (B)>"

def preparePacket():
    # get time
    global seqnum
    
    timestamp  = time.time_ns()
    timestamp_b = timestamp.to_bytes(80,'big')

    # get seqnum

    seqnum_b = seqnum.to_bytes(80,'big')

    header = timestamp_b + seqnum_b 

    # add additional payload

    padding = bytearray([1]*(PACKET_SIZE- getsizeof (header)))
    
    
    # append all in one bye array
    payload = header+ padding
    
    seqnum = seqnum+1
    return payload


def send_udp(payload):
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(payload, (UDP_IP, UDP_PORT))


print (USAGE)
UDP_IP      = "localhost"
UDP_PORT    = 6000

if (len(sys.argv)>3):
    UDP_IP      = sys.argv[1]
    UDP_PORT    = int(sys.argv[2])
    FREQ        = int(sys.argv[3])
    PACKET_SIZE = int(sys.argv[4])
else:
    exit()

starttime = time.time()

print ("UDP target IP: %s" % UDP_IP)
print ("UDP target port: %s" % UDP_PORT)
period = 1/FREQ
start = time.time()
now = start

while (True):
    payload = preparePacket()
    send_udp(payload)
    time.sleep(period - ((time.time() - starttime) % period))
    now = time.time()
    print ("# sent: ", now,seqnum)

