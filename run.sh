set -x

echo "starting full test.."
echo "starting iperf with TCP UL stream.."
python script.py $1 $2_tcpstreamsingleUL "iperf3 -c localhost -p 3000 -t "$3" -J -b 1800M" &
python udp_rx.py $1 $2_control_withTCPUL localhost 6000 $3 &
echo "finished.."

wait

echo "starting iperf with TCP UL+DL stream.."
python script.py $1 $2_tcpstreamUL "iperf3 -c localhost -p 3000 -t "$3" -J -b 1800M" &
python script.py $1 $2_tcpstreamDL "iperf3 -c localhost -p 3001 -t "$3" -J -b 1800M -R" &
python udp_rx.py $1 $2_control_withTCPULDL localhost 6000 $3 &
echo "finished.."

wait

echo "starting iperf with TCP UL+ UDP DL stream.."
python script.py $1 $2_tcpstreamULUDP "iperf3 -c localhost -p 3000 -t "$3" -J -b 1800M" &
python script.py $1 $2_tcpstreamUDPDL "iperf3 -c localhost -p 3001 -t "$3" -J -b 1800M -u -l 65500 -R" &
python udp_rx.py $1 $2_control_withTCPULUDPDL localhost 6000 $3 &
echo "finished.."


wait

echo "starting iperf with UDP UL stream.."
python script.py $1 $2_udpstreamsingleUL "iperf3 -c localhost -p 3000 -t "$3" -u -l 65500 -J -b 1800M" &
python udp_rx.py $1 $2_control_withUDPUL localhost 6000 $3 &
echo "finished.."


wait

echo "starting iperf with UDP UL+DL stream.."
python script.py $1 $2_udpstreamUL "iperf3 -c localhost -p 3000 -t "$3" -u -l 65500 -J -b 1800M" &
python script.py $1 $2_udpstreamDL "iperf3 -c localhost -p 3001 -t "$3" -u -l 65500 -J -b 1800M -R" &
python udp_rx.py $1 $2_control_withUDPULDL localhost 6000 $3 &
echo "finished.."

wait

echo "starting iperf with UDP UL+ TCP DL stream.."
python script.py $1 $2_udpstream_TCPDL "iperf3 -c localhost -p 3000 -t "$3" -u -l 65500 -J -b 1800M" &
python script.py $1 $2_udpstream_DLTCP "iperf3 -c localhost -p 3001 -t "$3" -J -b 1800M -R" &
python udp_rx.py $1 $2_control_withUDPULTCPDL localhost 6000 $3 &

wait
echo "range test finished.."

$SHELL