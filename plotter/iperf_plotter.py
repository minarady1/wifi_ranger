# -*- coding: utf-8 -*-
'''
Plotting script for captured measurements

PLotter v2.0

Bugwright2 Prject
Mina Rady mina.rady@insa-lyon.fr

'''

import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import pdb
import pandas as pd

expid = "loc1_n_20mhz_24ghz"
runid = "run6"
if len (sys.argv)>1:
    expid = sys.argv[1]
    runid = sys.argv[2]

controlfiles = [
    "../logs/{}/log_{}_{}_control_withTCPUL.jsonl".format(runid,expid,runid),
    "../logs/{}/log_{}_{}_control_withTCPULDL.jsonl".format(runid,expid,runid),
         ]
labels = [] 

exp_labels_streaming_pdr = [

              "UDP UL High (Rx)",            
              "UDP UL Low (Rx)",
              "UDP DL High",
              "UDP DL Low",
              ]

exp_labels_control = ["TCP  UL",  
              "TCP UL/DL",  
              ]

stream_configs = [ 
    "tcp_single_UL",
    "tcp_single_DL",
    
    "udp_single_UL",
    "udp_single_UL_server",
    
    # "udp_single_UL_low",
    # "udp_single_UL_low_server",
    
    "udp_single_DL",
    # "udp_single_DL_low",
]

stream_labels = [
              "TCP  UL",  
              "TCP DL",     
              
              "UDP UL High",
              "UDP UL High (Rx)",
              
              "UDP UL Low",
              "UDP UL Low (Rx)",
              
              "UDP DL High",
              "UDP DL Low",
              ]

phy_configs = [
    "ax_80mhz_5ghz",
    "ac_80mhz_5ghz",
    "ax_20mhz_5ghz",
    "ax_20mhz_24ghz",
    "ac_20mhz_5ghz",
    "n_20mhz_5ghz",
    "n_20mhz_24ghz",
    # "a_20mhz_5ghz", 
    # "g_20mhz_24ghz",
    ]

locations= ["loc1"]

def collectStreamData (grouping, filter_params):
    files = []
    global runid
    global stream_configs
    global phy_configs
    global json_objects_data
    global labels
    if (grouping == "phy_stream_config"):
        i = 0
        for config in stream_configs:
            server_dir = ""
            if "server" in config:
                server_dir = "server/"
            j = 0
            for phy in phy_configs:
                labels.append("{} {}".format(stream_labels[i], phy_configs[j]))
                j = j +1
                files.append("../logs/{}/{}{}_{}_{}_{}.json".format(runid,server_dir,filter_params["location"], phy ,runid, config))
            i = i +1
    if (grouping == "stream_config"):
        i = 0
        for config in stream_configs:
            if config != filter_params["stream_config"]:
                i = i +1
                continue
            server_dir = ""
            if "server" in config:
                server_dir = "server/"
            j = 0
            for phy in phy_configs:
                labels.append("{} {}".format(stream_labels[i], phy))
                files.append("../logs/{}/{}{}_{}_{}_{}.json".format(runid,server_dir,filter_params["location"], phy ,runid, config))
            i = i +1

    for file in  files:
        f = open(file)
        print (file)
        line = f.readline()
        if line:
            json_objects_data.append(json.loads(line))
        f.close()
    return json_objects_data

# process manual control files    
# for file in controlfiles:
#     f = open(file)
#     file_json_array=[]
#     while True:
#         line = f.readline()
#         if not line:
#             break
#         if line:
#             file_json_array.append(json.loads(line))
#     json_objects_control.append(file_json_array)
#     f.close()

throughput_all = []
streaming_time_all  = []
pdr_all = []
pdr_labels = []
json_objects_data = []
data=[]

control_time_all  = []
time  = []
delay_all = []
loss_all = []

def reset():
    global throughput_all
    global streaming_time_all  
    global pdr_all 
    global pdr_labels 
    global json_objects_data
    global data
    global labels

    throughput_all = []
    streaming_time_all  = []
    pdr_all = []
    pdr_labels= []
    json_objects_data = []
    data=[]
    labels = []
    

def processData ():
    global json_objects_data
    global throughput_all 
    global streaming_time_all  
    global pdr_all 
    throughput = []
    c = 0
    for exp in json_objects_data:
        time  = []
        throughput = []
        pdr = []
        hasPDR = False
        for i in exp['intervals']:
            time.append (i ['sum']['start'])
            throughput.append (i ['sum']['bits_per_second']/ 10**6)
            if "lost_percent" in i ['sum']:
                hasPDR = True
                pdr.append(100 - i ['sum']['lost_percent'])
        
        if (hasPDR):
            pdr_labels.append(labels[c])
        c= c+1
        streaming_time_all.append(time)
        throughput_all.append(throughput)
        if (len(pdr)>0):
            pdr_all.append(pdr)
        
