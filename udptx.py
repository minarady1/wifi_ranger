import socket
import rssi
import time
import json
from sys import getsizeof
import pdb
import sys



# epxeriment settings

UDP_IP = "10.90.90.1"
UDP_PORT = 5005
PACKET_SIZE = 500   # B 
FREQ =    0.1 # s


seqnum = 0

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

# send


print("UDP target IP: %s" % UDP_IP)
print("UDP target port: %s" % UDP_PORT)


def send(payload):
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(payload, (UDP_IP, UDP_PORT))

# parse argv

if (len(sys.argv)>1):
    FREQ = float(sys.argv[1])


starttime = time.time()

while True:
    
    payload = preparePacket()
    send(payload)
    time.sleep(FREQ - ((time.time() - starttime) % FREQ))

# interface = '3b512542-7170-4cbd-ba73-285f37aa1c1f'
# rssi_scanner = rssi.RSSI_Scan(interface)

# ssids = ['dd-wrt','linksys']

# # sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# # python file will have to be run with sudo privileges.
# ap_info = rssi_scanner.getAPinfo()

# print(ap_info)