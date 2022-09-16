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
import time



#--------------------------- Global variables ---------------------------------

duration = 300 #s 
expid = "cortex"
runid = "run8"
phy_data_lookup = False
current_location = ""

if len (sys.argv)>1:
    expid = sys.argv[1]
    runid = sys.argv[2]

# labels of phy_streamtype statistics

labels = [] 

# labels of global phy statistics

labels_phy = []

locations= [
    "cortex",
    "cortex_asus",
    ]
locations_labels= [
    "TP-Link",
    "Asus",
    ]

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
    # "tcp_single_UL_server",
    
    "tcp_single_DL",
    # "tcp_single_DL_server",
    
    "tcp_dual_UL",
    # "tcp_dual_UL_server",
    
    "tcp_dual_DL",
    # "tcp_dual_DL_server",
    
    # "udp_single_UL",
    "udp_single_UL_server",
    
    "udp_single_DL",
    # "udp_single_DL_server",
    
    # "udp_dual_UL",
    # "udp_dual_UL_server",
    
    # "udp_dual_DL",
    # "udp_dual_DL_server",
 ]

stream_labels = [
    "tcp_single_UL",
    # "tcp_single_UL_server",
    
    "tcp_single_DL",
    # "tcp_single_DL_server",
    
    "tcp_dual_UL",
    # "tcp_dual_UL_server",
    
    "tcp_dual_DL",
    # "tcp_dual_DL_server",
    
    # "udp_single_UL",
    "udp_single_UL_server",
    
    "udp_single_DL",
    # "udp_single_DL_server",
    
    # "udp_dual_UL",
    # "udp_dual_UL_server",
    
    # "udp_dual_DL",
    # "udp_dual_DL_server",
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


#--------------------------- Declarations -------------------------------------

throughput_all = []
throughput_global = {}
throughput_90th_all = {}
pdr_90th_all = {}
txrate_global = {}

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




def collectStreamData (grouping, filter_params):
    global runid
    global stream_configs
    global phy_configs
    global json_objects_data
    global labels
    global labels_phy
    global phy_df
    current_location = filter_params["location"]
    files = []
    global files_global 
    
    
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
                files.append("../logs/{}/{}{}_{}_{}_{}.json".format(
                    runid,server_dir,filter_params["location"], phy ,runid, 
                    config))
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
                labels_phy.append(phy)
                files.append("../logs/{}/{}{}_{}_{}_{}.json".format(
                        runid, server_dir, filter_params["location"], phy, 
                        runid, config))
            i = i +1

    for file in  files:
        f = open(file)
        line = f.readline()
        if line:
            json_objects_data.append(json.loads(line))
        f.close()
    
    return json_objects_data

def collectPhyData ():
    global runid
    global phy_df
    
    phy_dir = "../logs/{}/phy/phy_log.txt".format(runid)
    phy_df = pd.DataFrame(columns = ['timestamp', 'txrate', 'rxrate',
                             'rssi', 'mode'])

    # print (file)
    f = open(phy_dir)
    lines= f.readlines()
    i = 0
    for line in lines:        
        if line:
            js = json.loads(line)
            phy_df = phy_df.append({'timestamp': js["timestamp"],
                       'txrate' : js["txrate"],
                       'rxrate' : js["rxrate"],
                       'rssi': js["rssi"],
                       'mode': js["mode"]}, ignore_index = True)
            i = i+1
    f.close()


def reset():
    global streaming_time_all  
    global throughput_all 
    global phy_time_all 
    global pdr_all 
    global pdr_labels 
    global tcp_labels 
    global data
    global labels
    global txrate_all
    global rxrate_all
    global mode_all
    global rssi_all
    global retransmits_all
    global rtt_all
    global locations
    global json_objects_data
    
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
    data=[]
    labels = []
    retransmits_all = []
    rtt_all = []
    json_objects_data = []
    
def processData (filter_params):
    global json_objects_data
    global throughput_all 
    global throughput_90th_all
    global throughput_global
    global pdr_90th_all
    global txrate_global
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
    current_location = filter_params ["location"]
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
        
        throughput_all.append(throughput)            
        streaming_time_all.append(time)
        
        throughput_global [current_location] [labels_phy[c]] [filter_params ["stream_config"]]= throughput
        
        # add the 90th percentile to the global values of this PHY
        
        if (labels_phy[c] in throughput_90th_all[current_location].keys()):
            throughput_90th_all [current_location] [labels_phy[c]].append(np.percentile(throughput,90))
        else:
            throughput_90th_all [current_location] [labels_phy[c]] = [np.percentile(throughput,90)]
        
        if (isUDP):
            pdr_labels.append(labels[c])
            pdr_all.append(pdr)
            
            if (labels_phy[c] in pdr_90th_all.keys()):
                pdr_90th_all [labels_phy[c]].append(np.percentile(pdr,90))
            else:
                pdr_90th_all[labels_phy[c]] = [np.percentile(pdr,90)]
        
        if (isTCP):
            tcp_labels.append(labels[c])
            retransmits_all.append(retransmits)
            rtt_all.append(rtt)
        
        if (phy_data_lookup):
            
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
            phy_time_all.append (phy_time)
            txrate_all.append(txrate)
            rxrate_all.append(rxrate)
            rssi_all.append(rssi)
            mode_all.append(mode)
            
            # add the txrate of this phy
            if (labels_phy[c] in txrate_global.keys()):
                txrate_global [labels_phy[c]].extend(txrate)
            else:
                txrate_global[labels_phy[c]] = txrate
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

    # merging the columns for each location.
    i =0
    
    # justifying the data to the set max limit
    while (i< len(data)):
        data [i]= data[i][0:xlimit]
        i= i+1
   
    try:
        df = pd.DataFrame(data, index=labels)
    except:
        pdb.set_trace()
    fig, ax = plt.subplots()
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


def plotGlobal (data_dict, ylabel, tag, stream ):
    global phy_configs
    global_values = []
    global_keys   = []
    
    # plot:
    
    for c in phy_configs:
        i = 0
        for l in locations:
            global_keys.append ( c+"_"+locations_labels[i])
            global_values.append ( list(data_dict[l][c][stream]))
            i=i+1

    df = pd.DataFrame(global_values, index=global_keys)
    fig, ax = plt.subplots()
    bp_dict = df.T.boxplot(vert=False, return_type='both', patch_artist = True)
    plt.subplots_adjust(left=0.25)
    
    i = 0
    for box in bp_dict[1]["boxes"]:
        box.set_facecolor("w")
        if (i%2 ==0):
            box.set_edgecolor("g")
        else:
            box.set_edgecolor("b")
        i = i+1
    plt.ylabel('Configuration')
    plt.xlabel(ylabel)
    #ax.set_xticks(ticks)

    ax.grid(True)
    #ax.set_xticklabels(labels, rotation=90, size = 10)
    plt.title ("{} {}".format(tag,runid))
    plt.savefig(tag+"_box_global.png", dpi=400, bbox_inches='tight', rotation = 90)
    

def plotGlobalPercentiles (data_dict, ylabel, tag ):
    global phy_configs
    global_values = []
    global_keys   = []
    
    # plot:
    
    for c in phy_configs:
        i = 0
        for l in locations:
            global_keys.append ( c+"_"+locations_labels[i])
            global_values.append ( list(data_dict[l][c]))
            i=i+1

    df = pd.DataFrame(global_values, index=global_keys)
    fig, ax = plt.subplots()
    bp_dict = df.T.boxplot(vert=False, return_type='both', patch_artist = True)
    plt.subplots_adjust(left=0.25)
    
    i = 0
    for box in bp_dict[1]["boxes"]:
        box.set_facecolor("w")
        if (i%2 ==0):
            box.set_edgecolor("g")
        else:
            box.set_edgecolor("b")
        i = i+1
    plt.ylabel('Configuration')
    plt.xlabel(ylabel)
    #ax.set_xticks(ticks)

    ax.grid(True)
    #ax.set_xticklabels(labels, rotation=90, size = 10)
    plt.title ("{} {}".format(tag,runid))
    plt.savefig(tag+"_box_global_per.png", dpi=400, bbox_inches='tight', rotation = 90)
    
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
    plt.ylim([0,1])
    plt.legend()
    plt.grid(True)
    plt.title ("{} {}".format(tag,runid))
    plt.savefig(tag+"_cdf.png", dpi=300, bbox_inches='tight')



def plotPDF (data, labels, xlimit, ylabel, tag , ylimit=None, step = None):
    
    plt.figure(figsize=(12, 8))
    fig, ax = plt.subplots()
    i = 0
    while (i < len(data)):
        count, bins_count = np.histogram(data [i][0:xlimit], bins=10)
        pdf = count / sum(count)
        ax.bar(bins_count[1:]+((1/3)*i),pdf,label= labels [i], linewidth = 2, alpha = 0.5, width = 1/3)
        i =i+1
    
    
    plt.xlabel(ylabel)
    plt.ylabel("PDF")
    plt.legend(phy_configs)
    plt.grid(True)
    plt.title ("{} {}".format(tag,runid))
    plt.tight_layout()
    plt.savefig(tag+"_pdf.png", dpi=300, bbox_inches='tight')

def plotPDFMultiple (data, labels, xlimit, ylabel, tag , ylimit=None, step = None):
    
    plt.figure(figsize=(48, 4))
    figure, axis = plt.subplots(len(data), 1)
    i = 0
    while (i < len(data)):
        count, bins_count = np.histogram(data [i][0:xlimit], bins=10)
        pdf = count / sum(count)
        axis[i].bar(bins_count[1:],pdf,label= labels [i], width = 10)
       # axis[i].legend()
        axis[i].grid(True)
        axis[i].set_xlim([0,1300])
        axis[i].set_ylim([0,1])
        axis[i].set_title(labels [i])
        i =i+1

    # plt.ylabel(ylabel)
    # plt.title ("{} {}".format(tag,runid))
    plt.tight_layout()
    plt.show()
    plt.savefig(tag+"_pdfmulti.png", dpi=300)
  
    
def plot(groupby, filter_params):
    global duration
    reset()
    
    collectStreamData(groupby, filter_params)
    processData(filter_params)
    
    
    # plotBox(throughput_all, labels, duration,  
    #             'Throughput (Mbps)', 
    #             filter_params["tag"]+"_throughput")

    # plotCDF(throughput_all, labels, duration,  
    #             'Throughput (Mbps)', 
    #             filter_params["tag"]+"_throughput")    


    # plotTimeseries(throughput_all, streaming_time_all, labels, duration,  
    #             'Throughput (Mbps)', 
    #             filter_params["tag"]+"_throughput")
    
    # if (phy_data_lookup):
       
        # plotPDFMultiple(txrate_all, labels, duration, 
                      # 'Bitrate (Mbps)', 
                      # filter_params["tag"]+"_txrate")    
    
        # plotCDF(rxrate_all, labels, duration, 
        #           'Bitrate (Mbps)', 
        #           filter_params["tag"]+"_rxrate")
    
    
    # plotCDF(rssi_all, labels, duration, 
    #       'RSSI (dBm)', 
    #       filter_params["tag"]+"_rssi")
           
        
    # if (len(pdr_all)>0):
    #     plotBox(pdr_all, pdr_labels, duration,  'PDR (%)',  filter_params["tag"]+ "_pdr")

    # if (len(retransmits_all)>0):
    #     print ("here")
    #     plotCDF(retransmits_all, tcp_labels, duration,  'Retries',  
    #             filter_params["tag"]+ "_retries")
    # if (len(rtt_all)>0):
    #     plotCDF(rtt_all, tcp_labels, duration,  'RTT',  
    #             filter_params["tag"]+ "_rtt")
    

# initializing global data holders

for loc in locations: 
    throughput_90th_all [loc] = {}
    throughput_global [loc]   = {}
    for phy in phy_configs: 
        throughput_global [loc] [phy] = {}
        for s in stream_configs:
            throughput_global [loc] [phy] [s] = []


if (phy_data_lookup):
    collectPhyData()

tag_template = "{}_stream_{}_{}"
i = 0
while (i<len(locations)):
    print (locations[i])
    j = 0   
    while (j<len(stream_configs)):
        
        plot("stream_config", {
            "location":locations[i],
            "stream_config": stream_configs[j],
            "tag": tag_template.format(stream_configs[j],
            runid,
            locations[i])})
        
        
        j = j+1
    i=i+1
    
# all


j = 0   
while (j<len(stream_configs)):
    plotGlobal(throughput_global,"Mbps", "{}_stream_{}".format(stream_configs[j],
        runid,)+"_throughput" , 
        stream_configs[j])
    j=j+1


# plotGlobalPercentiles(throughput_90th_all,"Mbps", "throughput_90th")
# same for retries
# same for tx/rx rate
    
# plotGlobal(pdr_90th_all,"%", "pdr_90th")

# plotGlobal(txrate_global,"Mbps", "txrate_global")
print ("Done.")
sys.exit()