# for exp_array in json_objects_control:
#     time  = []
#     delay = []
#     loss = []
#     start_time = 0
#     prev_seqnum = -1
    
#     for i in exp_array:
#         delay.append(( i ["timestamp"]- i ["payload"] ["src_timestamp_ns"])/10**6)
        
#         if prev_seqnum == -1:
#             loss.append(0)
#             start_time = i ["timestamp"]
#         else:
#             loss.append(i ["payload"] ["seqnum"]-prev_seqnum-1)
#         prev_seqnum = i ["payload"] ["seqnum"]            
        
#         time.append ((i ["timestamp"]-start_time)/10**9)
       
        
#     control_time_all.append(time)
#     delay_all.append(delay)
#     loss_all.append(loss)


def plotViolin (data, labels, xlimit, ylabel, tag , ylimit=None, step = None):
    # justifying the data
    i =0
    while (i< len(data)):
        data [i]= data[i][0:xlimit]
        i= i+1
    
    # plot:
    fig, ax = plt.subplots()
    ticks =  list(range(1,len(labels)+1))
    try:
        vp = ax.violinplot(data, ticks)
    except:
        pdb.set_trace()
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
    ax.set_xticklabels(labels, rotation=90, size = 10)
    plt.title ("{} {}".format(tag,runid))
    plt.savefig(tag+"_violin.png", dpi=400, bbox_inches='tight', rotation = 90)
    
    #plt.show()

def plotBox (data, labels, xlimit, ylabel, tag , ylimit=None, step = None):
    # justifying the data
    i =0
    while (i< len(data)):
        data [i]= data[i][0:xlimit]
        i= i+1
    
    # plot:
    df = pd.DataFrame(data, index=labels)

    
    fig, ax = plt.subplots()
    ticks =  list(range(1,len(labels)+1))
    try:
        df.T.boxplot(vert=False)
        plt.subplots_adjust(left=0.25)
    except:
        pdb.set_trace()

    plt.ylabel('Configuration')
    plt.xlabel(ylabel)
    #ax.set_xticks(ticks)
    if (ylimit!=None):
        ax.set_yticks(np.arange(0,ylimit,step))

    ax.grid(True)
    #ax.set_xticklabels(labels, rotation=90, size = 10)
    plt.title ("{} {}".format(tag,runid))
    plt.savefig(tag+"_box.png", dpi=400, bbox_inches='tight', rotation = 90)
    
    
def plotTimeseries (data, time, labels, xlimit, ylabel, tag , ylimit=None, step = None):
    
    # plot:
    plt.figure(figsize=(12, 8))
    i = 0
    while (i < len(data)):
        plt.plot(time [0][0:xlimit], data [i][0:xlimit], linewidth=3, label = labels [i])
        i =i+1
    
    plt.tight_layout()
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.title ("{} {}".format(tag,runid))
    plt.savefig(tag+"_time.png", dpi=300, bbox_inches='tight')
    
    #plt.show()


def plot(groupby, filter_params):
    reset()
    collectStreamData(groupby, filter_params)
    processData()
    
    # plotViolin(throughput_all, labels, 180,  
    #           'Throughput (Mbps)', 
    #           filter_params["tag"]+"_throughput")
    plotBox(throughput_all, labels, 180,  
               'Throughput (Mbps)', 
               filter_params["tag"]+"_throughput")
    plotTimeseries(throughput_all, streaming_time_all, labels, 180, 
                  'Throughput (Mbps)', 
                  filter_params["tag"]+"_throughput")
    
    if (len(pdr_all)>0):
        # plotViolin(pdr_all, pdr_labels, 180,  'PDR (%)',  filter_params["tag"]+ "_pdr")
        plotBox(pdr_all, pdr_labels, 180,  'PDR (%)',  filter_params["tag"]+ "_pdr")

# phy_stream_config
# phy_stream 

# group by stream type
    
i = 0
j = 0

while (i<len(locations)):
    while (j<len(stream_configs)):
        
        plot("stream_config", {"location":locations[i],
                                 "stream_config": stream_configs[j],
                                 "tag": "{}_stream_{}_{}".format(locations[i],
                                                                    stream_configs[j],
                                                                    runid)})
        j = j+1
    i=i+1
# group by phy type
    
# all

print ("Done.")
sys.exit()