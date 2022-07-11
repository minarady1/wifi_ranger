set -x
echo "starting iperf with UDP stream.."
python iperf.py $1 $2_udpstream "iperf3 -c localhost -p 4000 -t 15 -J -u -l 65500 -b 27M" &
python iperf.py $1 $2_control_withudp "iperf3 -c localhost -p 3000 -t 15 -u -l 100 -J -R"
echo "finished.."

echo "starting iperf with UDP stream.."
python iperf.py $1 $2_tcpstream "iperf3 -c localhost -p 4000 -t 15 -J -b 27M" &
python iperf.py $1 $2_control_withtcp "iperf3 -c localhost -p 3000 -t 15 -u -l 100 -J -R"
echo "finished.."
$SHELL