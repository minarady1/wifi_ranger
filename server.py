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




# log settings

EXPERIMENT_ID = "test"
run_id = "test_run"
LOG_DIR_NAME = 'logs'
log_file_path = ''
CONN = "TCP"
USAGE = "Usage: server.py <experiment ID> <conn_type(TCP/UDP)>"

def prepare_log_file():
    log_dir_path = os.path.join(os.path.dirname(__file__), LOG_DIR_NAME,run_id)

    # make sure we have the log directory
    if os.path.isdir(log_dir_path):
        # log directory is ready :-)
        pass
    else:
        try:
            os.mkdir(log_dir_path)
        except OSError as err:
            sys.exit('Failed to make the log directory: {}'.format(err))

    # decide a log file name and create it
    log_file_name = 'log-{}_{}-{}.jsonl'.format(EXPERIMENT_ID, run_id,
        time.strftime('%Y%m%d-%H%M%S')
    )
    log_file_path = os.path.join(log_dir_path, log_file_name)
    if os.path.exists(log_file_path):
        msg = (
            'Failed to crate a log file.\n' +
            'Log file already exits: {}'.format(log_file_path)
        )
        sys.exit(msg)
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
    freq	    = int.from_bytes(data [170:180] , "big")
    conn	    = data [180:183].decode("utf-8")
    netinfo	    = data [183:183+5000].decode("utf-8")
 
    frame_len       = getsizeof(data) 
    print(seqnum)
    res = {
        "src_timestamp_ns"  : timestamp_ns,
        "seqnum"            : seqnum,
        "netinfo"	    : netinfo,
        "packet_size"       : packet_size,
        "freq"	            : freq,
        "conn" 		    : conn,
        "frame_len"         : frame_len,
        
    }
    # print (timestamp_ns,seqnum,frame_len, (time.time_ns()-timestamp_ns)/1000)
    return res

def log_data (data):
    global log_file_path
    ts = datetime.datetime.now()
    #pdb.set_trace()
    paylod_js = process_payload(data)
    with open(log_file_path, 'a') as f:
        log = {
            'name': EXPERIMENT_ID,
            'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            'timestamp': time.time_ns(),
            'payload'  : paylod_js
        }
        f.write('{}\n'.format(json.dumps(log)))
 
print (USAGE)

if (len(sys.argv)>2):
    EXPERIMENT_ID = sys.argv[1]
    CONN        = sys.argv[2]
else:
    exit()

log_file_path = prepare_log_file() 

print (log_file_path)

if (CONN == "UDP"):
# epxeriment settings
    HOST = "10.90.90.2"
    PORT = 5005
    print ("UDP Server: %s" % HOST)
    print ("UDP Port: %s" % PORT)
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.bind((HOST, PORT))
    while True:
        data, addr = sock.recvfrom(65500) 
        log_data(data)
        
if (CONN == "TCP"):
    HOST = None               # Symbolic name meaning all available interfaces
    PORT = 50007              # Arbitrary non-privileged port
    
    print ("TCP Server: All Ifs")
    print ("TCP Port  : %s" % PORT)
    
    s = None
    pdb.set_trace()
    for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                                  socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.bind(sa)
            s.listen(1)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    if s is None:
        print('could not open socket')
        sys.exit(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(65500)
            if (getsizeof(data)>100):
                log_data(data)
            # if not data: break
            # conn.send(data)
