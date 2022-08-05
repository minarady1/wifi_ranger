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
import os

duration = 180 #s 
expid = "loc1_n_20mhz_24ghz"
runid = "run6"
if len (sys.argv)>1:
    expid = sys.argv[1]
    runid = sys.argv[2]


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
    global runid
    global stream_configs
    global phy_configs
    global json_objects_data
    global labels
    global phy_df
    
    files = []
    
    
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
        line = f.readline()
        if line:
            json_objects_data.append(json.loads(line))
        f.close()
    
    return json_objects_data

def collectPhyData (grouping, filter_params):
    global runid
    global phy_df
    
    phy_files = []
    phy_dir = "../logs/{}/phy/".format(runid)
    phy_files = os.listdir(phy_dir)
    phy_df = pd.DataFrame(columns = ['timestamp', 'txrate', 'rxrate',
                             'rssi', 'mode'])

    for file in  phy_files:
        # print (file)
        f = open(phy_dir+file)
        line = f.read ()
        if line:
            # print (line)
            ts_string = file.replace(".htm","").replace("AutoSave_","")
            vals = line.split("/")
            txrate = int (vals [2].replace ("M",""))
            rxrate = int (vals [3].replace ("M",""))
            rssi   = int (vals [4]) *-1
            mode   = vals [5]
            phy_df = phy_df.append({'timestamp': int (ts_string[0:-3]),
                       'timestamp_ns' : int (ts_string),
                       'txrate' : txrate,
                       'rxrate' : rxrate,
                       'rssi': rssi,
                       'mode': mode}, ignore_index = True)
        f.close()

throughput_all = []
streaming_time_all  = []
phy_time_all  = []
pdr_all = []
pdr_labels = []
json_objects_data = []
data=[]
phy_df = pd.DataFrame()
time  = []
txrate_all = []
rxrate_all = [] 
mode_all  = []
rssi_all = []

def reset():
    global throughput_all
    global streaming_time_all  
    global phy_time_all 
    global pdr_all 
    global pdr_labels 
    global json_objects_data
    global data
    global labels
    global txrate_all
    global rxrate_all
    global mode_all
    global rssi_all
    
    throughput_all = []
    streaming_time_all  = []
    phy_time_all  = []
    pdr_all = []
    txrate_all = []
    rxrate_all = [] 
    mode_all  = []
    rssi_all = []
    pdr_labels= []
    json_objects_data = []
    data=[]
    labels = []
    

def processData ():
    global json_objects_data
    global throughput_all 
    global streaming_time_all  
    global phy_time_all
    global pdr_all 
    global duration
    global phy_df
    global txrate_all
    global rxrate_all
    global rssi_all
    global mode_all
    
    throughput = []
    c = 0
    for exp in json_objects_data:
        time  = []
        throughput = []
        pdr = []
        hasPDR = False
        ts_start = exp['start']['timestamp']['timesecs']
        ts_end = ts_start+duration
        res = phy_df.query("{}< timestamp <{}".format(ts_start, ts_end))
        
        phy_time = res ["timestamp"].tolist()
        st = phy_time[0]
        interval = phy_time[1] - phy_time[0]
        
        # shift the timestamps to end of the interval window
        phy_time = [(x - st + interval) for x in phy_time]
        txrate = res ["txrate"].tolist()
        rxrate = res ["rxrate"].tolist()
        rssi   = res ["rssi"].tolist()
        mode   = res ["mode"].tolist()
        
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
        phy_time_all.append (phy_time)
        throughput_all.append(throughput)
        txrate_all.append(txrate)
        rxrate_all.append(rxrate)
        rssi_all.append(rssi)
        mode_all.append(mode)
        
        if (len(pdr)>0):
            pdr_all.append(pdr)

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
        plt.plot(time [i][0:xlimit], data [i][0:xlimit], linewidth=3, label = labels [i])
        i =i+1
    
    plt.tight_layout()
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.title ("{} {}".format(tag,runid))
    plt.savefig(tag+"_time.png", dpi=300, bbox_inches='tight')
    
    #plt.show()


def plot(groupby, filter_params):
    global duration
    reset()
    collectPhyData(groupby, filter_params)
    collectStreamData(groupby, filter_params)
    processData()
    

    plotBox(throughput_all, labels, duration,  
               'Throughput (Mbps)', 
               filter_params["tag"]+"_throughput")
    
    

    plotTimeseries(txrate_all, phy_time_all, labels, duration, 
                  'Bitrate (Mbps)', 
                  filter_params["tag"]+"_txrate")
    
    
    plotTimeseries(rxrate_all, phy_time_all, labels, duration, 
              'Bitrate (Mbps)', 
              filter_params["tag"]+"_rxrate")
    
    
    plotTimeseries(rssi_all, phy_time_all, labels, duration, 
          'Bitrate (Mbps)', 
          filter_params["tag"]+"_rssi")
    
    
    if (len(pdr_all)>0):
        plotBox(pdr_all, pdr_labels, duration,  'PDR (%)',  filter_params["tag"]+ "_pdr")

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