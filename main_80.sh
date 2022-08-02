#! /bin/sh
set -x
date 



# =============================================================================

echo "testing AX 80 MHz @ 5   GHz"

powershell -File config_switch.ps1 63 "INSA DLINK 5GHz"
sleep 20

echo "start"
./run.sh $1"_ax_80mhz_5ghz" $2 $3 1800M

echo "end"

wait

# =============================================================================

echo "testing AC 80 MHz @ 5   GHz"

powershell -File config_switch.ps1 26 "INSA DLINK 5GHz"
sleep 20

echo "start"
./run.sh $1"_ac_80mhz_5ghz" $2 $3 1000M
echo "end"

wait
$SHELL
