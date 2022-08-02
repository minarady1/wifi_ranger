# -*- coding: utf-8 -*-
'''
Plottin script for captured measurements
Bugwright2 Prject
Mina Rady mina.rady@insa-lyon.fr
'''

import numpy as np
import matplotlib.pyplot as plt
import json
import sys

expid = "loc1_n_20mhz_24ghz"
runid = "run1"
if len (sys.argv)>1:
    expid = sys.argv[1]
    runid = sys.argv[2]

# make data:
json_objects_data = []
json_objects_control = []
data=[]


streamfiles = [
    "../logs/{}/{}_{}_tcp_single_UL.json".format(runid,expid,runid),
    "../logs/{}/{}_{}_tcp_single_DL.json".format(runid,expid,runid),
    
    "../logs/{}/{}_{}_udp_single_UL.json".format(runid,expid,runid),
    "../logs/{}/server/{}_{}_udp_single_UL_server.json".format(runid,expid,runid),
    
    "../logs/{}/{}_{}_udp_single_UL_low.json".format(runid,expid,runid),
    "../logs/{}/server/{}_{}_udp_single_UL_low_server.json".format(runid,expid,runid),
    
    "../logs/{}/{}_{}_udp_single_DL.json".format(runid,expid,runid),
    "../logs/{}/{}_{}_udp_single_DL_low.json".format(runid,expid,runid),
    # "../logs/{}/{}_{}_tcp_UL.json".format(runid,expid,runid),    
    # "../logs/{}/{}_{}_tcp_DL.json".format(runid,expid,runid),
    # "../logs/{}/{}_{}_tcpstreamUDPDL.json".format(runid,expid,runid),
    # "../logs/{}/{}_{}_tcpstreamULUDP.json".format(runid,expid,runid),
    
    # "../logs/{}/{}_{}_udpstreamsingleUL.json".format(runid,expid,runid),
    # "../logs/{}/{}_{}_udpstreamsingleUL_server.json".format(runid,expid,runid),
    # "../logs/{}/{}_{}_udpstreamUL.json".format(runid,expid,runid),
    # "../logs/{}/{}_{}_udpstreamUL_server.json".format(runid,expid,runid),    
    # "../logs/{}/{}_{}_udpstreamDL.json".format(runid,expid,runid),
    # "../logs/{}/{}_{}_udpstream_TCPDL.json".format(runid,expid,runid),
    # "../logs/{}/{}_{}_udpstream_TCPDL_server.json".format(runid,expid,runid),
    # "../logs/{}/{}_{}_udpstream_DLTCP.json".format(runid,expid,runid),
         ]

controlfiles = [
    "../logs/{}/log_{}_{}_control_withTCPUL.jsonl".format(runid,expid,runid),
    "../logs/{}/log_{}_{}_control_withTCPULDL.jsonl".format(runid,expid,runid),
    # "../logs/{}/log_{}_{}_control_withTCPULUDPDL.jsonl".format(runid,expid,runid),
    # "../logs/{}/log_{}_{}_control_withUDPUL.jsonl".format(runid,expid,runid),
    # "../logs/{}/log_{}_{}_control_withUDPULDL.jsonl".format(runid,expid,runid),
    # "../logs/{}/log_{}_{}_control_withUDPULTCPDL.jsonl".format(runid,expid,runid),
         ]
exp_labels_streaming = [
              "TCP  UL",  
              "TCP DL",     
              
              "UDP UL High",
              "UDP UL High (Rx)",
              
              "UDP UL Low",
              "UDP UL Low (Rx)",
              
              "UDP DL High",
              "UDP DL Low",
              ]

exp_labels_streaming_pdr = [

              "UDP UL High (Rx)",            
              "UDP UL Low (Rx)",
              "UDP DL High",
              "UDP DL Low",
              ]

exp_labels_control = ["TCP  UL",  
              "TCP UL/DL",  
              # "TCP  UL/UDP DL", 
              # "UDP DL (w/ TCP UL)", 
              
              # "UDP UL",  
              # "UDP UL/DL)",  
              # "UDP UL (w/ TCP DL)", 
              ]

for file in  streamfiles:
    f = open(file)
    print (file)
    line = f.readline()
    if line:
        json_objects_data.append(json.loads(line))
    f.close()

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
throughput = []
pdr_all = []
pdr_labels = []
streaming_time_all  = []


control_time_all  = []
time  = []
delay_all = []
loss_all = []

for exp in json_objects_data:
    time  = []
    throughput = []
    pdr = []
    for i in exp['intervals']:
        time.append (i ['sum']['start'])
        throughput.append (i ['sum']['bits_per_second']/ 10**6)
        if "lost_percent" in i ['sum']:
            pdr.append(100 - i ['sum']['lost_percent'])
    streaming_time_all.append(time)
    throughput_all.append(throughput)
    
    if (len(pdr)>0):
        pdr_all.append(pdr)
        
for exp_array in json_objects_control:
    time  = []
    delay = []
    loss = []
    start_time = 0
    prev_seqnum = -1
    
    for i in exp_array:
        delay.append(( i ["timestamp"]- i ["payload"] ["src_timestamp_ns"])/10**6)
        
        if prev_seqnum == -1:
            loss.append(0)
            start_time = i ["timestamp"]
        else:
            loss.append(i ["payload"] ["seqnum"]-prev_seqnum-1)
        prev_seqnum = i ["payload"] ["seqnum"]            
        
        time.append ((i ["timestamp"]-start_time)/10**9)
       
        
    control_time_all.append(time)
    delay_all.append(delay)
    loss_all.append(loss)


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
    ax.set_xticklabels(labels, rotation=90)
    plt.title ("{} {}".format(expid,runid))
    plt.savefig(tag+".png", dpi=300, bbox_inches='tight')
    
    #plt.show()
    
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
    plt.title ("{} {}".format(expid,runid))
    plt.savefig(tag+".png", dpi=300, bbox_inches='tight')
    
    #plt.show()


plotViolin(throughput_all, exp_labels_streaming, 180,  'Throughput (Mbps)',  "{}_{}_throughput_violin".format (expid, runid))

plotTimeseries(throughput_all, streaming_time_all, exp_labels_streaming, 180,  'Throughput (Mbps)',  "{}_{}_throughput_time".format (expid, runid))


#plotTimeseries(delay_all, control_time_all, exp_labels_control, 30,  'Delay (ms)',  "{}_{}_delay_time".format (expid, runid))

plotTimeseries(pdr_all, streaming_time_all, exp_labels_streaming_pdr, 180,  'PDR (%)',  "{}_{}_pdr_time".format (expid, runid))
plotViolin(pdr_all, exp_labels_streaming_pdr, 180,  'PDR (%)',  "{}_{}_pdr_violin".format (expid, runid))

# make box whisker plot
# make super plot

print ("Done.")
sys.exit()