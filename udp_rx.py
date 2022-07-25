'''
Simple UDP/TCP server appplication with logging feautre.

Bugwright2 Prject

Mina Rady mina.rady@inria.fr

'''

import socket
import sys
import time
import datetime
import json
import os
import pdb
from sys import getsizeof
import sys

USAGE = "Usage: udp_rx.py <host IP> <port> <duration (s)> <exp ID> <run ID>"
print (USAGE)

# log settings


LOG_DIR_NAME = 'logs'
EXPID        = sys.argv[1]
RUNID        = sys.argv[2]
UDP_IP       = sys.argv[3]
UDP_PORT     = int(sys.argv[4])
DURATION     = int(sys.argv[5])

log_file_path = ''
def prepare_log_file():
    log_dir_path = os.path.join(os.path.dirname(__file__), LOG_DIR_NAME)

    # make sure we have the log directory
    if os.path.isdir(log_dir_path):
        # log directory is ready :-)
        pass
    else:
        try:
            os.mkdir(log_dir_path)
        except OSError as err:
            sys.exit('Failed to make the log directory: {}'.format(err))

    # time.strftime('%Y%m%d-%H%M%S')
    # decide a log file name and create it
    
    log_file_name = 'log_{}_{}.jsonl'.format(EXPID, RUNID)
    log_file_path = os.path.join(log_dir_path, log_file_name)
    
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
        msg = (
            'Replacing file.\n' +
            'Log file already exits: {}'.format(log_file_path)
        )
        
    else:
        # create an empty file with the log file name
        try:
            open(log_file_path, 'w').close()
        except OSError as err:
            sys.exit('Failed to create a log file: {}'.format(err))

    return log_file_path

def process_payload(data):
    timestamp_ns    = int.from_bytes(data [0:80], "big")
    seqnum          = int.from_bytes(data [80:160] , "big")
    packet_size	    = int.from_bytes(data [160:170] , "big")
    freq	        = int.from_bytes(data [170:180] , "big")
  
    
    frame_len       = getsizeof(data) 
    print(seqnum,frame_len, "delay", (time.time_ns()-timestamp_ns)/10**9)
    res = {
        "src_timestamp_ns"  : timestamp_ns,
        "seqnum"            : seqnum,
        "packet_size"       : packet_size,
        "freq"	            : freq,
        "frame_len"         : frame_len,
        
    }
    return res

def log_data (data):
    global log_file_path
    ts = datetime.datetime.now()
    #pdb.set_trace()
    payload_js = process_payload(data)
    with open(log_file_path, 'a') as f:
        log = {
            'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'timestamp': time.time_ns(),
            'payload'  : payload_js
        }
        f.write('{}\n'.format(json.dumps(log)))



log_file_path = prepare_log_file() 

print (log_file_path)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

start = time.time()
now = start
while (now-start < DURATION):
    data, addr = sock.recvfrom(65500) 
    log_data(data)
    now = time.time()
sock.close()
print ("done, exiting  ...")
sys.exit()