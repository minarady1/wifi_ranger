# -*- coding: utf-8 -*-
'''
Plotting script for captured measurements

PLotter v2.0

Bugwright2 Project
Mina Rady mina.rady@insa-lyon.fr

'''

import numpy as np
import matplotlib.pyplot as plt
import json
import sys
import pdb
import pandas as pd
import os

duration = 300 #s 
expid = "cortex"
runid = "run8"
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
    "tcp_single_UL_server",
    
    "tcp_single_DL",
    "tcp_single_DL_server",
    
    "tcp_dual_UL",
    "tcp_dual_UL_server",
    
    "tcp_dual_DL",
    "tcp_dual_DL_server",
    
    "udp_single_UL",
    "udp_single_UL_server",
    
    "udp_single_DL",
    "udp_single_DL_server",
    
    "udp_dual_UL",
    "udp_dual_UL_server",
    
    "udp_dual_DL",
    "udp_dual_DL_server",
]

stream_labels = [
    "tcp_single_UL",
    "tcp_single_UL_server",
    
    "tcp_single_DL",
    "tcp_single_DL_server",
    
    "tcp_dual_UL",
    "tcp_dual_UL_server",
    
    "tcp_dual_DL",
    "tcp_dual_DL_server",
    
    "udp_single_UL",
    "udp_single_UL_server",
    
    "udp_single_DL",
    "udp_single_DL_server",
    
    "udp_dual_UL",
    "udp_dual_UL_server",
    
    "udp_dual_DL",
    "udp_dual_DL_server",
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

locations= ["cortex"]

line_styles= [
     'dashed',
     'dotted',
     'dashed',
     'dotted',
     'dashed',
     'dashdot',
     'dashdot',
    ]
marker_styles= [
     'o',
     's',
     '+',
     'x',
     '_',
     'o',
     's',
    ]
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
            if (len(vals)<6):
                break;
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
tcp_labels = []
retransmits_all = []
rtt_all = []

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
    global tcp_labels 
    global json_objects_data
    global data
    global labels
    global txrate_all
    global rxrate_all
    global mode_all
    global rssi_all
    global retransmits_all
    global rtt_all
    
    throughput_all = []
    streaming_time_all  = []
    phy_time_all  = []
    pdr_all = []
    txrate_all = []
    rxrate_all = [] 
    mode_all  = []
    rssi_all = []
    pdr_labels= []
    tcp_labels= []
    json_objects_data = []
    data=[]
    labels = []
    retransmits_all = []
    rtt_all = []
    

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
    global retransmits_all
    global rtt_all
    
    
    c = 0
    for exp in json_objects_data:
        time  = []
        throughput = []
        retransmits = []
        rtt = []
        pdr = []
        isUDP = False
        isTCP  = False
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
        print (">>", labels[c], set(mode) )
        
        for i in exp['intervals']:
            time.append (i ['sum']['start'])
            throughput.append (i ['sum']['bits_per_second']/ 10**6)
            if "retransmits" in i ['sum']:
                isTCP = True
                retransmits.append(i ['sum']['retransmits'])
                rtt.append (i['streams'][0]['rtt'])
            
            if "lost_percent" in i ['sum']:
                isUDP = True
                pdr.append(100 - i ['sum']['lost_percent'])
        
        
        streaming_time_all.append(time)
        phy_time_all.append (phy_time)
        throughput_all.append(throughput)
        txrate_all.append(txrate)
        rxrate_all.append(rxrate)
        rssi_all.append(rssi)
        mode_all.append(mode)

        if (isUDP):
            pdr_labels.append(labels[c])
            pdr_all.append(pdr)
        
        if (isTCP):
            tcp_labels.append(labels[c])
            retransmits_all.append(retransmits)
            rtt_all.append(rtt)
        c= c+1
            
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

def plotCDF (data, labels, xlimit, ylabel, tag , ylimit=None, step = None):
    
    plt.figure(figsize=(12, 8))
    
    i = 0
    while (i < len(data)):
        count, bins_count = np.histogram(data [i][0:xlimit], bins=30)
        pdf = count / sum(count)
        cdf = np.cumsum(pdf)
        plt.plot(bins_count[1:],cdf,label= labels [i],
                 linestyle= line_styles[i], marker = marker_styles[i])
        i =i+1
    
    plt.tight_layout()
    plt.xlabel(ylabel)
    plt.ylabel("CDF")
    plt.legend()
    plt.grid(True)
    plt.title ("{} {}".format(tag,runid))
    plt.savefig(tag+"_cdf.png", dpi=300, bbox_inches='tight')

def plotPDF (data, labels, xlimit, ylabel, tag , ylimit=None, step = None):
    
    plt.figure(figsize=(12, 8))
    fig, ax = plt.subplots()
    i = 0
    width = 1
    while (i < len(data)):
        count, bins_count = np.histogram(data [i][0:xlimit], bins=10)
        pdf = count / sum(count)
        ax.bar(bins_count[1:],pdf,label= labels [i])
        i =i+1
    
    
    plt.xlabel(ylabel)
    plt.ylabel("PDF")
    plt.legend()
    plt.grid(True)
    plt.title ("{} {}".format(tag,runid))
    plt.tight_layout()
    plt.savefig(tag+"_pdf.png", dpi=300, bbox_inches='tight')
    
def plot(groupby, filter_params):
    global duration
    reset()
    collectPhyData(groupby, filter_params)
    collectStreamData(groupby, filter_params)
    processData()
    

    plotBox(throughput_all, labels, duration,  
                'Throughput (Mbps)', 
                filter_params["tag"]+"_throughput")

    plotCDF(throughput_all, labels, duration,  
                'Throughput (Mbps)', 
                filter_params["tag"]+"_throughput")    

    plotTimeseries(txrate_all, phy_time_all, labels, duration, 
                  'Bitrate (Mbps)', 
                  filter_params["tag"]+"_txrate")
    
    plotCDF(txrate_all, labels, duration, 
                  'Bitrate (Mbps)', 
                  filter_params["tag"]+"_txrate")    

    plotPDF(txrate_all, labels, duration, 
                  'Bitrate (Mbps)', 
                  filter_params["tag"]+"_txrate")    
    
    plotTimeseries(rxrate_all, phy_time_all, labels, duration, 
              'Bitrate (Mbps)', 
              filter_params["tag"]+"_rxrate")
    
    
    plotTimeseries(rssi_all, phy_time_all, labels, duration, 
          'RSSI (dBm)', 
          filter_params["tag"]+"_rssi")
    
    plotTimeseries(throughput_all, streaming_time_all, labels, duration,  
                'Throughput (Mbps)', 
                filter_params["tag"]+"_throughput")
    
    
    
    if (len(pdr_all)>0):
        plotBox(pdr_all, pdr_labels, duration,  'PDR (%)',  filter_params["tag"]+ "_pdr")

    if (len(retransmits_all)>0):
        plotPDF(retransmits_all, tcp_labels, duration,  'Retries',  
                filter_params["tag"]+ "_retries")
    if (len(rtt_all)>0):
        plotTimeseries(rtt_all, streaming_time_all, tcp_labels, duration,  'RTT',  
                filter_params["tag"]+ "_rtt")

    
i = 0


while (i<len(locations)):
    print (locations[i])
    j = 0   
    while (j<len(stream_configs)):
        
        plot("stream_config", {"location":locations[i],
                                 "stream_config": stream_configs[j],
                                 "tag": "{}_stream_{}_{}".format(stream_configs[j],
                                                                    runid,
                                                                    locations[i])})
        j = j+1
    i=i+1
# group by phy type
    
# all

print ("Done.")
sys.exit()