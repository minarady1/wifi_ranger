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


CONN=  "TCP"
PACKET_SIZE = 1000000   # B 
FREQ        = 0.1   # s
seqnum      = 0
DURATION     = 60*3 # s
USAGE = "Usage: client.py <period (s)> <connection type(TCP/UDP)> <packet size (B)>"

def preparePacket():
    # get time
    global seqnum
    
    timestamp  = time.time_ns()
    timestamp_b = timestamp.to_bytes(80,'big')

    # get seqnum

    seqnum_b = seqnum.to_bytes(80,'big')

    # get networkinfo

    network_info_b = get_network_info()
    
    # Experiment info
    exp_info_b = get_exp_info()

    header = timestamp_b + seqnum_b + exp_info_b + network_info_b 

    # add additional payload

    padding = bytearray([1]*(PACKET_SIZE- getsizeof (header)))
    
    
    # append all in one bye array
    payload = header+ padding
    
    print ("#", timestamp,seqnum ,getsizeof (header), len (payload) )
    seqnum = seqnum+1
    return payload


def send_udp(payload):
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(payload, (UDP_IP, UDP_PORT))


def get_network_info():
    stream = os.popen("netsh wlan show interfaces")
    output = stream.read()
    output_b = bytes(output,"utf-8")
    print (output)
    len_net_info = getsizeof(output_b)
    if (len_net_info>5000):
        # problem
        pdb.set_trace()
    res = bytearray(5000) # max netinfo size 5kb
    i = 0
    for item in output_b:
        res [i] = item
        i=i+1
    return res

def get_exp_info ():
    packet_size = PACKET_SIZE.to_bytes(10,'big')
    freq        = FREQ.to_bytes(10,'big') 
    conn        = CONN.encode("utf-8") # 3 B
    res = packet_size + freq+ conn # total 23 B
    return res
     


print (USAGE)

if (len(sys.argv)>3):
    FREQ        = int(sys.argv[1])
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
    period = 1/FREQ
    start = time.time()
    now = start
    while (now-start< DURATION):
        payload = preparePacket()
        send_udp(payload)
        time.sleep(period - ((time.time() - starttime) % period))
        now = time.time()

if (CONN == "TCP"):
    HOST = '10.90.90.1'
    PORT = 50007
    print ("TCP Host: %s" % HOST)
    print ("TCP port: %s" % PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    try:
        starttime = time.time()
        period = 1/FREQ
        start = time.time()
        now = start
        while (now-start< DURATION):
            payload = preparePacket()
            s.sendall(payload)
            time.sleep(period - ((time.time() - starttime) % period))
            now = time.time()
    finally:
        s.close()
