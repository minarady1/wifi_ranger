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

# epxeriment settings

UDP_IP = "10.90.90.1"
UDP_PORT = 5005

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
    frame_len       = getsizeof(data) 
    print(seqnum)
    res = {
        "src_timestamp_ns"  : timestamp_ns,
        "seqnum"            : seqnum,
        "frame_len"         : frame_len
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
 

EXPERIMENT_ID = sys.argv[1]

log_file_path = prepare_log_file() 

print (log_file_path)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    log_data(data)