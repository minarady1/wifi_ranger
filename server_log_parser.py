# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 10:52:16 2022

@author: Mina Rady Local
"""
import json
import sys
import os
from pathlib import Path


# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.

log_dir_path = os.path.join(os.path.dirname(__file__), "logs")

def toFile (string):
    json_file = json.loads(string)
    if ( "title" in json_file):
        print (json_file["title"])
        log_file_name = "run5/server/{}_server.json".format(json_file["title"])
        file_path = os.path.join(log_dir_path, log_file_name)
        clean_out= string.replace('\r','').replace('\n','')
        
        with open(file_path, 'w+') as f:
            f.write('{}\n'.format(clean_out))
            f.close()
        

files  = [
"logs/run5/server/log_run0208_1_.json",
"logs/run5/server/log_run0208_1__2.json",
"logs/run5/server/log_run0208_2_.json",
"logs/run5/server/log_run0208_2__2.json",
]

for file_dir in files:
    file = open(file_dir, "r")
    out= file.read()
    file.close()
    # print (out)
    
    i = 0
    buffer = ""
    count_left = 0
    count_right = 0
    element_count = 0
    
    while i <len (out):
        buffer+=out[i]
        if out [i] == "{":
            count_left = count_left+1
        else:
            if out [i] == "}":
                count_right = count_right+1
        if count_left==count_right and (len(buffer)>2):
            toFile(buffer)
            buffer = ""
            count_left = 0
            count_right = 0
            element_count =element_count+1
        i = i+1
        
    print ("done: ", element_count)