set -x
echo "starting RSSI test.."
python client.py 1 UDP 10000 10      >> $1
echo "starting iperf tests.."
iperf3 -c 10.90.90.1 -p 3000   -t 120  >> $1
iperf3 -c 10.90.90.1 -p 3000   -u -l 65500 -b 1800M -t 120 >> $1
echo "finished.."
$SHELL