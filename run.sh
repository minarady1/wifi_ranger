set -x

echo "starting full test.."
echo "starting iperf with TCP UL stream.."
python wifiinfo.py $1 $2_wifi $3
python iperf.py $1 $2_tcpstreamsingleUL "iperf3 -c 10.90.90.1 -p 3000 -t "$3" -J -b 1800M" &
python udp_rx.py $1 $2_control_withTCPUL 10.90.90.2 6000 $3 &
echo "finished.."

wait

echo "starting iperf with TCP UL+DL stream.."
python wifiinfo.py $1 $2_wifi $3
python iperf.py $1 $2_tcpstreamUL "iperf3 -c 10.90.90.1 -p 3001 -t "$3" -J -b 1800M" &
python iperf.py $1 $2_tcpstreamDL "iperf3 -c 10.90.90.1 -p 3002 -t "$3" -J -b 1800M -R" &
python udp_rx.py $1 $2_control_withTCPULDL 10.90.90.2 6000 $3 &
echo "finished.."

wait

# echo "starting iperf with TCP UL+ UDP DL stream.."
# python iperf.py $1 $2_tcpstreamULUDP "iperf3 -c 10.90.90.1 -p 3003 -t "$3" -J -b 1800M" &
# python iperf.py $1 $2_tcpstreamUDPDL "iperf3 -c 10.90.90.1 -p 3004 -t "$3" -J -b 1800M -u -l 65500 -R" &
# python udp_rx.py $1 $2_control_withTCPULUDPDL 10.90.90.2 6000 $3 &
# echo "finished.."


# wait

# echo "starting iperf with UDP UL stream.."
# python iperf.py $1 $2_udpstreamsingleUL "iperf3 -c 10.90.90.1 -p 3005 -t "$3" -u -l 65500 -J -b 1800M" &
# python udp_rx.py $1 $2_control_withUDPUL 10.90.90.2 6000 $3 &
# echo "finished.."




# echo "starting iperf with UDP UL+DL stream.."
# python iperf.py $1 $2_udpstreamUL "iperf3 -c 10.90.90.1 -p 3006 -t "$3" -u -l 65500 -J -b 1800M" &
# python iperf.py $1 $2_udpstreamDL "iperf3 -c 10.90.90.1 -p 3007 -t "$3" -u -l 65500 -J -b 1800M -R" &
# python udp_rx.py $1 $2_control_withUDPULDL 10.90.90.2 6000 $3 &
# echo "finished.."

# wait

# echo "starting iperf with UDP UL+ TCP DL stream.."
# python iperf.py $1 $2_udpstream_TCPDL "iperf3 -c 10.90.90.1 -p 3008 -t "$3" -u -l 65500 -J -b 1800M" &
# python iperf.py $1 $2_udpstream_DLTCP "iperf3 -c 10.90.90.1 -p 3009 -t "$3" -J -b 1800M -R" &
# python udp_rx.py $1 $2_control_withUDPULTCPDL 10.90.90.2 6000 $3 &

# wait
echo "range test finished.."
