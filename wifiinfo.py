'''
Script to do passive scanning of WiFi interface using NetInfoView tool
It runs the scan for a priod of time and stores it into json format


Bugwright2 Prject

Mina Rady mina.rady@insa-lyon.fr
'''

import logging
import os
import io
import time
import subprocess
import sys
from subprocess import check_output

print (sys.argv)
expID = sys.argv[1]
runID = sys.argv[2]
DURATION     = int(sys.argv[3])
period = 1

start = time.time()
counter = 1
now = start
while (now-start < DURATION):
    print ((now-start )/10**6)
    log_file_name = "logs/{}_{}_{}_wifi.json".format(expID,runID, counter)
    counter =counter +1
    out = subprocess.run( ["WifiInfoView", "/DisplayMode", "1" ,"/sjson", log_file_name], shell=True, check=True, capture_output=True)
    time.sleep(1)
    now = time.time()
 
print ("done, exiting  ...")
sys.exit()
