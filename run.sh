set -x
echo "starting iperf with UDP stream.."
python iperf.py $1 $2_tcpstream "iperf3 -c 10.90.90.1 -p 4000 -t 15 -J -b 27M" &
# python udp_rx.py $1 $2_control_withtcp 10.90.90.2 6000
ping 10.90.90.2 -n 15 -w 2000 >> logs/ping_$1_$2_tcpsteram.json
echo "finished.."

echo "starting iperf with UDP stream.."
python iperf.py $1 $2_udpstream "iperf3 -c 10.90.90.1 -p 5000 -t 15 -J -u -l 65500 -b 27M" &
#python udp_rx.py $1 $2_control_withudp 10.90.90.2 6000 15
ping 10.90.90.2 -n 15 -w 2000 >> logs/ping_$1_$2_udpstream.json
echo "finished.."


$SHELL