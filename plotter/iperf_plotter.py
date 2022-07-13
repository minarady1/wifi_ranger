# -*- coding: utf-8 -*-
'''
Plottin script for captured measurements
Bugwright2 Prject
Mina Rady mina.rady@insa-lyon.fr
'''

import numpy as np
import matplotlib.pyplot as plt
import json




# make data:
json_objects = []
data=[]

files = ["../logs/loc1_24GHz_n_run2_tcpstream.json",
         "../logs/loc1_24GHz_n_run2_udpstream.json",
         ]
exp_labels = ["TCP Stream", "UDP Stream"]

for file in files:
    f = open(file)
    line = f.readline()
    print (line)
    if line:
        json_objects.append(json.loads(line))


throughput_all = []
throughput = []
plr_all = []
time_all  = []
time  = []

for exp in json_objects:
    time  = []
    throughput = []
    plr = []
    for i in exp['intervals']:
        time.append (i ['sum']['start'])
        throughput.append (i ['sum']['bits_per_second']/ 10**6)
        if "lost_percent" in i ['sum']:
            plr.append(i ['sum']['lost_percent'])
    time_all.append(time)
    throughput_all.append(throughput)
    
    if (len(plr)>0):
        plr_all.append(plr)
        
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

    plt.ylabel(ylabel)
    ax.grid(True)
    ax.set_xticklabels(labels, rotation=45)
    plt.savefig(tag+".png", dpi=300, bbox_inches='tight')
    
    plt.show()
    
def plotTimeseries (data, time, labels, xlimit, ylabel, tag , ylimit=None, step = None):

    
    # plot:
    plt.figure(figsize=(12, 8))
    i = 0
    while (i < len(data)):
        plt.plot(time [0], data [i], linewidth=3, label = labels [i])
        i =i+1
    
    plt.tight_layout()
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.savefig(tag+".png", dpi=300, bbox_inches='tight')
    
    plt.show()


plotViolin(throughput_all, exp_labels, 15,  'Throughput (Mbps)',  "location1_tcp_120s")


plotTimeseries(throughput_all, time_all, exp_labels, 15,  'Throughput (Mbps)',  "location1_tcp_120s_time")

