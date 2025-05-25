#!/bin/bash
cat <<'EOF' > "/usr/local/bin/ok.sh"
#!/bin/bash
while true; do
    S=$(( ( RANDOM % 3 )  + 1 ))
    for j in $( seq 1 $S ); do
      curl http://172.18.0.9 > /dev/null 2>&1
    done
  sleep 1
done
EOF
chmod +x "/usr/local/bin/ok.sh"
/usr/local/bin/ok.sh &

sleep 9999999
/bin/bash
