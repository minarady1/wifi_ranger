# -*- coding: utf-8 -*-
'''
Plottin script for captured measurements
Bugwright2 Prject
Mina Rady mina.rady@insa-lyon.fr
'''

import numpy as np
import matplotlib.pyplot as plt
import json


configs = [
    "WiFi-6 2.4 GHz\n 20 MHz",
    "WiFi-6 5 GHz \n 80 MHz",
    "WiFi-6 5 GHz \n 20 MHz",
    "WiFi-5 5 GHz \n 20 MHz", 
    "WiFi-4 2.4 GHz\n 20 MHz"]

# make data:
json_objects = []
data=[]

f = open('log1.json',)
while True:
    line = f.readline()
    if line:
        json_objects.append(json.loads(line))
    else:
        break


result_all = []
time_all  = []

for exp in json_objects:
    result = []
    time  = []
    for i in exp['intervals']:
        time.append (i ['sum']['start'])
        result.append(i ['sum']['bits_per_second'])
    time_all.append(time)
    result_all.append(result)

f.close()

def plotViolin (data, labels, xlimit, ylabel, tag , ylimit=None, step = None):
    # justifying the data
    i =0
    while (i< len(data)):
        data [i]= data[i][0:xlimit]
        i= i+1
    
    # plot:
    fig, ax = plt.subplots()
    ticks =  list(range(1,len(labels)+1))
    vp = ax.violinplot(data, ticks)
    # styling:
    for body in vp['bodies']:
        body.set_edgecolor('#000000')
        body.set_alpha(0.4)
    
    plt.xlabel('Configuration')
    ax.set_xticks(ticks)
    if (ylimit!=None):
        ax.set_yticks(np.arange(0,ylimit,step))
    ax.set_xticklabels(labels, rotation=45)
    plt.ylabel(ylabel)
    ax.grid(True)
    
    plt.savefig(tag+".png", dpi=300, bbox_inches='tight')
    
    plt.show()
    
def plotTimeseries (data, time, labels, xlimit, ylabel, tag , ylimit=None, step = None):

    
    # plot:
    plt.figure(figsize=(12, 8))
    i = 0
    while (i < len(data)):
        plt.plot(time [0], data [i], linewidth=3)
        i =i+1
    
    plt.tight_layout()
    plt.ylabel(ylabel)
    plt.savefig(tag+".png", dpi=300, bbox_inches='tight')
    
    plt.show()


plotViolin(result_all, ["UDP default l", "UDP max l" ], 30,  'TCP Throughput (Mbps)',  "location1_tcp_120s")


plotTimeseries(result_all, time_all, ["my config"], 30,  'TCP Throughput (Mbps)',  "location1_tcp_120s_time")

