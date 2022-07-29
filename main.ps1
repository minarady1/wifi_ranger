#! /usr/bin/pwsh

"Testing ax 5 GHz"
$config = $args[0]
$band = $args[1]
# ax 5

"configuring network"
Set-NetAdapterAdvancedProperty -Name "WiFi 2" -RegistryKeyword "WifiProtocol_phy0" -RegistryValue $config;
WifiInfoView /ConnectAP "$band";

"done."
