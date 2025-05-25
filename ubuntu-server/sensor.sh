#!/bin/bash
echo "Starting sensor"
CSV="/var/www/html/hits.csv"
echo 'time,ip,hps' > "${CSV}"
DFILE="/tmp/triggered_dos.api"
echo '' > "${DFILE}"
IS_UP='0'
SELF=$( ip a | grep -A2 'BROADCAST,MULTICAST,UP,LOWER_UP' | grep 'inet' | awk -F '/' '{print $1}' | awk '{print $2}' )
SVC_PORT="80"
SVC_PROTO="TCP"
while true; do
    if [ "$( grep -c ',,' "${CSV}" )" -gt 0 ]; then
        sed -i '/,,/d' "${CSV}"
    fi
    IP=''
    DOS=''
    LOGS=''
    if [ "${IS_UP}" -eq 0 ]; then
        NGINX=$( ss -tulpan | grep -Ec '0\.0\.0\.0\:80.*nginx' )
        if [[ "${NGINX}" -gt 0 ]]; then
            curl -s -X POST -H "Content-Type: application/json" http://172.18.0.8:8000/devctrl/svc-server-up/ --data "{ \"server_ip\": \"${SELF}\", \"port\": \"${SVC_PORT}\", \"proto\": \"${SVC_PROTO}\" }"
            IS_UP='1'
        fi
    fi
    curl -s localhost > /dev/null 2>&1
    SECS=$( date -d "$date +10797 seconds" +"%d/%b/%Y:%H:%M:%S" )
    LOGS=$( awk -v ts="$SECS" '$0 ~ ts {found=1} found' "/var/log/nginx/access.log" | awk '{print $1}' | sort | uniq -c )
    SUM=0
    while read -r HIT IP; do
        SUM=$(( SUM + HIT ))
    done < <( echo -e "${LOGS}" | xargs -n 2 )
    echo "$(date +%s),172.18.0.1,${SUM}" >> "${CSV}"
    HIT=0
    while read -r HIT IP; do
    SUM=0
    if [ "${IP}" != '::1' ]; then
        DOS=$( echo "${HIT}" | awk '{ if( $1 > 30 ) { print $1 }}' )
        if [ "$( grep -c "${IP}" "${DFILE}" )" -eq 0 ]; then
            if [ "${DOS}" != "" ]; then
                    curl -s -X POST -H "Content-Type: application/json" http://172.18.0.8:8000/devctrl/svc-ddos/ --data "{ \"server_ip\": \"${SELF}\", \"source\": \"${IP}\", \"port\": \"${SVC_PORT}\", \"proto\": \"${SVC_PROTO}\" }"
                echo "${IP}" >> "${DFILE}"
            fi
        fi
    fi
    done < <( echo -e "${LOGS}" | xargs -n 2 )
sleep 1
done
