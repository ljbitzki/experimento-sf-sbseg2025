#!/bin/bash

TAPI="/tmp/triggered_dos.api"
while true; do
    if [ "$( iptables -nL | grep -c 'TrueState-SNA - DoS' )" -eq 1 ]; then
        sleep 5
        if [ "$( iptables -nL | grep -c 'TrueState-SNA - DoS' )" -eq 0 ]; then
            if [ "$( grep -c '172.18.0.' "${TAPI}" )" -gt 0 ]; then
                echo '' > "${TAPI}"
            fi
        fi
    fi
    sleep 0.4
done