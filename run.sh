set -x

echo "starting full test.. duration:"$3 "s"

#==============================================================================
date +"%T"
echo "starting iperf with UDP UL stream.."
python wifiinfo.py $1 $2_udp_single_UL_wifi $3 &
python iperf.py $1 $2_udp_single_UL "iperf3 -c 10.90.90.1 -p 3000 -t "$3" -u -l 1400 -J -b "$4 
echo "finished.."

wait

#==============================================================================

date +"%T"
echo "starting iperf with UDP UL low throughput stream.."
python wifiinfo.py $1 $2_udp_single_UL_low_wifi $3 &
python iperf.py $1 $2_udp_single_UL_low "iperf3 -c 10.90.90.1 -p 3001 -t "$3" -u -l 1400 -J -b 1M" 
echo "finished.."

wait

#==============================================================================

date +"%T"
echo "starting iperf with UDP DL stream.."
python wifiinfo.py $1 $2_udp_single_DL_wifi $3 &
python iperf.py $1 $2_udp_single_DL "iperf3 -c 10.90.90.1 -p 3002 -t "$3" -u -l 1400 -J -b "$4" -R" 
echo "finished.."

wait

date +"%T"
echo "starting iperf with UDP DL low throughput stream.."
python wifiinfo.py $1 $2_udp_single_DL_low_wifi $3 &
python iperf.py $1 $2_udp_single_DL_low "iperf3 -c 10.90.90.1 -p 3003 -t "$3" -u -l 1400 -J -b 1M -R" 
echo "finished.."

wait


#==============================================================================

echo "starting iperf with TCP UL stream.."

date +"%T"
python wifiinfo.py $1 $2_tcp_single_UL $3 &
python iperf.py $1 $2_tcp_single_UL "iperf3 -c 10.90.90.1 -p 3004 -t "$3" -J -b "$4 &
echo "finished.."

wait

#==============================================================================

date +"%T"
echo "starting full test.. duration:"$3
echo "starting iperf with TCP UL stream.."
python wifiinfo.py $1 $2_tcp_single_DL_wifi $3 &
python iperf.py $1 $2_tcp_single_DL "iperf3 -c 10.90.90.1 -p 3005 -t "$3" -J -b "$4" -R" &
echo "finished.."

wait



echo "range test finished.."

