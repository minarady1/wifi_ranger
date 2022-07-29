 #! /bin/sh
set -x

echo "testing ax 5 GHz "
powershell -File main.ps1 63 "INSA DLINK 5GHz"
sleep 10

echo "start"
./run.sh $1"_ax_5ghz_20mhz" run5 10
echo "end"

echo "testing ax 2.4 GHz "
# ax 2.4
powershell -File main.ps1 63 "INSA DLINK 2.4GHz"
sleep 10

./run.sh $1"_ax_24ghz_20mhz" run5 10

wait

echo "done."
$SHELL