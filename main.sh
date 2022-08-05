 #! /bin/sh
set -x
date 

# =============================================================================

echo "testing AX 20 MHz @ 24  GHz"

powershell -File config_switch.ps1 63 "INSA DLINK 2.4GHz"
sleep 20

echo "start"
./run.sh $1"_ax_20mhz_24ghz" $2 $3 1800M
echo "end"

wait

# =============================================================================

echo "testing AX 20 MHz @ 5   GHz"

powershell -File config_switch.ps1 63 "INSA DLINK 5GHz"
sleep 20

echo "start"
./run.sh $1"_ax_20mhz_5ghz" $2 $3 1800M

echo "end"

wait

# =============================================================================

echo "testing AC 20 MHz @ 5   GHz"

powershell -File config_switch.ps1 26 "INSA DLINK 5GHz"
sleep 20

echo "start"
./run.sh $1"_ac_20mhz_5ghz" $2 $3 1000M
echo "end"

wait

# =============================================================================

echo "testing N  20 MHz @ 2.4 GHz"

powershell -File config_switch.ps1 13 "INSA DLINK 2.4GHz"
sleep 20

echo "start"
./run.sh $1"_n_20mhz_24ghz" $2 $3 1000M
echo "end"

wait

# =============================================================================

echo "testing N  20 MHz @ 5   GHz"

powershell -File config_switch.ps1 10 "INSA DLINK 5GHz"
sleep 20

echo "start"
./run.sh $1"_n_20mhz_5ghz" $2 $3 1000M
echo "end"

wait

# =============================================================================

# echo "testing G  20 MHz @ 2.4 GHz"

# powershell -File config_switch.ps1 5 "INSA DLINK 2.4GHz"
# sleep 20

# echo "start"
# ./run.sh $1"_g_20mhz_24ghz" $2 $3 25M 1000M
# echo "end"


# wait

# =============================================================================

# echo "testing A  20 MHz @ 5 GHz"


# powershell -File config_switch.ps1 2 "INSA DLINK 5GHz"
# sleep 20

# echo "start"
# ./run.sh $1"_a_20mhz_5ghz" $2 $3 25M
# echo "end"

# wait

# =============================================================================

# echo "testing B  20 MHz @ 2.4 GHz"

# powershell -File config_switch.ps1 1 "INSA DLINK 2.4GHz"
# sleep 20

# echo "start"
# ./run.sh $1"_b_20mhz_24ghz" $2 $3 5M
# echo "end"


# wait


echo "done."
$SHELL