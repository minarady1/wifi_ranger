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


CONN=  "TCP"
PACKET_SIZE = 500   # B 
FREQ        = 0.1   # s
seqnum      = 0

USAGE = "Usage: client.py <period (s)> <connection type(TCP/UDP)> <packet size (B)>"

def preparePacket():
    # get time
    global seqnum
    
    timestamp  = time.time_ns()
    timestamp_b = timestamp.to_bytes(80,'big')

    # get seqnum

    seqnum_b = seqnum.to_bytes(80,'big')

    # get rssi

    # todo

    header = timestamp_b + seqnum_b

    # add additional payload

    padding = bytearray([1]*(PACKET_SIZE- getsizeof (header)))
    
    print ("#", timestamp,seqnum ,getsizeof (header) )
    
    # append all in one bye array
    payload = header+ padding 
    
    seqnum = seqnum+1
    return payload


def send_udp(payload):
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(payload, (UDP_IP, UDP_PORT))

def send_tcp(payload):
    s.sendall(payload)

print (USAGE)

if (len(sys.argv)>3):
    FREQ        = float(sys.argv[1])
    CONN        = sys.argv[2]
    PACKET_SIZE = int(sys.argv[3])
else:
    exit()


starttime = time.time()

if (CONN == "UDP"):
    UDP_IP      = "10.90.90.1"
    UDP_PORT    = 5005
    print ("UDP target IP: %s" % UDP_IP)
    print ("UDP target port: %s" % UDP_PORT)
    
    while True:
        payload = preparePacket()
        send_udp(payload)
        time.sleep(FREQ - ((time.time() - starttime) % FREQ))

if (CONN == "TCP"):
    HOST = 'localhost'
    PORT = 50007
    print ("TCP Host: %s" % HOST)
    print ("TCP port: %s" % PORT)
    
    s = None
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    with s:
        starttime = time.time()
        while True:
            payload = preparePacket()
            send_tcp(payload)
            time.sleep(1 - ((time.time() - starttime) % 1))


# interface = '3b512542-7170-4cbd-ba73-285f37aa1c1f'
# rssi_scanner = rssi.RSSI_Scan(interface)

# ssids = ['dd-wrt','linksys']

# # sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# # python file will have to be run with sudo privileges.
# ap_info = rssi_scanner.getAPinfo()

# print(ap_info)