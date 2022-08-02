#! /usr/bin/pwsh

$config = $args[0]
$band = $args[1]

"configuring network"
Set-NetAdapterAdvancedProperty -Name "WiFi 2" -RegistryKeyword "WifiProtocol_phy0" -RegistryValue $config;

WifiInfoView /ConnectAP "$band";

"Done."
