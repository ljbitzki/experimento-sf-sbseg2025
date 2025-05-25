#!/bin/bash
echo "Iniciando SSH"
/usr/sbin/service ssh start
sleep 0.5
echo "Iniciando nginx"
/usr/sbin/service nginx start
sleep 0.5
echo "Iniciando iptables"
sudo /etc/init.d/firewall start
sleep 0.5
echo "Iniciando sensor DDoS"
/usr/local/bin/sensor.sh &
echo "Iniciando monitor"
/usr/local/bin/monitor.sh &
sleep 9999999
/bin/bash
